# quizshow

This is a quizshow

## Setuup

1. `pip3 install -r requirements.txt`
2. `cd ETest && npm i`

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