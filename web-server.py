#!/usr/bin/env python

import SocketServer
import SimpleHTTPServer
from urlparse import urlparse, parse_qsl
from pprint import pprint

import json
import os
import re
import subprocess
import serial

PORT = 8080

class MyWebHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def get_query_params_as_dict(self):
		kv_tuples = parse_qsl(urlparse(self.path)[4])
		result = {}    
		for k, v in kv_tuples:
			result[k] = v
		return result


	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()

		content_len = int(self.headers.getheader('Content-Length'))
		post_data_str = self.rfile.read(content_len)
		#print(post_data_str)
		post_data = json.loads(post_data_str)
		#pprint(post_data)
		#print(json.dumps(json.loads(post_data_str), indent=2))
		print post_data["this"]

		content = {
			'path': self.path,
			'data': post_data
		}
  
		#print(content)
		self.wfile.write(json.dumps(content))
		self.wfile.close()

class MyWebServer(SocketServer.TCPServer):
	allow_reuse_address = True

if __name__ == "__main__":
	httpd = MyWebServer(('', PORT), MyWebHandler)
	print('serving at port %d' % PORT)
	try:
		httpd.serve_forever()
		print "running"
	except KeyboardInterrupt:
	  print('bye')
	  httpd.server_close()

