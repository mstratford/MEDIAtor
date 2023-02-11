import logging
logging.basicConfig(level=logging.WARNING)
import simpleobsws
import json

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)
connection = None
class Connection():
    ws = None
    def __init__(self):
        pass

    async def connect(self):
        with open(".obs-config.json") as file:
            creds = json.load(file)
            host = creds["host"]
            port = creds["port"]
            password = creds["pass"]

            self.ws = simpleobsws.WebSocketClient(url = 'ws://{}:{}'.format(host,port), password = password, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.
            await self.ws.connect() # Make the connection to obs-websocket
            await self.ws.wait_until_identified() # Wait for the identification handshake to complete

    async def disconnect(self):
        if self.ws:
            await self.ws.disconnect() # Disconnect from the websocket server cleanly

    async def make_request(self, command: str, request_data: dict = {}):

        if not self.ws:
            await self.connect()

        response = {}

        request = simpleobsws.Request(command, requestData = request_data) # Build a Request object

        if self.ws:
            ret = await self.ws.call(request) # Perform the request
            if ret.ok(): # Check if the request succeeded
                #print("Request succeeded! Response data: {}".format(ret.responseData))
                response = ret.responseData



        return response
