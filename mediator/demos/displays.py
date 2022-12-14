import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws

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
  response = await make_request("GetMonitorList")
  monitors = response["monitors"]


  response = await make_request("OpenSourceProjector", {"sourceName": "Scene", "monitorIndex": 0 })
  response = await make_request("OpenSourceProjector", {"sourceName": "Scene 2", "monitorIndex": 2 })



loop = asyncio.get_event_loop()
loop.run_until_complete(do_thing())
