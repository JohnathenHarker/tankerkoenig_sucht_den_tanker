import csv 
import math as M
import time
import os.path

def parseDate(date):
	# parses date (day and time) to day, hour
	
	# day zero = 2014-07-01
	day_zero = 182
	
	year = int(date[0:4])
	month = int(date[5:7])
	day = int(date[8:10])
	hour = int(date[11:13])+int(date[19:22])
	
	
	# calculate the day after day_zero
	normalized_day = (year-2014) *365 + M.floor((year-2014 + 1)/4) -day_zero
	if month > 1:
		normalized_day = normalized_day +31
	if month > 2 and year % 4 == 0:
		normalized_day = normalized_day +29
	elif month > 2:
		normalized_day = normalized_day +28
	if month > 3:
		normalized_day = normalized_day +31
	if month > 4:
		normalized_day = normalized_day +30
	if month > 5:
		normalized_day = normalized_day +31
	if month > 6:
		normalized_day = normalized_day +30
	if month > 7:
		normalized_day = normalized_day +31
	if month > 8:
		normalized_day = normalized_day +31
	if month > 9:
		normalized_day = normalized_day +30
	if month > 10:
		normalized_day = normalized_day +31
	if month > 11:
		normalized_day = normalized_day +30
		
	normalized_day = normalized_day + day
		
	# last three values probably not needed
	return (normalized_day, hour)#, year, month, day)

class GasStation:
	"""
	represents set of gas stations with ID, position, prizes
	"""
	
	
	def __init__(self):
		
		#missingData = [5,7,33, 249, 291, 344, 345, 378, 386, 461, 536, 553, 554, 584, 591, 642, 643, 654]
		
		
		self.prizingTable = []
		
		# read table of gas stations
		with open('geg. Dateien/Eingabedaten/Tankstellen.csv') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=';')
			id = 1
			for row in readCSV:
				print("read gas station", id, end="\r")
				if id != int(row[0]):
					print("ERROR: fehlerhafte Tankstellenliste")
				marke = row[2]
				nord = float(row[7])
				ost = float(row[8])
								
				self.prizingTable.append((id, marke, nord, ost, self.read(10, id)))
				id = id+1
		# read historic data

		print ("completed")
	
	def findID(self, ID):
		""" TO DO:
		- find ID --> return position (and historic prizing data?)
		"""
		if ID == self.prizingTable[ID-1][0]:
			return self.prizingTable[ID-1]
		else:
			return
	
	def read(self, endDay, ID):
		
		# read historic data for given gas station till given day
		
		data = []
		oneDay = []
		d = 0
		h = 0
		prize = 0
		path = 'geg. Dateien/Eingabedaten/Benzinpreise/'+str(ID)+'.csv'
		
		# check wether file exists
		if os.path.isfile(path):
			with open(path) as csvfile:
				readCSV = csv.reader(csvfile, delimiter=';')
				row = next(readCSV)
				
				# first date in file
				day, hour = parseDate(row[0])
				
				while d < endDay:
					while day > d or (day == d and hour > h):
						oneDay.append(prize)
						if h < 23:
							h = h+1
						else:
							# day is over --> append data
							h = 0
							data.append(oneDay)
							oneDay = []
							d = d+1
					prize = int(row[1])
					defaultRow = row
					row = next(readCSV, defaultRow)
					if row != defaultRow:
						day, hour = parseDate(row[0])
					else:
						# no more new data in file --> use last data
						day, hour = endDay+1, 23
		return data
				
		
		
	def print(self):
		# prints all gas stations with positions
		for station in self.prizingTable:
			if station[0] < 10:
				print("ID:", station[0], station[1], "\tN:", station[2], "\tE:", station[3]) 

class Strategy:
	"""
	calculates the optimal fueling strategy for path with known prizes
	formerly known as tFontF
	"""
	def __init__(self):
		print("Calculating best route")
		self.capacity = 0
		self.route = []
		self.possibleRoutes = {}
        self.gasStation = None


	def calculate(self, route, gasStation):
		""" TO DO:
		- compute best strategy for fueling and return it
		"""
		self.capacity = route.capacity
		self.route = route.route
		self.gasStation = gasStation
		nullRoute = [0] * len(self.route)
		self.helpCalculate(0,0,0,nullRoute)
		self.possibleRoutes = {}
        route.appendAmount(self.possibleRoutes[min(list(self.possibleRoutes.keys()))])


	def helpCalculate(self, currentNode, currentGas, currentCost, previousRoute):
		def prize(position):
			return int(self.route[position][2])

		if currentNode == len(self.route)-1:
			previousRouteCopy = previousRoute[:]
			self.possibleRoutes[currentCost] = previousRouteCopy
			return

		for node in range(currentNode+1, len(self.route)):
			if self.consumption(currentNode, node) <= self.capacity:
				previousRouteCopy = previousRoute[:]

				if prize(node) <= prize(currentNode) and currentGas <= self.consumption(currentNode, node):
					previousRouteCopy[currentNode] = self.consumption(currentNode, node) - currentGas
					self.helpCalculate(node, 0, currentCost + (self.consumption(currentNode, node)-currentGas) * prize(currentNode), previousRouteCopy)
				elif prize(node) > prize(currentNode):
					previousRouteCopy[currentNode] = self.capacity - currentGas
					self.helpCalculate(node, self.capacity - self.consumption(currentNode, node), currentCost + (self.capacity - currentGas) * prize(currentNode), previousRouteCopy)
		return

	def consumption(self, currentNode, targetNode):
		def distance(self, station1, station2):
			def lat(stationNr):
				return self.gasStation.findID(stationNr)[7]

			def lon(stationNr):
				return self.gasStation.findID(stationNr)[8]

			return 6378.388 * M.acos(M.sin(lat(station1)) * M.sin(lat(station2)) + M.cos(lat(station1)) * M.cos(lat(station2)) * M.cos(lon(station2) - lon(station1)))

		def getIDfromPosInRoute(position):
			if position >= len(self.route):
				print("ERROR in getID function")
				return 0
			return int(self.route[position][1])

		if currentNode == targetNode:
			return 0
		else:
			dist = distance(getIDfromPosInRoute(currentNode), getIDfromPosInRoute(currentNode+1))
			consumptionPerKilometer = 5.6
			consumptionToNext = 1.0 * dist / consumptionPerKilometer
			return consumptionToNext + self.consumption(currentNode+1, targetNode)

		
