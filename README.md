# Footron API Setup

This guide is incomplete. We should finish it.

Base system is Ubuntu 20.04 Server. For best results, try to follow each section in order.

## Create users

- Create `ft` user
- TODO: Finish this section
  - Permissions
  - Groups
  - The setup and reasoning behind `/var/www/<url>/html` being owned by `ft`

## Installing applications

- `sudo apt install python3 python3-pip nginx`

## Preparing dotfiles

- Create a `config.toml` file following the format of `example-config.toml`, substituting in actual values
  - We should have these secrets stored somewhere safe
- Run `python3 -mpip install -r requirements.txt`
- `python3 compile.py`

Rendered dotfiles will be in `build/`

## Nginx

TODO: Go into our `/var/www/<url>/html` setup, including permission gotchas, SCP

## Certbot setup

TODO: Document how we set and renew Certbot (we use whatever the default Nginx plugin is)

## Footron API setup

- `pip install --upgrade git+https://github.com/BYU-PCCL/footron-api.git`
- Create a new directory `~/.local/share/footron`

Right now the command @vinhowe has been just running in `screen` is:
```sh
FT_LOG_LEVEL=debug FT_BASE_URL=https://{{ production_url }} FT_CONTROLLER_URL=http://{{ production_controller_api_url }} python3 -m uvicorn --ws-ping-interval 5 --ws-ping-timeout 5 footron_api.app:app --host 0.0.0.0
```
...but we should be using systemd like we do on the controller.

## systemd config

TODO: Configure systemd instead of just using a screen session. Our command looks like this:
