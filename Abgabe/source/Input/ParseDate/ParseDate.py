import math as M

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
	
	while (hour<0):
		hour = hour + 24
		normalized_day = normalized_day -1
		
	while (hour > 23):
		hour = hour - 24
		normalized_day = normalized_day +1

	# last three values probably not needed
	return (normalized_day, hour)#, year, month, day)