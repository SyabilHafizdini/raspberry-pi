

import json
import requests
import time
import sys
import os
import time

url = 'http://192.168.1.189:3000/data'
cwd = os.getcwd()

while True:
	#Checking if there is any files in 'data' folder
	listOfFiles = os.listdir(cwd)
	numberOfFiles = len(listOfFiles)
	if (numberOfFiles >= 1):
		for file_name in listOfFiles:
			if file_name.endswith('.txt'):
				time.sleep(5)
				startTime = time.time()
				with open(file_name) as json_file:
					data = json.load(json_file)
					count = 0
					for d in data['tempHumid']:
						isSent = True
						query = {
							"temperature": d['temperature'],
							"humidity": d['humidity'],
							"time": d['time'],
							"date": d['date']
						}
						try:
							res = requests.post(url, json=query)
							count = count + 1
							print("#{} Temp: {}C Humidity: {}% Time: {} Date: {}".format(count, d['temperature'], d['humidity'], d['time'], d['date']))
						except requests.exceptions.RequestException:
							print("Could not upload data")
							isSent = False
					if isSent:
						os.remove("/home/pi/FYP/POST_DATA/" + file_name)
						endTime =  time.time() - startTime
						print("{} cleared and {} data uploaded!".format(file_name, str(count)))
						print("It took {} seconds!".format(endTime))
					else:
						print("No connection. Could not upload {}".format(file_name))
