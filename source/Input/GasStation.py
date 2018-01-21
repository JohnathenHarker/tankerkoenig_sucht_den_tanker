from .ParseDate import *

import os.path
import csv
import time
import random

class GasStation:
	"""
	represents set of gas stations with ID, position, prizes
	"""

	def __init__(self):
		
		self.last_day = 1178 # last day with data
		self.count = 0	# counts number of gasStations
		self.prizingTable = []
		t1 = time.clock()
		# read table of gas stations
		with open('../geg. Dateien/Eingabedaten/Tankstellen.csv', encoding='utf-8') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=';')
			id = 1
			for row in readCSV:
				print("read gas station", id, end="\r")
				if id != int(row[0]):
					print("ERROR: fehlerhafte Tankstellenliste")
				marke = row[2]
				nord = float(row[7])
				sued = float(row[8])

				self.prizingTable.append((id, marke, nord, sued, self.read(self.last_day, id)))
				id = id+1
	
		# gas stations without historic data get some random data
		self.fillMissingData()

		t2 = time.clock()
		dt = t2-t1
		print("")
		print ("reading gas stations completed in", dt, "seconds")

	def noData(self, ID):
		return self.findID(ID)[4] == []

	def findID(self, ID):
		#returns data for given ID
		if ID == self.prizingTable[ID-1][0]:
			return self.prizingTable[ID-1]
		else:
			return self.prizingTable[self.prizingTable.index(ID)]

	def setID(self, ID, data):
		# sets data for gas-station-id
		if ID == self.prizingTable[ID-1][0]:
			self.prizingTable[ID-1] = data[:]

	def read(self, endDay, ID):
		# read historic data for given gas station till given day
		data = []
		oneDay = []
		d = 0
		h = 0
		prize = 0
		path = '../geg. Dateien/Eingabedaten/Benzinpreise/'+str(ID)+'.csv'

		# check wether file exists
		if os.path.isfile(path):
			self.count = self.count +1
			with open(path, encoding= 'utf-8') as csvfile:
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
		# returns random data sample of 8 days of gas station with given id
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
				# gas stations gets data of next gas station with data
				self.setID(ID, (self.findID(ID)[0], self.findID(ID)[1], self.findID(ID)[2], self.findID(ID)[3],  self.findID(station)[4][:]))
				self.count = self.count + 1

			ID = self.nextID(ID)


	def nextID(self, ID):
		# returns the next id 
		return ID % len(self.prizingTable) +1

	def getDailyData(self, ID, date):
		# returns (max) the last year of data, one sample per day
		if self.findID(ID)[4] == []:
			print ("ERROR: no data found for gas station", ID)
		else:
			day = max([date-364, 0])
			data = []
			while day <= date:
				data.append(self.findID(ID)[4][day][0])
				day = day +1
			return data

	def getCount(self):
		# returns number of gas stations
		return self.count
