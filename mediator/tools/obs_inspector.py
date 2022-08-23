# OBS Inspector.
# Loads in all of the current inputs from OBS scenes and displays their parameters.
# Useful for writing new input types programmatically.

import asyncio
import json
import logging
import pathlib
from mediator.obs_wrapper.general import get_version
from mediator.obs_wrapper.inputs import get_inputs
from mediator.obs_wrapper.scene_items import get_scene_items

from mediator.obs_wrapper.scenes import Scene, get_scene_list, get_scene

logging.basicConfig(level=logging.DEBUG)

async def inspect(scene_name = None, item_name = None):
  if scene_name:
    scene = await get_scene(scene_name)
    if not scene:
      logging.error("Could not find scene named: " + scene_name)
      return
    scenes = [scene]
  else:
    scenes = await get_scene_list()

  if len(scenes) == 0:
    logging.error("No scenes found.")
    return

  for scene in scenes:
    logging.info("Found Scene: " + scene.name)
    await inspect_scene(scene)

async def inspect_scene(scene: Scene):
  file_path = str(pathlib.Path(__file__).parent.resolve())+"/outputs/scene-{}.json".format(scene.name)
  logging.info("Writing scene inspection to " + file_path)
  with open(file_path, 'w') as file:

    file.write(json.dumps({
      "scene": scene.__dict__,
      "items": await get_scene_items(scene=scene)
    }, indent=2))


async def inspect_api():
  response = await get_version()
  response_json = json.dumps(response, indent=2)
  logging.info("Writing API info output to obs-info.json")
  with open(str(pathlib.Path(__file__).parent.resolve())+"/outputs/obs-info.json", "w") as file:
    file.write(response_json)

async def main():
  await inspect_api()
  await inspect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
