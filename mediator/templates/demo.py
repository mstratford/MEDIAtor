from .template import Template
from typing import Optional, Any
from cerberus import Validator
from ..obs_wrapper import scenes, inputs
import pathlib
from time import sleep

class Demo(Template):
  schema = {'name': {'type': 'string'}, 'display_number': {'min': 1}}

  def __init__(self, data: dict[str, Any]):
    super()
    self.display_number = -1

    if data:
      self.validate(data)
      self.__dict__.update(data)


  def validate(self, data: Optional[dict[str, Any]]):
    v = Validator(self.schema)
    v.validate(data)
    self.is_ready = True

    return super().validate(data)

  @property
  async def scene(self) -> Optional[scenes.Scene]:
    if not self.is_ready:
      return None

    if not self._scene:

      scene = await scenes.create_scene("Demo "+str(self.display_number), ignore_exists=True)

      file_dir=str(pathlib.Path(__file__).parent.resolve()) + "/../../assets/images/"
      wallpaper = file_dir + "wallpaper.jpg"
      logo = file_dir + "logo-white.png"
      await inputs.create_input("background"+scene.name, scene, inputs.InputKind.IMAGE, {"file": wallpaper})
      logo = await inputs.create_input("logo"+scene.name, scene, inputs.InputKind.IMAGE, {
        "file": logo
      })
      scene_item = await logo.get_scene_item()
      # Width and height are readonly computed values from the scene item, must set those there.
      # https://github.com/obsproject/obs-websocket/issues/1017#issuecomment-1304944286
      if scene_item:
        transform = scene_item.sceneItemTransform
        target_width = 1920/3
        target_height = target_width
        scale_x = target_width / transform["sourceWidth"]
        scale_y = target_height / transform["sourceHeight"]
        await scene_item.set_scene_item_transform(
          {
            "positionX": (1920/3),
            "positionY": (1080 - target_height) /2,
            "scaleX": scale_x,
            "scaleY": scale_y
          }
        )
      text = await inputs.create_input("text"+scene.name, scene, inputs.InputKind.TEXT, {
        "text": "Display " + str(self.display_number),
        "font": {
          "face": "Helvetica",
          "flags": 0,
          "size": 250,
          "style": "Regular"
        }
      })
      source_width = 0
      while (source_width <= 0):
        scene_item = await text.get_scene_item()

        if scene_item:
          transform = scene_item.sceneItemTransform
          source_width = transform["sourceWidth"]
          if source_width <= 0:
            sleep(0.2)
            continue

          target_width = 1920/3
          scale_x = target_width / transform["sourceWidth"]
          await scene_item.set_scene_item_transform(
            {
              "positionX": (1920 - target_width)/2,
              "positionY": 50,
              "scaleX": scale_x,
              "scaleY": scale_x
            }
          )

        self._scene = scene

    return self._scene

