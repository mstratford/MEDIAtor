from typing import List, Optional
from numbers import Number

from .scenes import Scene
from time import sleep
from enum import Enum

from . import common

class SceneItem(object):
  data: dict

  def __init__(self, data: dict):
    self.data = data

  @property
  def name(self) -> str:
    return self.data["sourceName"]

  @property
  def __str__(self):
    return "Scene Item: Name: " + self.name

async def get_scene_items(scene: Scene):
  response = await common.connection.make_request("GetSceneItemList", {"sceneName": scene.name})

  items = []

  if "sceneItems" in response:
    items = response["sceneItems"]

  return items
