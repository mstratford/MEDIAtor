import websocket
import json
import time
ws = websocket.WebSocket()

ws.connect("ws://localhost:8082")

def send_command(name, data = None):
  ws.send(json.dumps({
    "command": name,
    "data": data
  }))

send_command("load_preset", {"preset_number": 1})
#send_command("demo_start")
time.sleep(3)
send_command("close_projectors")
print(ws.recv())

ws.close()
