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

# Url of Kodi web api. Kodi control over HTTP must be activated
url = "localhost:8080"
# Declare Headers
headers = {'Content-Type': 'application/json'}
# Target any active player (video or audio)
params = {'jsonrpc': '2.0', 'method': 'Player.GetActivePlayers', 'id': '1'}

def tv():
    try :
        # Get TV status using tvservice
        tvService = subprocess.check_output(['tvservice', '-s'])
        # Split the output using shell like syntax. Much easier to parse
        tvStatus = shlex.split(tvService)[1]
        if tvStatus == On :
            pass
        elif tvStatus == Off :
            player()
        else :
            print "Unable to determine TV status. Please verify status codes."
    except OSError :
        print "Error while grabbing the status code. Please verify if tvservice is installed."

def player():
    try :
        conn = httplib.HTTPConnection(url)
        # Ask Kodi web api if a player's currently active
        conn.request('POST', '/jsonrpc?', json.dumps(params), headers)
        # Read json response
        playerStatus = json.loads(conn.getresponse().read())
        if playerStatus["result"] == [] :
            pass
        else :
            # Get active player's id
            playerId = playerStatus["result"][0]["playerid"]
            # Stop active player based on its id
            stopCmd = {'jsonrpc':'2.0', 'method':'Player.Stop', 'id':1, 'params':{'playerid': playerId}}
            conn.request('POST', '/jsonrpc?', json.dumps(stopCmd), headers)
        conn.close()
    except StandardError :
        print "Unable to determine player status. Please verify url."


tv()
