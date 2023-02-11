from typing import List, Optional
from numbers import Number

from .scenes import Scene
from time import sleep
from enum import Enum

from . import common

class SceneItem(object):
  data: dict

  def __init__(self, scene: Scene, data: dict):
    self.scene = scene
    self.data = data

  @property
  def sceneItemId(self) -> int:
    return self.data["sceneItemId"]

  @property
  def name(self) -> str:
    return self.data["sourceName"]

  @property
  def sceneItemTransform(self):
    return self.data["sceneItemTransform"]

  async def set_scene_item_transform(self, data):
    await common.connection.make_request("SetSceneItemTransform", {"sceneName": self.scene.name, "sceneItemId": self.sceneItemId, "sceneItemTransform": data})
    new_transform = await common.connection.make_request("GetSceneItemTransform", {"sceneName": self.scene.name, "sceneItemId": self.sceneItemId})
    self.data.update(new_transform)

  @property
  def __str__(self):
    return "Scene Item: Name: " + self.name

async def get_scene_item(scene: Scene, scene_item_id: int) -> Optional[SceneItem]:
  scene_items = await get_scene_items(scene)
  for item in scene_items:
    if item["sceneItemId"] == scene_item_id:
      return SceneItem(scene, item)

async def get_scene_items(scene: Scene):
  response = await common.connection.make_request("GetSceneItemList", {"sceneName": scene.name})

  items = []

  if "sceneItems" in response:
    items = response["sceneItems"]

  return items
