from ast import Str
import logging
from typing import Optional
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
from time import sleep

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

ws = simpleobsws.WebSocketClient(url = 'ws://localhost:4444', password = 'gVq6YMQlPUo3aBJa', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request(command: str, request_data: dict = {}):
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    response = {}

    request = simpleobsws.Request(command, requestData = request_data) # Build a Request object

    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
        response = ret.responseData






    await ws.disconnect() # Disconnect from the websocket server cleanly

    return response

#https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#requests-table-of-contents

async def do_thing():
  sceneResponse = await make_request("GetSceneList")
  scenes = sceneResponse["scenes"]
  print(scenes)

  # Cycle through scenes
  for scene in scenes:
    await make_request("SetCurrentProgramScene", {"sceneName": scene["sceneName"]})
    sleep(5)

loop = asyncio.get_event_loop()
loop.run_until_complete(do_thing())
