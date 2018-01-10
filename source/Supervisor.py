from Input import *

from Strategy import Strategy
from Model import Model


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
		self.gasStations = GasStation()

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

	def handleHandle(self):
		""" TO DO:
		- call right function at the right time
		- control user
		"""
		m = Model()
		m.train(self.gasStations, 400, 500)
		#for i in [1,2,3,4,5,10,15, 20, 25, 30]:
		for i in [30]:
			print(m.forecast(6, 400+i, 4, self.gasStations))
			print(self.gasStations.findID(6)[4][400+i][4])
		m.evaluate(self.gasStations)
