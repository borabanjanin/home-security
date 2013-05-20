#!/usr/bin/env python

import json
import requests
import jsondata as sql
import time
import serial


run = True
mod_number = 0
server = 'http://localhost:8090'
headers = {
  'Accept': 'application/json'
  }

data = sql.json_struct()


#port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
buf = [0]*10
test = 0
input_type = 0


def parse_rasp_input(size):
	global input_type
	global mod_number
	global data
	for i in range(size):
		print i 
		print buf[i]
		if input_type == 0:
			if buf[i] == 'p':
				port.write('p')
				port.write(mod_number)
				mod_number = mod_number + 1
				input_type = 0
			elif 'c' == buf[i]:
				input_type = input_type + 1
		elif input_type == 1:
			data["iden"] = buf[i]
			input_type = input_type + 1
		elif input_type == 2:
			if 't' == buf[i]:
				data["alarm"] = "True"
			else:
				data["alarm"] = "False"
			input_type = input_type + 1
		elif input_type == 3:
			if 'n' == buf[i]:
				data["slot_1"] = "None"
			else:
				data["slot_1"] = "SensorName"
			input_type = input_type + 1
		elif input_type == 4:
			if 'n' == buf[i]:
				data["slot_2"] = "None"
			else:
				data["slot_2"] = "SensorName"
			input_type = input_type + 1
		elif input_type == 5:
			if 'n' == buf[i]:
				data["slot_3"] = "None"
			else:
				data["slot_3"] = "SensorName"
			input_type = input_type + 1
		if input_type == 6:
			server_request()
			send_pi_data()
			input_type = 0
			
#def store_input():

def send_pi_data():
		global data		
		port.write('iden')
		if data['armed'] = "True"
			port.write('T')
		else:
			port.write('F')
		port.write('c')
		port.write('d')
		port.write('e')

def read_port():
	size = port.readinto(buf)
	print size
	for i in range(size):
		print buf[i]
	return size


def server_request():
	response = requests.post('%s/endpoint' % server, data=json.dumps(data), headers=headers)
	response_str = response.text
	if response.status_code == requests.codes.OK:
	  print('Response: HTTP %s' % response.status_code)
	  print(json.dumps(json.loads(response_str), indent=2))
	else:
	  print('Error: HTTP %s' % response.status_code)
	  print(response_str)
	

def print_data():
	print data['iden']
	print	data['armed']
	print	data['alarm']
	print	data['sensor_1']
	print	data['sensor_2']
	print	data['sensor_3']
	print	data['sensor_4']
	print	data['sensor_5']
	print	data['sensor_6']
	print	data['sensor_7']
	print	data['sensor_8']
	print	data['slot_1']
	print	data['slot_2']
	print	data['slot_3']

def test_pi_coms():
	global buf
	buf[0] = 'c'
	buf[1] = '25'
	buf[2] = 't'
	buf[3] = 'n'
	buf[4] = 'n'
	buf[5] = 'n'
	parse_rasp_input(6)
	#print_data()

test_pi_coms()
while run == True:	
	try:
		time.sleep(2)
		#size = read_port()
		#parse_input(size)
	except KeyboardInterrupt:
		run = False
