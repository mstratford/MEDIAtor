from typing import List
from numbers import Number
from .common import make_request
from time import sleep


#{'sceneIndex': 0, 'sceneName': 'Scene 3'}
class Scene(object):
  data: dict

  def __init__(self, data: dict):
    self.data = data

  @property
  def name(self) -> str:
    return self.data["sceneName"]

  @property
  def index(self) -> Number:
    return self.data["sceneIndex"]

  @property
  def __str__(self):
    return "Scene: Name: " + self.name

async def get_scene_list() -> List[Scene]:
  response = await make_request("GetSceneList")
  scenes = []
  if "scenes" in response:
    for scene in response["scenes"]:
      scenes.append(Scene(scene))

  return scenes

async def create_scene(sceneName: str, ignore_exits: bool = False) -> Scene:
  scenes = await get_scene_list()
  for scene in scenes:
    if scene.name == sceneName:
      if ignore_exits:
        return scene # Return existing scene
      raise Exception("Scene already exists!")

  await make_request("CreateScene", { "sceneName": sceneName })
  for i in range(10):
    scenes = await get_scene_list()
    for scene in scenes:
      if scene.name == sceneName:
        return scene
    sleep(0.2)
  raise Exception("No scene was seen after creating it.")

async def remove_scene(scene_to_remove: Scene):
  await make_request("RemoveScene", { "sceneName": scene_to_remove.name })
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

