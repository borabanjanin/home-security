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
import serial

import sys
sys.path.append("/home/bora/Code/home-security")
import jsondata as sql

PORT = 8080
sql.create_table()
sql.create_module("0", "false", "false", "none", "none", "none")

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def get_query_params_as_dict(self):
		kv_tuples = parse_qsl(urlparse(self.path)[4])
		result = {}    
		for k, v in kv_tuples:
			result[k] = v
		return result

	def do_GET(self):
		if self.path == '/favicon.ico':
			self.send_response(404)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.close()
		else:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("""
				%s
				<form method="POST">
				<input type="text" name="iden" />
				<input type="text" name="armed" />
				<input type="text" name="alarm" />
				<input type="submit" name="Go" />
				</form>
			""" % self.path)
			self.wfile.close()


	def do_POST(self):
		self.send_response(200)
		self.end_headers()

		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
			         'CONTENT_TYPE':self.headers['Content-Type'],
			         })

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

