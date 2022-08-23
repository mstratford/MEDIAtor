from typing import List
from numbers import Number
from . import scenes
from .common import make_request\

# {'monitors': [{'monitorHeight': 1692, 'monitorIndex': 0, 'monitorName': 'ASUS PB287Q(0)', 'monitorPositionX': 0, 'monitorPositionY': 0, 'monitorWidth': 3008}, {'monitorHeight': 1200, 'monitorIndex': 1, 'monitorName': 'Color LCD(1)', 'monitorPositionX': -1920, 'monitorPositionY': 492, 'monitorWidth': 1920}, {'monitorHeight': 1692, 'monitorIndex': 2, 'monitorName': 'ASUS MG28U(2)', 'monitorPositionX': 3008, 'monitorPositionY': 0, 'monitorWidth': 3008}]}
class Monitor(object):
  data: dict

  def __init__(self, data: dict):
    self.data = data

  @property
  def height(self) -> Number:
    return self.data["monitorHeight"]

  @property
  def width(self) -> Number:
    return self.data["monitorWeight"]

  @property
  def position_x(self) -> Number:
    return self.data["monitorPositionX"]

  @property
  def position_y(self) -> Number:
    return self.data["monitorPositionY"]

  @property
  def name(self) -> str:
    return self.data["monitorName"]

  @property
  def index(self) -> Number:
    return self.data["monitorIndex"]

  @property
  def __str__(self):
    return "Monitor: Name: " + self.name

async def get_monitor_list() -> List[Monitor]:
  response = await make_request("GetMonitorList")
  monitors = []
  if "monitors" in response:
    for monitor in response["monitors"]:
      monitors.append(Monitor(monitor))

  return monitors

# TODO Return bool
async def open_source_projector(source: scenes.Scene, monitor: Monitor):
  await make_request("OpenSourceProjector", {"sourceName": source.name, "monitorIndex": monitor.index })


# Kind of a hack, OBS API doesn't let you close the projector.
async def close_projector(monitor: Monitor):
  if not monitor:
    raise Exception("No monitor provided.")

  temp_scene = await scenes.create_scene("temp-RemoveProjector", ignore_exits=True)
  # Because we've set only one full screen projector per monitor (@TODO Actually set this automatically!),
  # we can replace it with another projector, then delete the scene. This will close the projector window.
  await open_source_projector(temp_scene, monitor)
  await scenes.remove_scene(temp_scene)