class Route:
	"""
	stores a route with (predicted) prizes and fueling amounts
	"""
	
	
	def __init__(self, file):
		# inputs file instantly
		print("input route")
		#route is a tuple of capacity and the list of tuples of arrival time, id, prize and amount of a certain gas station
		self.capacity = 0
		self.route = []
		self.read(file)
	
	def read(self, file):
		""" TO DO:
		- input file
		"""
		self.capacity = 0
		self.route = []
		routelist = []

		with open(file) as routefile:
			first_line = True
			for line in routefile:
				if first_line:
					self.capacity = int(line)
					first_line = False
				else:
					linelist = line.split(";")
					#(date, id, prize, amount)
					routelist.append((parseDate(linelist[0]),int(linelist[1]),0,0))

		self.route = routelist[:]
		return (self.capacity, self.route)


	def appendPrize(self, listOfPrizes):
		""" TO DO:
		- add prize to each gas station
		"""

		if len(listOfPrizes) != len(self.route):
			print("Error in appendPrize method")

		counter = 0

		while counter < len(listOfPrizes) and counter < len(self.route):
			templist = list(self.route[counter])
			templist[2] = listOfPrizes[counter]
			self.route[counter] = tuple(templist)

			counter += 1
		
	def appendAmount(self, listOfAmounts):
		""" TO DO:
		- add amount of fuel to each gas station
		"""

		if len(listOfAmounts) != len(self.route):
			print("ERROR in appendAmount method")

		counter = 0

		while counter < len(listOfAmounts) and counter < len(self.route):
			templist = list(self.route[counter])
			templist[3] = listOfAmounts[counter]
			self.route[counter] = tuple(templist)

			counter += 1
		
	def getCapacity(self):
		return self.capacity
	
	def write(self, file):
		""" TO DO:
		- write data to file
		"""

		readlines = []
		with open(file, "r") as f:
			first_line = True
			for line in file:
				if first_line:
					first_line = False
				else:
					readlines.append(line)

		with open(file, "w") as f:
			counter = 0
			for line in readlines:
				f.write(line + ";" + str(self.route[counter][2]) + ";" + str(self.route[counter][3]))
				counter += 1

class PrizingForecast:
	"""
	handles files with prize requests
	"""

	def __init__(self, file):
		#contains a list of tuples consisting of endDate, forecastDate and the gas station id
		self.forecastParameter = []
		self.read(file)

	def read(self, file):
		""" TO DO:
		- import data from file--> store in forecastParameters
		"""

		with open(file, "r") as f:
			self.forecastParameter = []
			for line in f:
				#(endDate, forecastDate, id, prize)
				lineValues = tuple(line.split(";"))
				self.forecastParameter.append((parseDate(lineValues[0]), parseDate(lineValues[1]), int(lineValues[2]), 0))
		
	def appendPrize(self, listOfPrizes):
		""" TO DO:
		- add prizes to each request
		"""

		counter = 0

		while counter < len(listOfPrizes) and counter < len(self.forecastParameter):
			templist = list(self.forecastParameter[counter])
			templist[3] = listOfPrizes[counter]
			self.forecastParameter[counter] = tuple(templist)

			counter += 1
		
	def getForecastParams(self):
		return self.forecastParameter
	
	def write(self, file):
		""" TO DO:
		write data to file
		"""

		readlines = []
		with open(file, "r") as f:
			for line in file:
				readlines.append(line)

		with open(file, "w") as f:
			counter = 0
			for line in readlines:
				f.write(line + ";" + str(self.forecastParameter[counter][3]))
				counter += 1


class Model:
	"""
	makes predictions for the prize of gas
	"""
	
	
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

		
		
t1 = time.clock()		
		
S = Supervisor()
S.handleHandle()

t2 = time.clock()

dt = t2-t1
print("Zeit:", dt)
