from typing import Any, Optional, Dict
from ..obs_wrapper import scenes
class Template(object):
  _ready = False
  _scene = None

  # Creates object, if data is present, load in an existing template of this type.
  def __init__(self, data: dict[str, Any]):
    self.name = data["name"]

#  # Trigger deletion of the OBS scene
#  def __del__(self):
#    print(f"Deleting template {self.name}")
#    delattr(self,"scene")


  # Write parameter validations in here.
  # This could be used to pre-validate a configuration without saving.
  # Return Exceptions for invalid parameters
  def validate(self, data: Optional[dict[str, Any]]):
    pass

  # Set template configuration options. Any dict keys present should be validated and updated.
  def update(self, data: dict[str, Any]):
    pass

  # Return if we have enough & valid configuration to display something.
  @property
  def is_ready(self) -> bool:
    return self._ready

  @is_ready.setter
  def is_ready(self, ready: bool):
    self._ready = ready

  # Generates an OBS scene with the current template configurationm
  # Returns reference to the scene
  @property
  async def scene(self) -> Optional[scenes.Scene]:
    return self._scene

  @scene.deleter
  def scene(self):
    print("Deleting scene")
    if self._scene:
      # Sync required because deleters can't be async it seems?
      del self._scene
    self._scene = None
