import os.path
import csv 
import math as M
import numpy as np
from neupy import algorithms, environment
import time
import random




NUMBER_OF_EPOCHS = 100
random.seed(42)


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
		self.count = 0	# counts number of gasStations
		self.prizingTable = []
		t1 = time.clock()	
		# read table of gas stations
		with open('geg. Dateien/Eingabedaten/Tankstellen_short.csv') as csvfile:
		#with open('geg. Dateien/Eingabedaten/Tankstellen.csv') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=';')
			id = 1
			for row in readCSV:
				print("read gas station", id, end="\r")
				if id != int(row[0]):
					print("ERROR: fehlerhafte Tankstellenliste")
				marke = row[2]
				nord = float(row[7])
				sued = float(row[8])
								
				self.prizingTable.append((id, marke, nord, sued, self.read(500, id)))
				id = id+1
		# read historic data

		self.fillMissingData()
		
		t2 = time.clock()
		dt = t2-t1
		print("")
		print ("reading gas stations completed in", dt, "seconds")
	
	def noData(self, ID):
		return self.findID(ID)[4] == []
	
	def findID(self, ID):
		""" TO DO:
		- find ID --> return position (and historic prizing data?)
		"""
		if ID == self.prizingTable[ID-1][0]:
			return self.prizingTable[ID-1]
		
	def setID(self, ID, data):
		if ID == self.prizingTable[ID-1][0]:
			self.prizingTable[ID-1] = data[:]
	
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
			self.count = self.count +1
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
				
				
	def randomData(self, ID, date):
		# returns random data sample of 8 days
		
		if self.findID(ID)[4] == []:
			print ("ERROR: no data found for gas station", ID)
		else:
			day = int(random.random() * (date - 8))
			i = 0
			while self.findID(ID)[4][day][0] == 0 and i < 20:
				# we do not want to use data with 0 in it, maybe we are forced to do so
				day = int(random.random() * (date - 8))
				i = i+1
			data = []
			return self.findID(ID)[4][day:day+8]
	
	def fillMissingData(self):
		# fills in data for stations without data
		ID = 2
		while ID != 1:
			if self.findID(ID)[4] == []:
				# no data file for gas station with id = ID
				station = self.nextID(ID)
				while self.findID(station)[4] == []:
					station = self.nextID(station)
				self.setID(ID, (self.findID(ID)[0], self.findID(ID)[1], self.findID(ID)[2], self.findID(ID)[3],  self.findID(station)[4][:]))
				self.count = self.count + 1
			
			ID = self.nextID(ID)
		
	
	def nextID(self, ID):
		return ID % len(self.prizingTable) +1
	
	def getDailyData(self, ID, date):
		# returns (max) the last year of data, one sample per day
		if self.findID(ID)[4] == []:
			print ("ERROR: no data found for gas station", ID)
		else:
			day = max([date-364, 0])
			data = []
			while day <= date:
				#print(day, date, len(self.findID(ID)[4]))
				data.append(self.findID(ID)[4][day][0])
				day = day +1
			return data
	
	def getCount(self):
		return self.count

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
			print("Error in appendAmount method")

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
	
	def __init__(self):	
		
		HALF_LIFE = 20
		
		# 100 sofms for each category one
		self.sofms = []
		i = 0
		while i < 100:
			self.sofms.append(algorithms.SOFM(
				n_inputs=24*8,			# 8 days of data
				features_grid=(10,10), 	# 100 categories

				#distance = euclid,
				shuffle_data = True,
				learning_radius=5,
				reduce_radius_after = int(NUMBER_OF_EPOCHS / 6),
				reduce_step_after = 20,
				reduce_std_after = 20,
				#weight = sample_from_data,	# start with random weights from data

				step=0.1,

				show_epoch = '10 times',
				verbose = False,
			))
			i = i + 1
		
		# find SOFM for ID
		self.lookupID = {0: -1}
		
		# find all IDs for SOFM
		self.lookupSOFMS = []
		for i in range(0, 100):
			self.lookupSOFMS.append([])
		
	
	def train(self, gasStations, date, datasize):
		""" 
		train the SOFM with the given data
		"""
		
		"""

		self.sofm.train(data_array, epochs = NUMBER_OF_EPOCHS)
		"""
		self.trainRough(gasStations, date)
		self.trainFine(gasStations, date, datasize)
		
		
	def trainRough(self, gasStations, date):	
		dimension = len(gasStations.getDailyData(1, date))
		self.rough = algorithms.SOFM(
			n_inputs = dimension,		# max 365 days of data
			features_grid=(10,10), 	# 100 categories
			
			shuffle_data = True,
			learning_radius = 5,
			reduce_radius_after = 2,
			reduce_step_after = 1,
			reduce_std_after = 3,
			step=0.5,
			
			show_epoch = '5 times',
			verbose = True,
		)
		
		data_array = np.zeros((gasStations.getCount(), dimension))
		ID = 1
		i = 0
		while i < gasStations.getCount():
			while gasStations.noData(ID):
				# find gas station with data
				ID = gasStations.nextID(ID)
			data = gasStations.getDailyData(ID, date)
			data_array[i] = data[:]
			i = i + 1
			ID = gasStations.nextID(ID)
		
		# sort gas stations roughly
		self.rough.train(data_array, epochs = 10)
		
		ID = 1
		i = 0
		
		# assign gas stations to category
		while i < gasStations.getCount():
			while gasStations.noData(ID):
				# find gas station with data
				ID = gasStations.nextID(ID)
			data = gasStations.getDailyData(ID, date)
			y = np.nonzero(self.rough.predict(data)[0] == 1)[0][0]
			self.lookupSOFMS[y].append(ID)
			lookup = {ID:y}
			self.lookupID.update(lookup)
			i = i + 1
			ID = gasStations.nextID(ID)
		
		#for i in range(0,100):
		#	print(len(self.lookupSOFMS[i]))
			
		
		
	
	def trainFine(self, gasStations, date, datasize):
		print("train SOMFS")
		for i in range (0, 100):
			if len(self.lookupSOFMS[i]) != 0:
				# only train SOFMS with associated gas stations
				self.trainSOFM(i, gasStations, date, datasize)
		
		
	def trainSOFM(self, sofmID, gasStations, date, datasize):
		print("train SOFM", sofmID, end="\r")
		data_array = np.zeros((datasize, 24*8))
		j = 0
		i = 0
		while i < datasize:
			ID = self.lookupSOFMS[sofmID][j]
			j = (j+1)%len(self.lookupSOFMS[sofmID])
			data = gasStations.randomData(ID, date)
			flattened_data = [y for x in data for y in x]
			data_array[i]= flattened_data[:]
			i = i+1
		
		self.sofms[sofmID].train(data_array, epochs = NUMBER_OF_EPOCHS)	
		
	def forecast(self, history,date):
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
		M = Model()
		M.train(self.gasStations, 400, 100)

		
		
	
	
#M = Model()
#M.train([])
S = Supervisor()
S.handleHandle()
