from typing import List, Optional
from .scenes import Scene
from time import sleep
from enum import Enum
from . import common
# 'inputKinds': ['image_source', 'color_source_v3', 'slideshow', 'av_capture_input_v2', 'coreaudio_input_capture', 'coreaudio_output_capture',
# 'screen_capture', 'display_capture', 'window_capture', 'syphon-input', 'browser_source', 'ffmpeg_source', 'text_ft2_source_v2', 'vlc_source']}


# @TODO MacOS only!
class InputKind(Enum):
  IMAGE = "image_source"
  COLOR = "color_source_v3"
  SLIDESHOW = "slideshow"
  AV_CAPTURE = "av_capture_input_v2"
  AUDIO_INPUT = 'coreaudio_input_capture',
  AUDIO_OUTPUT = 'coreaudio_output_capture'
  SCREEN_CAPTURE = "screen_capture"
  DISPLAY_CAPTURE = 'display_capture'
  WINDOW_CAPTURE = 'window_capture'
  SYPHON = 'syphon-input'
  BROWSER = 'browser_source'
  FFMPEG = 'ffmpeg_source'
  TEXT = 'text_ft2_source_v2'
  VLC = 'vlc_source'



class Input(object):
  data: dict

  def __init__(self, data: dict):
    self.data = data

  @property
  def name(self) -> str:
    return self.data["inputName"]

  @property
  def settings(self) -> dict:
    return self.data["inputSettings"]

  @property
  def kind(self) -> InputKind:
    return self.data["inputKind"]

  @property
  def __str__(self):
    return "Input: Name: " + self.name

async def create_input(name: str, scene: Scene, kind: InputKind, settings: dict) -> Input:
  params = { "inputName": f'{scene.name}-{name}', "sceneName": scene.name, "inputKind": kind.value, "inputSettings": settings}
  await common.connection.make_request("CreateInput", params)


async def get_inputs(kind: Optional[InputKind] = None):
  params = {}
  if kind:
    params["inputKind"] = kind
  response = await common.connection.make_request("GetInputList", params)

  if "inputs" in response:
    return response["inputs"]

  return []

