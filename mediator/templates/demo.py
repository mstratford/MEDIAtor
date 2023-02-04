from .template import Template
from typing import Optional, Any
from cerberus import Validator
from ..obs_wrapper import scenes, inputs
import pathlib

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

      scene = await scenes.create_scene("Demo "+str(self.display_number), ignore_exits=True)

      file_dir=str(pathlib.Path(__file__).parent.resolve()) + "/../../assets/images/"
      wallpaper = file_dir + "wallpaper.jpg"
      logo = file_dir + "logo.png"
      await inputs.create_input("background"+scene.name, scene, inputs.InputKind.IMAGE, {"file": wallpaper})
      await inputs.create_input("logo"+scene.name, scene, inputs.InputKind.IMAGE, {"file": logo})
      await inputs.create_input("text"+scene.name, scene, inputs.InputKind.TEXT, {"text": "Display " + scene.name})

      self._scene = scene

    return self._scene

