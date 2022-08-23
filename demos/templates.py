from ast import Str
import logging
from pickle import TRUE
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
  scene_name = "TemplateScene"
  #await make_request("CreateScene", {"sceneName": scene_name})

  #response = await make_request("GetInputKindList")
  # 'inputKinds': ['image_source', 'color_source_v3', 'slideshow', 'av_capture_input_v2', 'coreaudio_input_capture', 'coreaudio_output_capture', 'screen_capture', 'display_capture', 'window_capture', 'syphon-input', 'browser_source', 'ffmpeg_source', 'text_ft2_source_v2', 'vlc_source']}
  settings = {
    "width": 1920,
    "height": 1080,
    "url": "https://ury.org.uk/timelord"
  }
  #response = await make_request("CreateInput", {"sceneName": scene_name, "inputName": "Browser Source", "inputKind": "browser_source", "inputSettings": settings, "sceneItemEnabled": True})

  response = await make_request("GetInputSettings", {"inputName": "Image"})

  #await make_request("SetCurrentProgramScene", {"sceneName": scene_name})

  #response = await make_request("OpenSourceProjector", {"sourceName": scene_name, "monitorIndex": 0 })

  #sleep(5)



  #await make_request("RemoveScene", {"sceneName": scene_name})

loop = asyncio.get_event_loop()
loop.run_until_complete(do_thing())
