from .ParseDate import *

class PrizingForecast:
	"""
	handles files with prize requests
	"""

	def __init__(self, file):
		#contains a list of tuples consisting of endDate, forecastDate and the gas station id
		self.forecastParameter = []
		self.read(file)

	def read(self, file):
		"""
		- import data from file--> store in forecastParameters
		"""

		with open(file, "r", encoding='utf-8') as f:
			self.forecastParameter = []
			for line in f:
				#(endDate, forecastDate, id, prize)
				lineValues = tuple(line.split(";"))
				self.forecastParameter.append((parseDate(lineValues[0]), parseDate(lineValues[1]), int(lineValues[2]), 0))

	def appendPrize(self, listOfPrizes):
		"""
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
		"""
		write data to file
		"""

		readLines = []
		with open(file, "r", encoding='utf-8') as f:
			for line in file:
				readLines.append(line)

		with open(file, "w") as f:
			counter = 0
			for line in readLines:
				f.write(line + ";" + str(self.forecastParameter[counter][3]))
				counter += 1