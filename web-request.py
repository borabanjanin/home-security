#!/usr/bin/env python

import json
import requests

server = 'http://localhost:8080'
headers = {
  'Accept': 'application/json'
  }
data = {
  'this': 'test',
  }

# see python-requests.org for more help

response = requests.post('%s/endpoint' % server, data=json.dumps(data), headers=headers)

response_str = response.text
if response.status_code == requests.codes.OK:
  print('Response: HTTP %s' % response.status_code)
  print(json.dumps(json.loads(response_str), indent=2))
else:
  print('Error: HTTP %s' % response.status_code)
  print(response_str)
