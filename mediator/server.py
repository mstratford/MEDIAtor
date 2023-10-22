#! /usr/bin/env python3
from time import sleep
from typing import List, Optional
from enum import Enum
import inspect
import nest_asyncio
from syncer import sync
import logging

#Websocket Server
import asyncio
from simple_websocket_server import WebSocketServer, WebSocket
import json

# MEDIAtor resources
from .obs_wrapper import projectors, scenes
from .templates import demo
from .obs_wrapper import common
class ResponseStatus(Enum):
  """Response status enums for command responses to websocket clients"""

  OK = "OK"
  MALFORMED = "MALFORMED"
  INVALID_COMMAND = "INVALID_COMMAND"
  INVALID_DATA = "INVALID_DATA"
  NOT_READY = "NOT_READY"
  SERVER_ERROR = "SERVER_ERROR"


class Response():
  """Class representing a response back to the client"""

  status: ResponseStatus
  data: Optional[dict]
  command: Optional[str]


  def __init__(self, status: ResponseStatus = ResponseStatus.OK, data: Optional[dict] = None, command: Optional[str] = None):
    """Generate a response object from data"""

    self.status = status
    self.data = data
    self.command = command

  @property
  def __dict__(self) -> dict:
    """Return a JSON serialisable dict """

    return {
      "status": self.status.value,
      "command": self.command,
      "data": self.data
    }

class MEDIAtor():
  """The MEDIAtor main websocket server"""


  def __init__(self):
    logging.info("Hello! Welcome to MEDIAtor!")
    common.connection = common.Connection()

  async def delete(self):
    if common.connection:
      await common.connection.disconnect()

class MEDIAtorWebSocketServer(WebSocket):

  #####
  ### Websocket handling functions
  #####


  def connected(self):
    """On websocket client connection, store client object in global array for broadcasts."""
    logging.info(self.address, 'connected')
    global ws_clients
    if not self in ws_clients:
        ws_clients.append(self)


  def handle_close(self):
    """Handle closing a client closing the websocket connection"""

    logging.info(self.address, 'closed')
    global ws_clients
    if self in ws_clients:
      ws_clients.remove(self)


  def handle(self):
    """
    Callback function called on a new incoming message over the websocket.

    Used to decode message, route it to a command function and respond.
    """

    logging.info(self.data)

    response: Response

    # Check/parse if it's valid JSON
    message: dict = {}
    try:
      data = str(self.data)
      message = json.loads(data)
    except Exception:
      logging.error("Decode Error! Message is not valid JSON.")
      self.send_response(Response(ResponseStatus.MALFORMED))


    if ("command" not in message):
      logging.error("No command found in message.")
      self.send_response(Response(ResponseStatus.MALFORMED))
      return

    command = message["command"]

    # Look for a function in this class called "command_{the_command}", default to None if not present.
    command_function = getattr(self, 'command_' + command, None)

    if not command_function:
      self.send_response(Response(ResponseStatus.INVALID_COMMAND, command=command))
      return

    message_has_data = "data" in message and message["data"]
    # call the command, each command should send any responses required.
    if inspect.iscoroutinefunction(command_function):
      command_requires_data = "data" in inspect.getfullargspec(command_function)[0]
      if message_has_data:
        if command_requires_data:
          response = sync(command_function(message["data"]))
        else:
          response = Response(ResponseStatus.INVALID_DATA, data={"Reason": "This command does not accept data parameters."})
      else:
        response = sync(command_function())
    else:
      command_requires_data = "data" in inspect.getfullargspec(command_function)[0]
      if message_has_data:
        if command_requires_data:
          response = command_function(message["data"])
        else:
          response = Response(ResponseStatus.INVALID_DATA, data={"Reason": "This command does not accept data parameters."})
      else:
        response = command_function()

    if not isinstance(response, Response):
      self.send_response(Response(ResponseStatus.SERVER_ERROR, command=command))
      logging.exception(f"Command function {command_function} did not return Response!")
      return

    # The command function doesn't return the command in the response, plug that in here.
    response.command = command

    self.send_response(response)


  # Send data to client
  def send(self, data: dict):
    self.send_message(json.dumps(data))

  # Send formatted response to client
  def send_response(self, response: Response):
    self.send(response.__dict__)


  ######
  ### Command Functions
  ######

  def command_ping(self):
    """Responds to a ping with a pong!"""

    return Response(data={
      "pong": True
    })


  async def command_demo_start(self, data: Optional[dict] = None):
    """Triggers display enumeration demo on monitors"""

    monitor_indexes = []
    if data:
      if "monitor_indexes" in data and isinstance(data["monitor_index"], list):
        monitor_indexes = data["monitor_indexes"]

    monitors = await projectors.get_monitor_list()

    await scenes.remove_all_scenes()

    new_scenes = []
    for monitor in monitors:
      if monitor_indexes and monitor.index not in monitor_indexes:
        continue

      template = demo.Demo({'name': f"Demo Display {monitor.index}", 'display_number': monitor.index})

      new_scenes.append(await template.scene)


      await projectors.open_source_projector(new_scenes[-1], monitor)

    return Response()


  async def command_close_projectors(self):
    """Triggers all projectors (screens) to close"""

    monitors = await projectors.get_monitor_list()
    monitors=monitors[1:2]
    for monitor in monitors:
      await projectors.close_projector(monitor)

    for scene in await scenes.get_scene_list():
      await scene.delete()

    #await self.delete()

    return Response()


ws_clients: List[MEDIAtorWebSocketServer] = []


async def run_websocket_server():
    websocket_server = WebSocketServer('localhost', 8082, MEDIAtorWebSocketServer)
    websocket_server.serve_forever()


def main():

    media = MEDIAtor()
    asyncio.run(
        run_websocket_server(),
        debug=True
    )


if __name__ == "__main__":
  logging.getLogger("asyncio").setLevel(logging.DEBUG)
  logging.basicConfig(level=logging.DEBUG)
  main()
