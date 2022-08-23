import logging
logging.basicConfig(level=logging.DEBUG)
import simpleobsws
import json

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

with open(".obs-config.json") as file:
    creds = json.load(file)
    host = creds["host"]
    port = creds["port"]
    password = creds["pass"]

    ws = simpleobsws.WebSocketClient(url = 'ws://{}:{}'.format(host,port), password = password, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

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
