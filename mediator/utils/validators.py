import string

def is_valid_color(field, color, error):
  if not isinstance(color, str):
    error(field, "Must be a str")
  elif len(color) != 7:
    error(field, "Must be 7 chars long (#000000).")
  elif not color.startswith("#"):
    error(field, "Must begin with #")
  if not all(c in string.hexdigits for c in color[1:]):
    error(field, "Must be a valid hex code")
