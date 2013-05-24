#!/usr/bin/env python

import json, ast
import requests
import jsondata as sql
import time
import serial


run = True
mod_number = 1
server = 'http://192.168.1.3:8090'
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
		if input_type == 0:
			if buf[i] == 'p':
				port.write('p')
				port.write(mod_number)
				mod_number = mod_number + 1
				input_type = 0
			elif 'u' == buf[i]:
				input_type = input_type + 1
		elif input_type == 1:
			data["iden"] = buf[i]
			input_type = input_type + 1
		elif input_type == 2:
			if 't' == buf[i]:
				data["alarm"] = "On"
			else:
				data["alarm"] = "Off"
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
			#send_pi_data()
			input_type = 0

def send_pi_data():
		global data
		port.write("c")		
		port.write(data['iden'])
		if data['armed'] == "On":
			port.write('t')
		else:
			port.write('f')

		if data['sensor_1'] == "None":
			port.write('n')
		else:
			port.write('s')
		if data['sensor_2'] == "None":
			port.write('n')
		else:
			port.write('s')
		if data['sensor_3'] == "None":
			port.write('n')

		else:
			port.write('s')
		if data['sensor_4'] == "None":
			port.write('n')
		else:
			port.write('s')
		if data['sensor_5'] == "None":
			port.write('n')
		else:
			port.write('s')
		if data['sensor_6'] == "None":
			port.write('n')
		else:
			port.write('s')
		if data['sensor_7'] == "None":
			port.write('n')
		else:
			port.write('s')
		if data['sensor_8'] == "None":
			port.write('n')
		else:
			port.write('s')


def read_port():
	size = port.readinto(buf)
	return size


def server_request():
	global data
	response = requests.post('%s/endpoint' % server, data=json.dumps(data), headers=headers)
	response_str = response.text
	packet = json.loads(response_str)
	#data = packet['data']
	#print data
	if response.status_code == requests.codes.OK:
		print('Response: HTTP %s' % response.status_code)
		#print(json.dumps(json.loads(response_str), indent=2))
		#print response["armed"]
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

char = '0'
def test_pi_coms():
	global buf
	global char
	buf[0] = 'u'
	buf[1] = chr(ord(char) + 1)
	char = chr(ord(char) + 1)
	buf[2] = 'f'
	buf[3] = 'n'
	buf[4] = 'n'
	buf[5] = 'n'
	parse_rasp_input(6)
	buf[0] = 'u'
	buf[1] = '1'
	buf[2] = 'f'
	buf[3] = 'n'
	buf[4] = 'n'
	buf[5] = 'n'
	parse_rasp_input(6)


while run == True:	
	try:
		print data
		test_pi_coms()
		time.sleep(2)
		#size = read_port()
		#parse_input(size)
	except KeyboardInterrupt:
		run = False
