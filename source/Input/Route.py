from .ParseDate import *

class Route:
	"""
	stores a route with (predicted) prizes and fueling amounts
	"""


	def __init__(self):
		# inputs file instantly
		print("input route")
		#route is a tuple of capacity and the list of tuples of arrival time, id, prize and amount of a certain gas station
		self.capacity = 0
		self.route = []
		print("route", self.route)

	def read(self, file):
		"""
		- input file
		"""
		self.capacity = 0
		self.route = []
		routelist = []

		with open(file, encoding='utf-8') as routefile:
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
		"""
		- add prize to each gas station in a given route
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
		"""
		- add amount of fuel to each gas station in a given route
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
		"""
		- write data to file
		"""

		readlines = []
		with open(file, "r", encoding='utf-8') as f:
			first_line = True
			for line in file:
				if first_line:
					first_line = False
				else:
					readlines.append(line)

		with open(file + "mitTankstrategie", "w") as f:
			counter = 0
			for line in readlines:
				f.write(line + ";" + str(self.route[counter][2]) + ";" + str(self.route[counter][3]))
				counter += 1
