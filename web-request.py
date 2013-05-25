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


port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
buf = [0]*12
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
			data["slot_1"] = process_slot(buf[i])
			input_type = input_type + 1
		elif input_type == 4:
			data["slot_2"] = process_slot(buf[i])
			input_type = input_type + 1
		elif input_type == 5:
			data["slot_3"] = process_slot(buf[i])
			input_type = input_type + 1
		if input_type == 6:
			print "sending server request"
			server_request()
			send_pi_data()
			input_type = 0

def process_slot(input_char):
	sensor_name = ""
	if '7' == input_char:
		sensor_name = "None"
	elif '3' == input_char:
		sensor_name = "TestSensor"
	else:
		sensor_name = "SensorName"
	return sensor_name

def send_pi_data():
		global data
		port.write("c")		
		print 'c'
		port.write(data['iden'])
		print data['iden']
		if data['armed'] == "On":
			port.write('t')
			print 't'
		else:
			port.write('f')
			print 'f'

		if data['sensor_1'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_2'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_3'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_4'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_5'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_6'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_7'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'
		if data['sensor_8'] == "None":
			port.write('n')
			print 'n'
		else:
			port.write('s')
			print 's'

def read_port():
	buf[0] = port.read(1)
	return 1


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
	#parse_rasp_input(6)
	buf[6] = 'u'
	buf[7] = '1'
	buf[8] = 'f'
	buf[9] = 'n'
	buf[10] = 'n'
	buf[11] = 'n'
	parse_rasp_input(12)


while run == True:	
	try:
		#print data
		#test_pi_coms()
		#time.sleep(2)
		size = read_port()
		parse_rasp_input(size)
	except KeyboardInterrupt:
		run = False
