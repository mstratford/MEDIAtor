from typing import List, Optional
from .scenes import Scene, get_scene
from .scene_items import get_scene_item, SceneItem
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
  data: dict = {}

  def __init__(self, data: dict):
    self.data = data

  @property
  def name(self) -> str:
    return self.data["inputName"]

  @property
  async def settings(self) -> Optional[dict]:
    settings = await common.connection.make_request("GetInputSettings", {"inputName": self.name})
    defaults = await common.connection.make_request("GetDefaultSettings", {"inputKind": self.kind})
    print(settings,defaults)
    full_settings = {}
    if "defaultInputSettings" in defaults:
      full_settings.update(defaults["defaultInputSettings"])

    if "inputSettings" in settings:
      full_settings.update(settings["inputSettings"])
    self.data["inputSettings"] = full_settings
    return self.data["inputSettings"]

  @property
  def kind(self) -> InputKind:
    return self.data["inputKind"]

  @property
  def sceneItemId(self) -> Optional[int]:
    if "sceneItemId" in self.data:
      return self.data["sceneItemId"]

  async def get_scene_item(self) -> Optional[SceneItem]:
    scene = await get_scene(self.data["sceneName"])
    if scene:
      if self.sceneItemId:
        return await get_scene_item(scene,self.sceneItemId)

  @property
  def __str__(self):
    return "Input: Name: " + self.name

  async def __dict__(self):
    await self.settings
    return self.data

async def create_input(name: str, scene: Scene, kind: InputKind, settings: dict) -> Input:
  params = { "inputName": f'{scene.name}-{name}', "sceneName": scene.name, "inputKind": kind.value, "inputSettings": settings}
  scene_item_id = await common.connection.make_request("CreateInput", params)
  params.update(scene_item_id)
  return Input(params)


async def get_inputs(kind: Optional[InputKind] = None) -> List[Input]:
  params = {}
  if kind:
    params["inputKind"] = kind
  response = await common.connection.make_request("GetInputList", params)

  if "inputs" in response:
    input_objs = []
    for input in response["inputs"]:
      input_objs.append(Input(input))
    return input_objs

  return []

