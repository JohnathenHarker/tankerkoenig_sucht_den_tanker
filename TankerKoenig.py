import csv 
import math as M
import time

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
		
		missingData = [5,7,33, 249, 291, 344, 345, 378, 386, 461, 536, 553, 554, 584, 591, 642, 643, 654]
		print("input gas stations")
		""" TO DO: 
		- input IDs and position of gas stations
		- input historic data
		"""
		
		
		self.prizingTable = []
		
		# read table of gas stations
		with open('geg. Dateien/Eingabedaten/Tankstellen.csv') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=';')
			id = 1
			for row in readCSV:
				print("read gas station", id)
				if id != int(row[0]):
					print("ERROR: fehlerhafte Tankstellenliste")
				marke = row[2]
				nord = float(row[7])
				sued = float(row[8])
				
				# Bedingung muss DRINGEND noch angepasst werden
				if id %600+1 not in missingData:
					self.prizingTable.append((id, marke, nord, sued, self.read(1000, id%600+1)))
				#self.prizingTable.append((id, marke, nord, sued, self.read(600, id)))
				id = id+1
		# read historic data

		print ("completed")
	
	def findID(self, ID):
		""" TO DO:
		- find ID --> return position (and historic prizing data?)
		"""
	
	def read(self, endDay, ID):
		
		# read historic data for given gas station till given day
		
		data = []
		oneDay = []
		d = 0
		h = 0
		prize = 0
		with open('geg. Dateien/Eingabedaten/Benzinpreise/'+str(ID)+'.csv') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=';')
			row = next(readCSV)
			day, hour = parseDate(row[0])
			while d < endDay:
				
				while day > d or (day == d and hour > h):
					oneDay.append(prize)
					if h < 23:
						h = h+1
					else:
						h = 0
						data.append(day)
						oneDay = [];
						d = d+1
				prize = int(row[1])
				defaultRow = row
				row = next(readCSV, defaultRow)
				if row != defaultRow:
					day, hour = parseDate(row[0])
				else:
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
	def calculate(route, gasStation):
		""" TO DO:
		- compute best strategy for fueling and return it
		"""

		
class Route:
	"""
	stores a route with (predicted) prizes and fueling amounts
	"""
	
	
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
		input('hi')

		
		
t1 = time.clock()		
		
S = Supervisor()
S.handleHandle()

t2 = time.clock()

dt = t1-t2
print("Zeit:", dt)
