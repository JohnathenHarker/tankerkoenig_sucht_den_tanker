class GasStation:
	"""
	represents set of gas stations with ID, position, prizes
	"""
	prizingTable
	
	
	def __init__(self):
		print("input gas stations")
		""" TO DO: 
		- input IDs and position of gas stations
		- input historic data
		"""
		print ("completed")
	
	def findID(self):
		""" TO DO:
		- find ID --> return position (and historic prizing data?)
		"""
	
	def read(self, day, ID):
		""" TO DO:
		- read historic data for given day and gas station
		"""
		
class Strategy:
	"""
	calculates the optimal fueling strategy for path with known prizes
	formerly known as tFontF
	"""
	def calculate(route, gasStation):
		""" TO DO:
		- compute best strategy for fueling and return it
		"""

		
class Route:
	"""
	stores a route with (predicted) prizes and fueling amounts
	"""
	route
	capacity
	
	def __init__(self, file):
		# inputs file instantly
		self.read(file)
	
	def read(self, file):
		""" TO DO:
		- input file
		"""
	
	def appendPrize(self, listOfPrizes):
		""" TO DO:
		- add prize to each gas station
		"""
		
	def appendAmount(self, ListOfAmounts):
		""" TO DO:
		- add amount of fuell to each gas station
		"""
		
	def getCapaity(self):
		return self.capacity
	
	def write(self):
		""" TO DO:
		- write data to file
		"""
	
		
class PrizingForecast:
	"""
	handles files with prize requests
	"""
	
	forecastParameters
	
	def read(self, file):
		""" TO DO:
		- import data from file--> store in forecastParameters
		"""
		
	def appendPrize(self, listOfPrizes):
		""" TO DO:
		- add prizes to each request
		"""
		
	def getForecastParams(self):
		return self.forecastParameters
	
	def write(self):
		""" TO DO:
		write data to file
		"""
	
		
		
		
		
class Model:
	"""
	makes predictions for the prize of gas
	"""
	
	data
	
	def train(self, data):
		""" TO DO:
		train the SOFM with teh given data
		"""
		
	def forecast(self, date):
		""" TO DO:
		predict prize
		"""
		
class Supervisor:
	"""
	manages workflow
	"""
	
	def __init__(self):
		""" TO DO:
		create gas stations, read historic data from files
		"""
	
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