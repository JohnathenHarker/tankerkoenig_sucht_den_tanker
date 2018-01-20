from Input import *

from Strategy import Strategy
from Model import Model

import os.path


class Supervisor:
	"""
	manages workflow
	"""


	"""
		gasStation = GasStation()
		route = Route("../geg. Dateien/Eingabedaten/Fahrzeugrouten/Bertha Benz Memorial Route.csv")
		strategy = Strategy()
		L = [1] * 31
		route.appendPrize(L)
		print(route.route)
		t = time.clock()
		strategy.calculate(route, gasStation)
		print(route.route)
	"""

	def __init__(self):
		""" TO DO:
		create gas stations, read historic data from files
		"""
		self.gasStation = GasStation()

	def handleRoute(self, file):
		""" TO DO:
		- input route
		- create model
		- train model
		- predict prizes --> appendPrize
		- call Strategy with 'new' route
		- call appendAmount(Strategys solution)
		- write solution to file
		"""

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
		""" TO DO:
		- input requests
		- for each request:
			- create model
			- train model
			- make prediction
		- store results in list
		- call appendPrize(list)
		- write solution to file
		"""

		prizingForecast = PrizingForecast()
		prizingForecast.read(file)

		model = Model()

		print("Starting to calculate forecasts")
		prizeList = []
		for element in prizingForecast.forecastParameter:
			((lastKnownDate,lastKnownHour),(forecastDate, forecastHour)), ID, prize = element
			model.train(self.gasStation, lastKnownDate, 500)
			prizeList.append(model.forecast(ID, forecastDate, forecastHour, self.gasStation))
		print("Finished forecasts")

		prizingForecast.appendPrize(prizeList)

		prizingForecast.write(file)




	def handleHandle(self):
		""" TO DO:
		- call right function at the right time
		- control user
		"""
		"""
		m = Model()
		m.train(self.gasStation, 700, 500)
		#for i in [1,2,3,4,5,10,15, 20, 25, 30]:
		for i in [30]:
			print(m.forecast(6, 400+i, 4, self.gasStation))
			print(self.gasStation.findID(6)[4][400+i][4])
		m.evaluate(self.gasStation)
		"""

		with open("config", encoding='utf-8') as file:
			for line in file:
				if line.__contains__("#"):
					pass
				else:
					listList = line.split(";")
					command = listList[0]
					path = listList[1]

					if command == "route" or command == "Route":
						if os.path.isfile(path):
							self.handleRoute(listList[1])
						else:
							print("Invalid path", path)
					elif command == "forecast" or command == "Forecast":

						if os.path.isfile(path):
							self.handlePrizingForecast(listList[1])
						else:
							print("Invalid path", path)
					else:
						print("Invalid command", command)
