import asyncio
from .obs_wrapper import projectors, scenes
from time import sleep
from .templates import demo
from .obs_wrapper import common
# The MEDIAtor main server.

class MEDIAtor():
  def __init__(self):
    print("Hello! Welcome to MEDIAtor!")
    common.connection = common.Connection()

  async def delete(self):
    if common.connection:
      await common.connection.disconnect()


  async def do_demo(self):
    monitors = await projectors.get_monitor_list()

    await scenes.remove_all_scenes()

    new_scenes = []
    for i in range(len(monitors)):

      template = demo.Demo({'name': f"Demo Display {i}", 'display_number': i})

      new_scenes.append(await template.scene)


    for i in range(len(new_scenes)):
      await projectors.open_source_projector(new_scenes[i], monitors[i])

    sleep(5)

    for monitor in monitors:
      await projectors.close_projector(monitor)

    for scene in new_scenes:
      await scene.delete()

    await self.delete()



media = MEDIAtor()

loop = asyncio.get_event_loop()
loop.run_until_complete(media.do_demo())
