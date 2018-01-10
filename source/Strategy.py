#from Input.GasStation import GasStation
#from Input.Route import Route
import math as M

class Strategy:
	"""
	calculates the optimal fueling strategy for path with known prizes
	formerly known as tFontF
	"""
	def __init__(self):
		print("Calculating best route")
		self.capacity = 0
		self.route = []
		self.bestRoute = []
		self.gasStation = None

	def calculate(self, route, gasStation):
		"""
		- compute best strategy for fueling and return it
		"""

		self.capacity = route.capacity
		self.route = route.route
		self.gasStation = gasStation
		self.bestRoute = [0] * len(self.route)

		self.driveToNext(0, self.findNextBreakpoint(0), 0)

		route.appendAmount(self.bestRoute)

		print("Finished calculating.")


	def next(self, node):
		if node == len(self.route)-1:
			return node

		nodeList = {}
		currentNode = node+1
		while self.consumption(node,currentNode) <= self.capacity:
			nodeList[self.prize(currentNode)] = currentNode
			if currentNode == len(self.route)-1:
				break
			else:
				currentNode = currentNode +1

		if len(list(nodeList.keys())) > 0:
			return nodeList[min(list(nodeList.keys()))]
		else:
			print("Route not valid")
			return 999999

	def previous(self, node):
		nodeList = {}
		currentNode = node

		while self.consumption(currentNode, node) <= self.capacity:
			nodeList[self.prize(currentNode)] = currentNode

			if currentNode == 0:
				break
			else:
				currentNode = currentNode -1

		if min(list(nodeList.keys())) == self.prize(node):
			return node

		return nodeList[min(list(nodeList.keys()))]

	def prize(self, position):
		if position == len(self.route)-1:
			return 0
		return int(self.route[position][2])

	def findBreakPoints(self):
		returnList = []

		for node in range(1, len(self.route)):
			if self.previous(node) == node:
				returnList.append(node)

		return returnList

	def findNextBreakpoint(self, currentNode):
		"""
		finds next breakpoint, otherwise returns the node given by next()
		:param currentNode:
		:return:
		"""
		if currentNode == len(self.route)-1:
			return currentNode

		for node in self.findBreakPoints():
			if node > currentNode:
				return node

		return next(currentNode)

	def driveToNext(self, currentNode, targetNode, currentGas):
		xNode = currentNode

		if self.consumption(currentNode, targetNode) <= self.capacity:
			fillingValue = self.consumption(currentNode, targetNode) - currentGas
			self.bestRoute[currentNode] = fillingValue
			nextNode = self.findNextBreakpoint(targetNode)
			if nextNode == targetNode:
				return
			self.driveToNext(targetNode, self.findNextBreakpoint(targetNode), 0)
		else:
			fillingValue = self.capacity - currentGas
			self.bestRoute[currentNode] = fillingValue
			nextNode = self.next(currentNode)
			self.driveToNext(nextNode, targetNode, self.capacity)

	def consumption(self, currentNode, targetNode):
		def distance(station1, station2):
			def lat(stationNr):
				return self.gasStation.findID(stationNr)[2]/90.0 * M.pi

			def lon(stationNr):
				return self.gasStation.findID(stationNr)[3]/180.0 * M.pi

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
			consumptionPerKilometer = 5.6 /100.0
			consumptionToNext = 1.0 * dist * consumptionPerKilometer
			return consumptionToNext + self.consumption(currentNode+1, targetNode)
