#!/usr/bin/env python

import json
import requests
import jsondata as sql
import time
import serial


run = True
mod_number = 0
server = 'http://192.168.1.3:8090'
headers = {
  'Accept': 'application/json'
  }

data = sql.json_struct()


port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
buf = [0]*10
input_type


def parse_input(size):
	for i in range(size):
		if input_type == 0:
			if buf[i] == 'p':
				port.write('p')
				port.write(mod_number)
				mod_number = mod_number + 1
				input_type = 0
			elif buf[i] == 'c':
				input_type = input_type + 1
		elif input_type == 1:
		elif input_type == 2:
			


def read_port():
	size = port.readinto(buf)
	print size
	for i in range(size):
		print buf[i]
	return size


def server_request():
	response = requests.post('%s/endpoint' % server, data=json.dumps(data), headers=headers)
	response_str = response.text
	'''
	if response.status_code == requests.codes.OK:
		 print('Response: HTTP %s' % response.status_code)
		 print(json.dumps(json.loads(response_str), indent=2))
	else:
		print('Error: HTTP %s' % response.status_code)
  		print(response_str)
	'''
	


while run == True:	
	try:
		#time.sleep(2)
		server_request()
		size = read_port()
		parse_input(size)
	except KeyboardInterrupt:
		run = False
