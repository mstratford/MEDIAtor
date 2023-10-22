import asyncio
from .obs_wrapper import projectors, scenes
from time import sleep
from .templates import demo, solid_color
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
    #monitors=monitors[1:2]
    await scenes.remove_all_scenes()

    new_scenes = []
    colors = ["#FF0000", "#00FF00", "0000FF"]
    for monitor in monitors:

      template = demo.Demo({'name': f"Demo Display {monitor.index}", 'display_number': monitor.index})
      #template = solid_color.SolidColor({'name': f"Color {monitor.index}", 'color': colors[monitor.index % len(colors)]})
      new_scenes.append(await template.scene)


      await projectors.open_source_projector(new_scenes[-1], monitor)

    sleep(5)

    for monitor in monitors:
      await projectors.close_projector(monitor)

    for scene in new_scenes:
      await scene.delete()

    await self.delete()



media = MEDIAtor()

loop = asyncio.new_event_loop()
loop.run_until_complete(media.do_demo())
