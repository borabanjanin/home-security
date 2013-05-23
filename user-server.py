#!/usr/bin/env python

import SocketServer
import SimpleHTTPServer
from urlparse import urlparse, parse_qsl
from pprint import pprint
import cgi

import json
import os
import re
import subprocess
import jsondata as sql

PORT = 8080
#sql.create_table()
#sql.create_module("0", "false", "false", "none", "none", "none", "255", "255", "255")


class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def get_query_params_as_dict(self):
		kv_tuples = parse_qsl(urlparse(self.path)[4])
		result = {}    
		for k, v in kv_tuples:
			result[k] = v
		return result

	def do_GET(self):
		
		top = """
		<html>
				<head>
					<title>CSE 477</title>
					<link rel="stylesheet" type="text/css" href="index.css" />
				</head>
				<body>"""

		
		if self.path == '/favicon.ico':
			self.send_response(404)
			self.send_header("Content-type", "text/html")
			self.end_headers()
	
		elif self.path == '/configure':
			
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("""%s""" %top)
			self.wfile.write("""
						<img src="http://media.merchantcircle.com/29974860/icon-power-button%20OFF_full.gif" />
						<h1>SenseI Hub User Configuration</h1>
				<form method="POST">						
						<fieldset>
							<legend>System </legend>
							Arm Status
							<select name="armed">
									<option value="ARMED">ARM SYSTEM</option>
									<option value="NOT ARMED">DISARM SYSTEM</option>
							</select><br />
							Alarm Status 
							<select name="alarm">
									<option value="on">ON
							</select>
						</fieldset>
				
							<fieldset>
								</legend>Sensor Modules</legend>
								<input type="text" name="iden" /><br />
								<input type="text" name="config1" /><br />
								<input type="text" name="config2" /><br />
								<input type="text" name="config3" /><br />
								<input id="submit" type="submit" name="Go" />
							</fieldset>
						</form>
				</body>
		</html>
			""" )
		
		else:
			alarm_message = ""
			if sql.alarm_status() == 0:
				alarm_message = "OFF"
			else:
				alarm_message = "Tripped"
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("""%s""" %top)
			self.wfile.write("""
				<img src="http://media.merchantcircle.com/29974860/icon-power-button%20OFF_full.gif" />
				<h1>SenseI Portal</h1>
				
				<p>Welcome to the SenseI user interface portal</p>
				

			""")

			
			self.wfile.write("""

				<form method="POST">
					<input type="text" name="iden" />
					<input type="submit" name="Go" />
				</form>
				</body>

				<p><b>Status:</b>.</p>
		
				Alarm: %s
			</html>
			
			"""% alarm_message)
		self.wfile.close()


	def do_POST(self):
		#print self.path
		self.send_response(200)
		self.end_headers()

		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
			         'CONTENT_TYPE':self.headers['Content-Type'],
			         })
		if self.path == '/configure': 
			iden = form['iden'].value
			config1 = form['config1'].value
			config2 = form['config2'].value
	 		config3 = form['config3'].value
			print form['armed'].value
			sql.user_server_config(iden, config1, config2, config3)
	
		else:
			iden = form['iden'].value
			armed = form['armed'].value
			alarm = form['alarm'].value
			sql.user_server_update(iden, armed, alarm)
			
#		self.wfile.write(form['his_name'].value)
#		self.wfile.write(form['your_name'].value)
		self.wfile.close()


class MyHTTPServer(SocketServer.TCPServer):
	allow_reuse_address = True

if __name__ == "__main__":
	httpd = MyHTTPServer(('', PORT), MyHTTPHandler)
	print('serving at port %d' % PORT)
	try:
		httpd.serve_forever()
		print "running"
	except KeyboardInterrupt:
		print('bye')
		httpd.server_close()
'''

						<fieldset>
							<legend>System </legend>
							Arm Status
							<select name="armed">
									<option value="ARMED">ARM SYSTEM</option>
									<option value="NOT ARMED">DISARM SYSTEM</option>
							</select><br />
							Alarm Status 
							<select name="alarm">
									<option value="on">ON
							</select>
						</fieldset>


					<select name="armed">
							<option value="ARMED" selected="selected">ARM SYSTEM</option>
							<option value="NOT ARMED">DISARM SYSTEM</option>
					</select><br />
'''
