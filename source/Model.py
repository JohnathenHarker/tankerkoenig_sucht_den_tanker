from multiprocessing import Process
import threading as td
import math as M
import numpy as np
import matplotlib.pyplot as plt
from neupy import algorithms, environment, init
import time
import random

NUMBER_OF_EPOCHS = 100
NUMBER_OF_CORES = 8
random.seed(42)

class Model:
	"""
	makes predictions for the prize of gas
	"""

	def __init__(self):

		HALF_LIFE = 20

		# 16 sofms for each category one
		self.sofms = []


		# find SOFM for ID
		self.lookupID = {0: -1}

		# find all IDs for SOFM
		self.lookupSOFMS = []
		for i in range(0, 16):
			self.lookupSOFMS.append([])


	def train(self, gasStations, date, datasize):
		"""
		train the SOFM with the given data
		"""

		self.trainingDate = date
		self.trainRough(gasStations, date)
		
		i = 0
		
		while i < 16:
			self.sofms.append(algorithms.SOFM(
				n_inputs=24*8,			# 8 days of data
				features_grid=(10,10), 	# 100 categories

				#distance = euclid,
				shuffle_data = True,
				learning_radius=3,
				reduce_radius_after = int(NUMBER_OF_EPOCHS / 6),
				reduce_step_after = 10,
				reduce_std_after = 20,

				#weight = 'sample_from_data',	# start with random weights from data
				weight = init.Normal(mean = 0, std = 10),

				step=0.8,

				show_epoch = '10 times',
				verbose = False,
			))
			i = i + 1
			
		self.trainFineParallel(gasStations, date, datasize)


	def trainRough(self, gasStations, date):
		print("train rough")
		dimension = len(gasStations.getDailyData(1, date))
		self.rough = algorithms.SOFM(
			n_inputs = dimension,		# max 365 days of data
			features_grid=(4,4), 		# 100 categories

			shuffle_data = True,
			learning_radius = 5,
			reduce_radius_after = 2,
			reduce_step_after = 2,
			reduce_std_after = 3,
			step=0.5,
			weight = 'sample_from_data',	# start with random weights from data

			show_epoch = '5 times',
			verbose = False,
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
		self.rough.init_weights(data_array)
		self.rough.train(data_array, epochs = 20)

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
		for i in range (0, 16):
			if len(self.lookupSOFMS[i]) != 0:
				# only train SOFMS with associated gas stations
				self.trainSOFM(i, gasStations, date, datasize)


	def trainFineParallel(self, gasStations, date, datasize):
		print ("train SOFMS parallel")
		t1 = time.time()

		i = 0
		P = []
		while i < 16:
			P = []
			a = 0
			while a < NUMBER_OF_CORES and i < 16:
				if len(self.lookupSOFMS[i]) != 0:
					P.append(Process(target=self.trainSOFM, args=(i, gasStations, date, datasize,)))
					a = a + 1
				i = i+1
			for j in range (0,len(P)):
				P[j].start()
			for j in range (0,len(P)):
				P[j].join()

		t2 = time.time()	
	
		dt = t2-t1
		print("finished in", dt, "seconds")


	def trainSOFM(self, sofmID, gasStations, date, datasize):
		if len(self.lookupSOFMS[sofmID]) != 0:
			
			# create random start values
			init_weights = np.zeros((100, 24*8))
			j = 0
			i = 0
			while i < 100:
				ID = self.lookupSOFMS[sofmID][j]
				j = (j+1)%len(self.lookupSOFMS[sofmID])
				data = gasStations.randomData(ID, date)
				flattened_data = [y - data[6][23] for x in data for y in x]
				init_weights[i]= flattened_data[:]
				i = i+1
			
			init_weight = np.transpose(init_weights)[:]
			
			self.sofms[sofmID] = algorithms.SOFM(
				n_inputs=24*8,			# 8 days of data
				features_grid=(10,10), 	# 100 categories

				#distance = euclid,
				shuffle_data = True,
				learning_radius=4,
				reduce_radius_after = int(NUMBER_OF_EPOCHS / 4),
				reduce_step_after = 10,
				reduce_std_after = 10,

				#weight = 'sample_from_data',	# start with random weights from data
				weight = init_weight,

				step=0.8,

				show_epoch = '10 times',
				verbose = False,
			)
			
			data_array = np.zeros((datasize, 24*8))
			j = 0
			i = 0
			while i < datasize:
				ID = self.lookupSOFMS[sofmID][j]
				j = (j+1)%len(self.lookupSOFMS[sofmID])
				data = gasStations.randomData(ID, date)
				flattened_data = [y - data[6][23] for x in data for y in x]
				data_array[i]= flattened_data[:]
				i = i+1

			self.sofms[sofmID].train(data_array, epochs = NUMBER_OF_EPOCHS)
			
		#if sofmID == 5 :
		#	print("map4:", self.sofms[sofmID].weight[:192, 4])
		#	print("map80:", self.sofms[sofmID].weight[:192, 80])
			
		return

	def forecast(self, ID, date, hour, gasStations):
		""" TO DO:
		predict prize
		"""
		sofmID = self.lookupID[ID]
		history = gasStations.findID(ID)[4][self.trainingDate-6 : self.trainingDate+1]
		history = [y for x in history for y in x]
		history = np.asarray(history)
		weights = self.sofms[sofmID].weight

		d = date-self.trainingDate
		if (d > 0):
			for i in range(0, d):
				prediction = self.simpleForecast(weights, history)
				history = np.append(history[24:], prediction)
			return prediction[hour]
		else:
			#print("NOTE: requestet prize is not in the future")
			return gasStations.findID(ID)[4][date][hour]


	def simpleForecast(self, weights, history):
		# returns one day of forecasting
		a = history
		start = a[167]
		a = a-start
		dist = np.linalg.norm(a - weights[:168, 0])
		#print("dist:", dist, 0)
		best_matching = 0
		for i in range(0, weights.shape[1]):
			# visit all columns
			d = np.linalg.norm(a - weights[:168, i])
			#print("d:", d, dist, i)
			if d < dist:
				dist = d
				best_matching = i
		#return day plus first value
		#print("best:",best_matching)
		#print (weights[:, best_matching])
		return weights[168:193,best_matching] + start

	
	def evaluate(self, gasStations):
		data = np.zeros((30,2))
		begin = self.trainingDate
		rounds = 200
		for day in range(0,30):
			d1 = []
			d2 = []
			for i in range(0, rounds):
				station = int(random.random()* (gasStations.count-1))+1
				hour = int(random.random() * 23)
				if not gasStations.noData(station):
					a = self.forecast(station, begin+day, hour, gasStations) 	# prediction
					b = gasStations.findID(station)[4][begin+day][hour]		# real value
					c = gasStations.findID(station)[4][begin][0]			# start value of month

					dif1 = abs(b-a)
					dif2 = abs(c-b)
					d1.append(dif1)
					d2.append(dif2)
			dif1 = np.median(np.asarray(d1))
			dif2 = np.median(np.asarray(d2))
			data[day][0] = dif1
			data[day][1] = dif2
			
		plt.plot(data[:, 0:1])
		plt.ylabel('Durchschnittliche Abweichung der Vorhersage vom richtigen Wert (0,1 ct)')
		plt.xlabel('Tage hinter bekanntem Preis')
		plt.show()
		
		plt.plot(data[:, 1:2])
		plt.ylabel('Durchschnittliche Abweichung vom letzten bekannten Wert (0,1 ct)')
		plt.xlabel('Tage hinter bekanntem Preis')
		plt.show()
		np.savetxt('evaluation.csv', data, delimiter=';')
		print("model evaluated")
