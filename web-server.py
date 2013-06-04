#!/usr/bin/env python

import SocketServer
import SimpleHTTPServer
from urlparse import urlparse, parse_qsl

import json
import os
import re
import subprocess
import jsondata as sql
PORT = 8090
from twilio.rest import TwilioRestClient

ACCOUNT_SID = "AC10980dc422a3e9684ae913c90f009188"
AUTH_TOKEN = "ee7a9b27a18a681741fccde6f93d7d0a"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
sql.create_table()
sql.create_user_table()
sql.create_user_home()
alarm_message_sent = False	

def send_text():
	print "User Alerted"
	numbers = sql.fetch_numbers()
	for num in numbers:		
		print "%s" % (num[1])
		message = client.sms.messages.create(to=num[1],from_="+14253362335",body="Your house alarm has been tripped!!")

class MyWebHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def get_query_params_as_dict(self):
		kv_tuples = parse_qsl(urlparse(self.path)[4])
		result = {}    
		for k, v in kv_tuples:
			result[k] = v
		return result

	def do_POST(self):
		global alarm_message_sent
		global created
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		content_len = int(self.headers.getheader('Content-Length'))
		post_data_str = self.rfile.read(content_len)
		post_data = json.loads(post_data_str)
		

		iden = post_data['iden']
		alarm = post_data['alarm']


		slot1 = post_data['slot_1']
		slot2 = post_data['slot_2']
		slot3 = post_data['slot_3']
		if post_data['user_home'] == False:
			sql.update_user_home('False')
		elif post_data['user_home'] == True:
			sql.update_user_home('True')
		else:
			print "error in inserting"

		#needs to be altered to allow for scaling
		if sql.check_iden(post_data['iden']) == 0:
			print "created" + post_data['iden']
			sql.create_module(iden, "Off", alarm, "None", "None", "None", "None", "None", "None", "None", "None", slot1, slot2, slot3)
		else:
			
			if sql.alarm_status() == 0:
				alarm = post_data['alarm']	
			else:
				row = sql.alarm_status_module(iden);
				alarm = row[1]

			sql.update_module_pi(iden, alarm, slot1, slot2, slot3)
			info = sql.pull_iden(iden)
			numbers = sql.fetch_numbers()
			list_num = []
			for num in numbers:
				list_num.append(num[2])
				if num[2] not in post_data['mac_address'] and num[2] != 'default':
					post_data['mac_address'].append(num[2])
			for address in post_data['mac_address']:
				if address not in list_num:
					post_data['mac_address'].remove(address)

			

			#print info
			post_data["armed"] = info[1]
			post_data["sensor_1"] = info[3]
			post_data["sensor_2"] = info[4]
			post_data["sensor_3"] = info[5]
			post_data["sensor_4"] =	info[6]
			post_data["sensor_5"] =	info[7]
			post_data["sensor_6"] =	info[8]
			post_data["sensor_7"] =	info[9]
			post_data["sensor_8"] =	info[10]

		
		if sql.alarm_status() == 0:
			sql.user_message_status("False")
	
		if alarm == "On" and post_data["armed"] == "On" and sql.user_message() == 0:
			user_tracker = sql.user_home_status()
			if user_tracker[0] == "False" and user_tracker[1] == "True":
				send_text()
				sql.user_message_status("True")
		


		content = {
			'path': self.path,
			'data': post_data
		}
  		
		#print(content)
		self.wfile.write(json.dumps(content))
		self.wfile.close()

class MyWebServer(SocketServer.TCPServer):
	allow_reuse_address = True
	
httpd = MyWebServer(('10.249.41.39', PORT), MyWebHandler)
print('serving at port %d' % PORT)

try:
	#send_text()
	httpd.serve_forever()
except KeyboardInterrupt:
	print('bye')
	httpd.server_close()



