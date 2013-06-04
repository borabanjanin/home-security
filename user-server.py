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

PORT = 80
#sql.create_table()
#sql.create_module("0", "false", "false", "none", "none", "none", "255", "255", "255")
sql.create_user_table()
sql.create_user_home()
phone_iden = "1"

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def get_query_params_as_dict(self):
		kv_tuples = parse_qsl(urlparse(self.path)[4])
		result = {}    
		for k, v in kv_tuples:
			result[k] = v
		return result

	def do_GET(self):
		
		top = """
		<!DOCTYPE html>
		<html>
			<head>
				<title>CSE 477</title>	
			</head>
			
			<style type="text/css">
				h1 {
					text-align: center;
					font-family: serif;
					color: gold;
				}
				
				img {
					display: block;
					margin-left: auto;
					margin-right: auto;
					width: 200px;
				}
				
				fieldset {
					border: solid;
					border-radius: 20px;
					border-color: gold;
					padding: 20px;
					display: inline;
					margin: 20px;
					margin-right: auto;
					margin-left: auto;
					margin: 20px;
				}
				

				span {
					background="green";
				}

				p {
					padding: 0px;
					margin: 0px;
				}
				
				html, body {

				}
				
				a {
					color:gold;
				}

				body {
					background-color: indigo;
					background-image: linear-gradient(bottom, rgb(158,58,252) 20%, rgb(80,8,138) 60%);
					background-image: -o-linear-gradient(bottom, rgb(158,58,252) 20%, rgb(80,8,138) 60%);
					background-image: -moz-linear-gradient(bottom, rgb(158,58,252) 20%, rgb(80,8,138) 60%);
					background-image: -webkit-linear-gradient(bottom, rgb(158,58,252) 20%, rgb(80,8,138) 60%);
					background-image: -ms-linear-gradient(bottom, rgb(158,58,252) 20%, rgb(80,8,138) 60%);
					
					background-image: -webkit-gradient(
						linear,
						left bottom,
						left top,
						color-stop(0.2, rgb(158,58,252)),
						color-stop(0.6, rgb(80,8,138))
					);
					
					background-repeat:no-repeat;
					color: white;
					padding:75px;
					text-align: center;
				}
				
				legend {
					font-size: 20;
					font-weight: bold;
					font-family: sans-serif;
				}
				
				form{
					overflow: hidden;
					padding 39px;
				}
			</style>
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
			self.wfile.write("""<br><img src="http://crosscut.com/media/resized_image/story_image/Story%2BImage_uw_huskies_logo_fit_300x300.jpg"/></br>""")
			self.wfile.write("""
						<h1>SenseI Hub User Configuration</h1>				
			""" )
			rows = sql.fetch_idens()
			if not rows:
				print "hit"
				self.wfile.write("""<br><b>No Modules Detected To Configure</b></br>""")
				self.wfile.write("""<br><b</b></br>""")
			self.wfile.write("""<br><form method="POST"></br>""")	
			self.wfile.write("""<fieldset>""")
			self.wfile.write("""		<legend>System </legend>""")
			for row in rows:
				
				self.wfile.write("""		<select name="iden">""")
				self.wfile.write("""			<option value="%s"> Module %s</option>"""%(row[0],row[0]))
				self.wfile.write("""		</select><br />""")	
				self.wfile.write("""			<select name="armed">
						<option value="On">Arm Module</option>
						<option value="Off">Disarm Module</option>
						</select><br />
			""")
			if rows:
				self.wfile.write("""	Accelerometer:	<select name="config_1">""")
				self.wfile.write("""			<option value="Default"> Default</option>""")
				self.wfile.write("""			<option value="Less"> Less Sensitive</option>""")
				self.wfile.write("""		</select><br />""")

				self.wfile.write("""	Motion Sensor:	<select name="config_2">""")
				self.wfile.write("""			<option value="Default"> Default</option>""")
				self.wfile.write("""			<option value="Less"> Less Sensitive</option>""")
				self.wfile.write("""		</select><br />""")

				self.wfile.write("""	Ambient Sensor:	<select name="config_5">""")
				self.wfile.write("""			<option value="Default"> Default</option>""")
				self.wfile.write("""			<option value="Less"> Less Sensitive</option>""")
				self.wfile.write("""		</select><br />""")

				self.wfile.write("""<input type="submit" name="Go" onclick="redirect()"/>""")
			else: 
				self.wfile.write("""<b>-_-</b>""")

			self.wfile.write("""</fieldset><br />""")
	
			self.wfile.write("""
					</form>
					</body>
					<a href="http://senseihome.com" > Home </a> <br />
					<a href="http://senseihome.com/telephone" > Configure Users </a>
				
			</html>
				""" )
		elif self.path == '/telephone':		
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("""%s""" %top)
			self.wfile.write("""<br><img src="http://crosscut.com/media/resized_image/story_image/Story%2BImage_uw_huskies_logo_fit_300x300.jpg" /></br>""")
			self.wfile.write("""<br><form method="POST"></br>""")	
			self.wfile.write("""<br>	Phone Number: <input type="text" name="phone"value="default"/></br>""")
			self.wfile.write("""<br>Example Phone number: 4251234567</br>""")
			self.wfile.write("""<br>	MAC Address: <input type="text" name="mac" value="default"/></br>""")
			self.wfile.write("""<br>Example MAC Address: 78:2b:cb:90:b6:94 </br>""")
			self.wfile.write("""<br><input type="submit" name="Go" /></br>""")
			response = "<br>Numbers Already entered: </br>"
			numbers = sql.fetch_numbers()
			visual_number = 0
			for num in numbers:
				visual_number = visual_number + 1
				response += "<fieldset>"
				response += "<br></t>	Click to remove "
				response	+=	""" <input type="checkbox" name="%s" id="checkbox_id" value="value" />""" % (num[0])
									#<label for="%s">what</label>""" % (num[0])
				response += "<legend>Phone #%s </legend>" % visual_number
				response += "</t><fieldset>	Phone Number: %s  </fieldset>" % (num[1])
				response += "</t><fieldset>	Mac Address: %s </fieldset>" %	(num[2])
				response += "</fieldset>"
			self.wfile.write("""%s""" % response)
			self.wfile.write("""<br></form></br>""")
			self.wfile.write("""<br></body></br>""")
			self.wfile.write("""<a href="http://senseihome.com" > Home </a><br />""")
			self.wfile.write("""<a href="http://senseihome.com/configure" > Configure your Modules </a>""")
			self.wfile.write("""<br></html></br>""")

		else:
			alarm_message = ""
			user_tracker = sql.user_home_status()
			print sql.arm_system_status()
			if sql.alarm_status() == 0 or sql.arm_system_status() == None:
				alarm_message = "OFF"
			else:
				if user_tracker[1] == 'True' and user_tracker[0] == 'True':
					alarm_message = "OFF"
				else:
					alarm_message = "Tripped"

				

			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("""%s""" %top)
			self.wfile.write("""
				<img src="http://1.bp.blogspot.com/-F-JOiQ-3bTs/TaHRUqf7jkI/AAAAAAAAEVU/uyZrwEXTzM4/s400/UW_W-Logo_RGB.png" />
				<h1>SenseI Portal</h1>
			
				<h2>Welcome to the SenseI user interface portal</h2><br />
			""")
		
			
			user_message = ""
			if user_tracker[0] == "True" and user_tracker[1] == "True":
				user_message = "Phone: Detected"
				sql.alarm_system("Off")
				sql.user_message_status("False")	
			elif user_tracker[0] == "False" and user_tracker[1] == "True":
				user_message = "Phone: Not Detected"
			elif user_tracker[1] == "False":
				user_message = "Auto Track Disabled"
			else:
				print "error determining status of user"
			self.wfile.write("""
				<fieldset><legend>Status:</legend>
				<p> Alarm: %s <br />
					%s	
			</p></fieldset>
	
			"""% (alarm_message, user_message))

			rows = sql.arm_status()
			module_number_iterator = 0
			if not rows:
				self.wfile.write("""<br><fieldset>No Modules Detected</fieldset></br>""")
			for row in rows:
				message = ""
				if row[1] == "Off":
					message = "Disarmed"
				else: 
					message = "Armed"
				self.wfile.write("""
				<p> <fieldset><legend>Module #%s</legend> Status: %s <br />
					<span class="sensors">Sensor 1: %s <br /> </span>  <span class="sensors">Sensor 2:	%s <br /> </span><span class="sensors">Sensor 3: %s</span>  	</fieldset></p>
				"""%(row[0],message,row[2],row[3],row[4]))
			self.wfile.write("""			
					<form method="POST" action="/">
						<select name="armed">
						<option value="True">ARM SYSTEM</option>
						<option value="False">DISARM SYSTEM</option>
						</select><br />	
						<select name="user">
						<option value="True">ENABLE AUTO TRACK</option>
						<option value="False">DISABLE AUTO TRACK</option>
						</select><br />	
						<input type="submit" name="Go" />
					</form>
					<a href="http://senseihome.com/telephone" > Configure Users </a><br />
					<a href="http://senseihome.com/configure" > Configure your Modules </a>
					</body>
						</html>
			""")

		self.wfile.close()

	def do_POST(self):
		global phone_iden
		#print self.path
		#self.send_response(200)
		#self.end_headers()
		self.send_response(200)
		self.send_header('','localhost:8080')
		self.end_headers()
		

		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
			         'CONTENT_TYPE':self.headers['Content-Type'],
			         })
		if self.path == '/configure': 
			iden = form['iden'].value
			arm = form['armed'].value
			sql.arm_module(iden,arm) 
			configure1 = form["config_1"].value
			configure3 = form["config_2"].value
			configure5 = form["config_5"].value
			sql.insert_config(iden,configure1,configure3,configure5)
			self.wfile.write("""<html><head>""")	
			self.wfile.write("""<meta http-equiv="REFRESH" content="0;url=http://senseihome.com/configure"></head></html>""")	
		elif self.path == '/telephone':
			phone = form['phone'].value
			mac = form['mac'].value
		#	for i in range(1,ord(phone_iden)):
		#		print form[i].value
			if re.match(r"\d{10}\b",phone) is None:
				print "error: Invalid Number"
			else:
				sql.add_number(phone_iden,phone,mac)	
				phone_iden = chr(ord(phone_iden) + 1)
			numbers = sql.fetch_numbers()
			for num in numbers:
				if num[0] in form:
					sql.delete_number(num[0])
			self.wfile.write("""<html><head>""")	
			self.wfile.write("""<meta http-equiv="REFRESH" content="0;url=http://senseihome.com/telephone"></head></html>""")	
		else:
			sql.arm_system(form['armed'].value)
			if form['user'].value == "False":
				sql.user_tracker("False")
			elif form['user'].value == "True":
				sql.user_tracker("True")
			else:
				print "not putting in values"
			if 0 != sql.alarm_status():
				if form['armed'].value == "True":
					sql.alarm_system("On")
					sql.user_message_status("False")
				elif form['armed'].value == "False":
					sql.alarm_system("Off")
					sql.user_message_status("False")				
				else:
					print "error parsing post arm status"
			self.wfile.write("""<html><head>""")	
			self.wfile.write("""<meta http-equiv="REFRESH" content="0;url=http://senseihome.com"></head></html>""")	
			
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


			self.wfile.write("""
					<select name="%s">
							<option value="ARMED">ARM MODULE %s </option>
							<option value="NOT ARMED">DISARM MODULE %s </option>
							</select><br />
			"""% (row[0], row[0], row[0]))
'''
