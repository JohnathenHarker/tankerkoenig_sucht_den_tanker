from Input import *

from Strategy import Strategy
from Model import Model

import os.path


class Supervisor:
	"""
	manages workflow
	"""

	def __init__(self):

		self.gasStation = GasStation()

	def handleRoute(self, file):
		route = Route()
		route.read(file)
		model = Model()
		model.train(self.gasStation, route.route[0][0][0]-1, 500)

		print("Starting to calculate prize for each station on route")
		prizeList = []
		for element in route.route:
			(date, hour), ID, prize, amount = element
			prizeList.append(model.forecast(ID, date, hour, self.gasStation))

		route.appendPrize(prizeList)
		print("Finished calculating")

		#calculating best tanking strategy
		strategy = Strategy(self.gasStation)
		strategy.calculate(route)

		#writing route
		route.write(file)



	def handlePrizingForecast(self, file):
		prizingForecast = PrizingForecast()
		prizingForecast.read(file)

		model = Model()

		print("Starting to calculate forecasts")
		prizeList = []
		for element in prizingForecast.forecastParameter:
			((lastKnownDate,lastKnownHour),(forecastDate, forecastHour)), ID, prize = element
			model.train(self.gasStation, lastKnownDate, 500)
			prizeList.append(int(model.forecast(ID, forecastDate, forecastHour, self.gasStation)))
		print("Finished forecasts")

		prizingForecast.appendPrize(prizeList)

		prizingForecast.write(file)




	def handleHandle(self):		
		with open("config", encoding='utf-8') as file:
			for line in file:
				if line.__contains__("#") or line.strip() == "":
					pass
				else:
					listList = line.split(";")
					command = listList[0].strip()
					path = listList[1].strip()

					if command == "route" or command == "Route":
						if os.path.isfile(path):
							self.handleRoute(path)
						else:
							print("Invalid path", path)
					elif command == "forecast" or command == "Forecast":

						if os.path.isfile(path):
							self.handlePrizingForecast(path)
						else:
							print("Invalid path", path)
					else:
						print("Invalid command", command)
