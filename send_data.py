#!/usr/bin/python
import sys
import Adafruit_DHT
import requests
import time
import datetime
import json
import random

url = 'http://192.168.1.189:3000/data'
#url = 'http://192.168.1.40:3000/data'
#url = 'http://192.168.1.35:3000/data'
datas = {}
datas['tempHumid'] = []
while True:
    time.sleep(.5)
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    now = datetime.datetime.now()
    curtime = now.strftime("%X")
    curdate = now.strftime("%d/%m/%y")

    query = {
        "temperature" : temperature,
        "humidity": humidity,
        "time": curtime,
	"date": curdate
    }

    output = 'Temp: {0:0.1f}C  Humidity: {1:0.1f}% Time: {2} Date: {3}'.format(temperature, humidity, curtime, curdate)
    try:
	res = requests.post(url, json=query)
	if len(datas['tempHumid']) > 0:
		fileName = "data" + str(len(datas['tempHumid'])) + "_" + str(random.randint(1,100)) + ".txt"
		with open(fileName, "w+") as outfile:
			print("Connection established: Saving " +  str(len(datas['tempHumid'])) + " data to file.")
			print("Data saved in " + fileName)
			json.dump(datas, outfile)
			datas.clear()
			datas['tempHumid'] = []
	else :
	        print(output)
	        print(res.text)
    except requests.exceptions.RequestException:
        datas['tempHumid'].append(query)
	print(output)
	print("Connection error: Data saved in dictionary.")
