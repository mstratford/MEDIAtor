import pathlib

def get_relative_obs_filepath(file: str):
  # TODO Improve this
  file = get_relative_filepath(file)
  # Probably on WSL, OBS won't be in WSL to rewrite them.
  # /mnt/c/ -> C:/
  if file.startswith("/mnt/"):
    file = file[5].capitalize() + ":" + file[6:]

  return file

def get_relative_filepath(file: str):
  new_file = file
  if not file.startswith((".", "/")):
    new_file = "/" + file

  file = str(pathlib.Path(__file__).parent.parent.resolve()) + new_file
  print(file)
  return file
