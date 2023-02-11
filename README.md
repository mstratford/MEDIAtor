# MEDIAtor
Got a screen? Want to put some fancy graphics on it? Want to do that from a nice easy UI? Hopefully MEDIAtor is here for you!

## Early in development!

# Development

## Windows (via Ubuntu 22.04 WSL)
See also: https://stackoverflow.com/questions/46610256/chmod-wsl-bash-doesnt-work
```
git config --global core.autocrlf true
sudo apt update && sudo apt upgrade
sudo apt install python-is-python3 python3-virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## OBS Configuration
Note settings under `Tools -> WebSocket Server Settings`, put these in `.obs-config.json`. A example `.dist` is provided.

Settings -> General -> Projectors
- [x] Hide cursor over projectors
- [x] Make Projectors always on top
- [ ] Save projectors on Exit
- [x] Limit to one full-screen projector per screen

## Tools

Tools can be run by commands like `python3 -m mediator.tools.obs_inspector`.


`obs_inspector.py` helps to find out about existing scenes, inputs and commands inside OBS. It outputs to `tools/outputs/*` in JSON format.

# Credits

## Images & Assets

### 'Testcard'
- Unsplash / Milad Fakurian @miladfakurian https://unsplash.com/photos/E8Ufcyxz514

### Logo
- Uxwing Icons https://uxwing.com/television-icon/ https://uxwing.com/video-production-icon/
