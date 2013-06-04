#!/usr/bin/env python

import json, ast
import requests
import jsondata as sql
import time
import serial
import homescan


run = True
mod_number = "1"
#server = 'http://10.249.41.39:8090'
server = 'http://localhost:8090'
headers = {
  'Accept': 'application/json'
  }

data = sql.json_struct()


port = serial.Serial("/dev/ttyAMA0", baudrate=9600)
buf = [0]*12
test = 0
input_type = 0
modules_created = []

def parse_rasp_input(size):
	global input_type
	global mod_number
	global data
	for i in range(size):
		print buf[i]
		if input_type == 0:
			if buf[i] == 'p':
				print 'p'
				port.write('p')
				port.write(mod_number)
				print mod_number
				modules_created.append(mod_number)
				mod_number = chr(ord(mod_number) + 1)
				input_type = 0
			elif 'u' == buf[i]:
				input_type = input_type + 1
			else:
				print "error: packet type"
				input_type = 0
		elif input_type == 1:
			if buf[i] in modules_created:
				data["iden"] = buf[i]
				input_type = input_type + 1
			else:
				print "error: module not created"
				input_type = 0
		elif input_type == 2:
			if 't' == buf[i]:
				data["alarm"] = "On"
				input_type = input_type + 1			
			elif 'f' == buf[i]:
				data["alarm"] = "Off"
				input_type = input_type + 1
			else:
				print "error: improper alarm data"
				input_type = 0
		elif input_type == 3:
			sensor_slot = process_slot(buf[i])
			if "error" != sensor_slot:
				data["slot_1"] = sensor_slot
				input_type = input_type + 1
			else:
				print "error: slot type"
				input_type = 0
		elif input_type == 4:
			sensor_slot = process_slot(buf[i])
			if "error" != sensor_slot:
				data["slot_2"] = sensor_slot
				input_type = input_type + 1
			else:
				print "error: slot type"
				input_type = 0		
		elif input_type == 5:
			sensor_slot = process_slot(buf[i])
			if "error" != sensor_slot:
				data["slot_3"] = sensor_slot
				input_type = input_type + 1
			else:
				print "error: slot type"
				input_type = 0		
		if input_type == 6:
			print "sending server request"
			data['user_home'] = user_check()
			server_request()
			send_pi_data()
			input_type = 0

def process_slot(input_char):
	sensor_name = ""
	if '7' == input_char:
		sensor_name = "None"
	elif '5' == input_char:
		sensor_name = "Ambient Sensor"
	elif '1' == input_char:
		sensor_name = "Accelerometer"
	elif '3' == input_char:
		sensor_name = "Motion Sensor"
	else:
		sensor_name = "error"
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
		elif data['armed'] == "Off":
			port.write('f')
			print 'f'
		else:
			print "error: armed data not recognized"

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
#	buf[1] = port.read(1)
#	buf[2] = port.read(1)
#	buf[3] = port.read(1)
#	buf[4] = port.read(1)
#	buf[5] = port.read(1)
	return 1


def server_request():
	global data
	response = requests.post('%s/endpoint' % server, data=json.dumps(data), headers=headers)
	response_str = response.text
	packet = json.loads(response_str)
	data = packet['data']
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
	buf[0] = 'p'
	parse_rasp_input(1)
	#buf[0] = 'u'
	#buf[1] = chr(ord(char) + 1)
	#char = chr(ord(char) + 1)
	#buf[2] = 't'
	#buf[3] = '7'
	#buf[4] = '7'
	#buf[5] = '7'
	#parse_rasp_input(6)
	buf[0] = 'u'
	buf[1] = '1'
	buf[2] = 't'
	buf[3] = '7'
	buf[4] = '7'
	buf[5] = '7'
	parse_rasp_input(6)

def user_check():
	for address in data['mac_address']:
		if homescan.search_network(address) == True:		
			return True
	return False
			
#buf[0] = 'p'
#parse_rasp_input(1)
while run == True:	
	try:
		time.sleep(2)
		#test_pi_coms()
		size = read_port()
		parse_rasp_input(size)
		#print data
		server_request()
		
	except KeyboardInterrupt:
		run = False
	#except:
		#input_type = 0
		#pass
		#print "what"
	#else:
		#print "Some Error Keep Running!!!"
		#pass
