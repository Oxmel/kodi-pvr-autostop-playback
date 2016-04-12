#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import shlex
import requests
import json
import time

# Tv status code returned by 'tvservice'. May vary depending on the brand
# Run 'tvservice -s' with TV turned On and Off to get your own
On = "0x12000a" 
Off = "0x120009" 
# Connect to kodi web api. Kodi control over HTTP must be activated
# Change the host IP and port according to your setup
url = "http://192.168.0.2:7331/jsonrpc?"
# Declare Header (raise an error if not configured)
headers = {'Content-Type': 'application/json'}
# Request the list of all active players
statusCmd = {'jsonrpc': '2.0', 'method': 'Player.GetActivePlayers', 'id': '1'}

def tv():
    # Read TV status using tvservice
    tvservice = subprocess.check_output(['tvservice', '-s'])
    # Split the output using shell like syntax. Much easier to parse
    tvStatus = shlex.split(tvservice)[1]
    if tvStatus == On :
        pass
    elif tvStatus == Off :
        player()

def player():
    # Check for active players
    playerStatus = json.loads(requests.post(url, 
        headers=headers, 
        json=statusCmd).text)
    # If there is no active player
    if playerStatus["result"] == [] :
        # Do nothing
        pass
    else :
        # Get active player's id
        playerId = playerStatus["result"][0]["playerid"] 
        # Stop active player based on the id
        stopCmd = {'jsonrpc':'2.0', 
                'method':'Player.Stop', 
                'id':1, 
                'params':{'playerid': playerId}}
        requests.post(url, headers=headers, json=stopCmd)


while True:
    tv()
    time.sleep(300)
