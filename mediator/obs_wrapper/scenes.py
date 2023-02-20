import json
from typing import List, Optional
from numbers import Number
from . import common
from time import sleep

EMPTY_SCENE_NAME = "MEDIAtor Empty Scene"

#{'sceneIndex': 0, 'sceneName': 'Scene 3'}
class Scene(object):
  data: dict

  def __init__(self, data: dict):
    self.data = data

  async def delete(self):
    await remove_scene(self)
    del self

  @property
  def name(self) -> str:
    return self.data["sceneName"]

  @property
  def index(self) -> Number:
    return self.data["sceneIndex"]

  @property
  def __str__(self):
    return "Scene: Name: " + self.name

  @property
  def __dict__(self):
    return {
      "name": self.name,
      "index": self.index
    }

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

async def get_scene_list() -> List[Scene]:
  response = await common.connection.make_request("GetSceneList")
  scenes = []
  if "scenes" in response:
    for scene in response["scenes"]:
      scenes.append(Scene(scene))

  return scenes

async def get_scene(name: str) -> Optional[Scene]:
  scenes = await get_scene_list()
  for scene in scenes:
    if scene.name == name:
      return scene

async def create_scene(name: str, ignore_exists: bool = False) -> Scene:
  scenes = await get_scene_list()
  for scene in scenes:
    if scene.name == name:
      if ignore_exists:
        return scene # Return existing scene
      raise Exception("Scene already exists!")

  await common.connection.make_request("CreateScene", { "sceneName": name })
  for i in range(20):
    scenes = await get_scene_list()
    for scene in scenes:
      if scene.name == name:
        return scene
    sleep(0.2)
  raise Exception("No scene was seen after creating it.")

async def remove_scene(scene_to_remove: Scene):
  scenes = await get_scene_list()
  # Can't have 0 scenes, create a blank one.
  if len(scenes) <= 1:
    await create_blank_scene()

  # We always need to keep one scene
  if scene_to_remove.name == EMPTY_SCENE_NAME:
    return

  await common.connection.make_request("RemoveScene", { "sceneName": scene_to_remove.name })
  found = False
  for i in range(4):
    scenes = await get_scene_list()
    for scene in scenes:
      if scene.name == scene_to_remove.name:
        found = True

    if found:
      found = False
      sleep(0.2)
      continue
    else:
      break
  if found:
    raise Exception("Failed to remove scene, it still exists!")

async def create_blank_scene():
  print("Create blank scene")
  await create_scene(EMPTY_SCENE_NAME, ignore_exists=True)

async def remove_all_scenes():
  # You can't have 0 scenes, so create an empty one before removing the rest.
  await create_blank_scene()
  scenes = await get_scene_list()

  for scene in scenes:
    if scene.name != EMPTY_SCENE_NAME:
      await remove_scene(scene)
