# gnp-discord-bot

## Install

Install inotify-tools to watch bot file being edit and reload the bot service without systemd
Screen works for running backgroud processes without systemd

```bash
pacman -Sy inotify-tools screen

virtualenv venv
pip install -r requirements.txt
```

## Usage

### Run the server daemon

Run the main daemon:

```bash
bash server.sh
```
