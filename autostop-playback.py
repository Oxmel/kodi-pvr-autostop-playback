#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import shlex
import httplib
import json

# Tv status code returned by 'tvservice'. May vary depending on the brand
# Run 'tvservice -s' with TV turned On and Off to get your own
on = "0x12000a"
off = "0x120009"

# Url of Kodi web api. Kodi control over HTTP must be activated
url = "localhost:8080"
# Declare Headers
headers = {'Content-Type': 'application/json'}
# Target any active player (video or audio)
params = {'jsonrpc': '2.0', 'method': 'Player.GetActivePlayers', 'id': '1'}

def tv():
    try :
        # Get TV status using tvservice
        tv_service = subprocess.check_output(['/usr/bin/tvservice', '-s'])
        # Split the output using shell like syntax. Much easier to parse
        tv_status = shlex.split(tv_service)[1]
        if tv_status == on :
            pass
        elif tv_status == off :
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
        player_status = json.loads(conn.getresponse().read())
        if player_status["result"] == [] :
            pass
        else :
            # Get active player's id
            player_id = player_status["result"][0]["playerid"]
            # Stop active player based on its id
            stop_cmd = {'jsonrpc':'2.0', 'method':'Player.Stop', 'id':1, 'params':{'playerid': player_id}}
            conn.request('POST', '/jsonrpc?', json.dumps(stop_cmd), headers)
        conn.close()
    except StandardError :
        print "Unable to determine player status. Please verify url."

# Call the main function in a cleaner fashion
if __name__ == '__main__':
    tv()
