def hex_to_obs(color: str):
  color = color.strip("#")

  value = 0
  for i in range(0, len(color), 2):
    print(i)
    value = value * 16
    print(color[i:i+2])
    color_section = int(color[i:i+2],16)
    print(color_section)
    value += color_section
  return value

print(hex_to_obs("#d1d1d1FF"))
