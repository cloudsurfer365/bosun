#!/usr/bin/env python

import json
import csvmapper
import requests

def get_google_json(spreadsheet_key):
	
	# google spreadsheet csv url
	url = "https://docs.google.com/spreadsheets/d/" + spreadsheet_key + "/pub?output=csv"

	# get csv url response
	response = requests.get(url)
	assert response.status_code == 200, 'Wrong status code'

	# open csv and write csv response
	f = open('google_csv.csv', 'w')
	f.write(response.content)
	f.close()


	# how does the object look
	mapper = csvmapper.DictMapper([ 
	  [ 
	     { 'name' : 'port'},
	     { 'name' : 'name' },
	     { 'name' : 'vlan'},
	     { 'name' : 'mode' }
	  ]
	 ])

	# parser instance
	parser = csvmapper.CSVParser('google_csv.csv', mapper, hasHeader=True)
	# conversion service
	converter = csvmapper.JSONConverter(parser)

	json_config = converter.doConvert(pretty=True)

	read_json = json.loads(json_config)

	return json_config
