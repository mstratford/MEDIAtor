from .template import Template
from typing import Optional, Any
from cerberus import Validator
from ..obs_wrapper import scenes, inputs
from ..utils import validators, colors
from time import sleep

class SolidColor(Template):
  # color is 7 chars,
  schema = {'name': {'type': 'string', 'required': True}, 'color': {'check_with': validators.is_valid_color}}

  def __init__(self, data: dict[str, Any]):
    super()
    self.color = "#000000"

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

      scene = await scenes.create_scene(self.name, ignore_exists=True)


      background = await inputs.create_input("background"+scene.name, scene, inputs.InputKind.COLOR, {"color": colors.hex_to_obs(self.color), "width": 1920, "height": 1080})

      self._scene = scene

    return self._scene

