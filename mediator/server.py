import asyncio
from obs_wrapper import projectors, scenes, inputs
from time import sleep
import pathlib
# The MEDIAtor main server.

class MEDIAtor():
  def __init__(self):
    print("Hello! Welcome to MEDIAtor!")

  async def do_demo(self):
    monitors = await projectors.get_monitor_list()

    new_scenes = []
    for i in range(len(monitors)):

      new_scenes.append(await scenes.create_scene("Demo "+str(i), ignore_exits=True))

    file_dir=str(pathlib.Path(__file__).parent.resolve()) + "/assets/images/"
    wallpaper = file_dir + "wallpaper.jpg"
    logo = file_dir + "logo.png"
    for scene in new_scenes:
      await inputs.create_input("background"+scene.name, scene, inputs.InputKind.IMAGE, {"file": wallpaper})
      await inputs.create_input("logo"+scene.name, scene, inputs.InputKind.IMAGE, {"file": logo})
      await inputs.create_input("text"+scene.name, scene, inputs.InputKind.TEXT, {"text": "Display " + scene.name})

    sceneList = new_scenes #await scenes.get_scene_list()

    for i in range(len(sceneList)):
      await projectors.open_source_projector(sceneList[i], monitors[i])

    sleep(5)

    for monitor in monitors:
      await projectors.close_projector(monitor)

    for scene in new_scenes:
      await scenes.remove_scene(scene)



media = MEDIAtor()

loop = asyncio.get_event_loop()
loop.run_until_complete(media.do_demo())
