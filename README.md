# quizshow

This is a quizshow

## Setup

1. `pip3 install -r requirements.txt`
2. `cd ETest && npm i`

## Config file

Paste this into `config.cfg`

```conf
[DEFAULT]
# How long each round is
ROUND_TIME=10
# How long the game is
GAME_TIME=60
# The ID of each board to populate with players
BOARD_STACK=65535
# Max numeber of players per board
BOARD_PLAYER_LIMIT=3
# How much to increment the score
INC_SCORE=1
# How much to decrement the score
DEC_SCORE=1
# Initial score
INIT_SCORE=0
# Database address
DB_URL=sqlite:///quizShow.db
# How long to flash the button lights when inviting a player
INVITE_SLEEP=3
# The hostname for the display
DISP_HOST=localhost:8080
# My hostname
ME_HOST=localhost:5000
# Video library
PREAMBLE_VID=./video/start.vid
```

## Usage

### QuizShowGamePlay.py

There are no CLI args

Api:

```bash
curl host.domain/ -X POST -d 'playerCount=#' # Starts a game
curl host.domain/dump -X GET # Returns all the settings and stats for the game
curl host.domain/pause -X GET # Pauses/unpauses the game
```

### Display

Docs can be found [here](Display/README.md)