#!/usr/bin/env python
from __future__ import print_function
import time
from itertools import cycle
from functools import wraps
from flask import Flask, Response, request, jsonify, render_template, Request, json
import os
import sys
import shlex, subprocess

from netmiko import ConnectHandler
import textfsm
import texttable
import clitable
import pprint

import csv
import json
import urllib2

from google_csv import get_google_json
from secrets import ip, un, pw


#import RPi.GPIO as io

def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function



app = Flask(__name__)


#######################################
#   Global Netmiko & TextFSM Params   #
#######################################

# Netmiko - SSH connection information
ip_addr = ip
port = 22
username = un
password = pw
device_type = 'cisco_ios'

# Netmiko - SSH device array 

switch = {
    'ip': ip,
    'port': port,
    'username': username,
    'password': password,
    'device_type': device_type
}


# TextFSM - template file and index file (index_file path is relative to template_dir)
index_file = 'index'
template_dir = 'textfsm_templates'

#######################################
#          End Global Params          #
#######################################

# cisco ios show vlan brief
@app.route("/show-vlan", methods=['GET'])
@jsonp
def show_vlan():

    # establish ssh connection
    device = ConnectHandler(**switch)

    # define cisco ios show command
    command = 'show vlan brief'

    # Execute show commands on the channel:
    output = device.send_command(command)

    # close ssh connection gracefully
    device.disconnect()
    
    # Create CliTable object
    cli_table = clitable.CliTable(index_file, template_dir)
    attrs = {'Command': command, 'platform': device_type}

    # Dynamically parse the output from the router against the template
    cli_table.ParseCmd(output, attrs)

    # Convert cli_table to Python Dictionary
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)

    # jsonify dictionary and return result
    return jsonify(vlans=objs)


# cisco ios show interfaces status
@app.route("/show-interfaces-status", methods=['GET'])
@jsonp
def show_interfaces_status():

    # establish ssh connection
    device = ConnectHandler(**switch)

    # define show command to send to switch
    command = 'show interfaces status'

    # Execute show commands on the channel:
    output = device.send_command(command)

    # close ssh connection gracefully
    device.disconnect()
    
    # Create CliTable object
    cli_table = clitable.CliTable(index_file, template_dir)
    attrs = {'Command': command, 'platform': device_type}

    # Dynamically parse the output from the router against the template
    cli_table.ParseCmd(output, attrs)

    # Convert cli_table to Python Dictionary
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)

    # jsonify dictionary and return result
    return jsonify(interfaces=objs)

# get switch config json from google speardsheet csv
@app.route("/show-google-config", methods=['GET'])

def show_google_config():
    
    # get spreadsheet key from request param
    spreadsheet_key = request.args.get('spreadsheet_key')

    # call get_google_json() to get switch config json from google spreadsheet csv
    raw_config = get_google_json(spreadsheet_key)

    # create payload object
    config = json.loads(raw_config)

    # return JSONified switch config payload
    return jsonify(config=config)


@app.route("/configure-switch-with-google-spreadsheet", methods=['GET'])
def config_switch_google_csv():

    # get spreadsheet key from request param
    spreadsheet_key = request.args.get('spreadsheet_key')

    # call get_google_json() to get switch config json from google spreadsheet csv
    raw_config = get_google_json(spreadsheet_key)

    # create payload object
    config = json.loads(raw_config)

    # send config payload to switch config endpoint
    send_config = process_config_payload(config)

    # process_config_payload() jsonifies output, so no need here
    return send_config


# cisco ios show interfaces status
@app.route("/configure-port", methods=['POST'])
@jsonp

# request config payload from POST
def configure_port():

    # get json from POST
    payload = request.get_json()
    return process_config_payload(payload)


def process_config_payload(data):
    # convert POST payload to array if need be
    if type(data) is not type(list()):
        data = [data]

    # define Netmiko config payload as an array
    config_commands = []

    # create Netmiko config payload to pass to send_config_set() function
    for item in data:
        # Config command variables
        port = item['port']

        # Check to see if keys are present in POSTed json
        # & set command variables only if keys are present
        if 'name' in item:
            name = item['name']
            name_command = 'description ' + name
        else:
            name_command = ''

        if 'vlan' in item:
            vlan = item['vlan']
            vlan_command = 'switchport access vlan ' + vlan
        else:
            vlan_command = ''

        if 'mode' in item:
            mode = item['mode']
            mode_command = 'switchport mode ' + mode
        else: mode_command = ''

        trunk_command = 'switchport trunk encapsulation dot1q'

        # assemble multiline Netmiko config payload
        config_commands.append('interface gigabitEthernet ' + port)
        config_commands.append(name_command)
        config_commands.append(vlan_command)
        config_commands.append(trunk_command)
        config_commands.append(mode_command)
        config_commands.append('!')

    # establish ssh connection
    device = ConnectHandler(**switch)

    # Execute show commands on the channel:
    output = device.send_config_set(config_commands)

    # close ssh connection gracefully
    device.disconnect()

    # jsonify dictionary and return result
    return jsonify(message=output)

@app.route("/write-mem", methods=['GET'])
def write_mem():

    # establish ssh connection
    device = ConnectHandler(**switch)

    # set write mem command
    wr_command = "wr"

    # Execute show commands on the channel:
    output = device.send_command(wr_command)

    # close ssh connection gracefully
    device.disconnect()

    # jsonify dictionary and return result
    return jsonify(message=output)

# index
@app.route("/")
@jsonp
def index():
        #data = room_status()
		#volume_data = volume()
        #return out_json
        return render_template('index.html', power='active', data='data')

if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=80)