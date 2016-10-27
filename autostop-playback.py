#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import shlex
import httplib
import json

# Tv status code returned by 'tvservice'. May vary depending on the brand
# Run 'tvservice -s' with TV turned On and Off to get your own
On = "0x12000a" 
Off = "0x120009" 
# Connect to kodi web api. Kodi control over HTTP must be activated
url = "localhost:8080"
# Declare Headers
headers = {'Content-Type': 'application/json'}

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
    # Request the list of all active players
    params = {'jsonrpc': '2.0', 'method': 'Player.GetActivePlayers', 'id': '1'}
    # Check for active players
    conn = httplib.HTTPConnection(url)
    conn.request('POST', '/jsonrpc?', json.dumps(params), headers)
    response = conn.getresponse()
    playerStatus = json.loads(response.read())

    if playerStatus["result"] == [] :
        conn.close()
        pass
    else :
        # Get active player's id
        playerId = playerStatus["result"][0]["playerid"] 
        # Stop active player based on its id
        stopCmd = {'jsonrpc':'2.0', 'method':'Player.Stop', 'id':1, 'params':{'playerid': playerId}}
        conn.request('POST', '/jsonrpc?', json.dumps(stopCmd), headers)
        conn.close()

tv()
