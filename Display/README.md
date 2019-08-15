# Quiz Show

This is the display component of the quiz show

- [Quiz Show](#quiz-show)
  - [Installation](#installation)
  - [.env Config](#env-config)
  - [Usage](#usage)
    - [POST /](#post)
    - [DELETE /](#delete)
    - [POST /start](#post-start)
    - [POST /restart](#post-restart)

## Installation

``` bash
cd ETest
npm install
```

## .env Config

Configuring the timers comes from the enviroment. Create a `.env` file next to `index.js` and then paste this in:

```conf
# How long each round is
ROUND_SECONDS = 6

# How long the game is
GAME_SECONDS = 360

# Link to preable video
PREAMBLE_VIDEO = http://localhost:3000/path/to/video
```

## Usage

All interactions are done via `http` on port `8080`

### POST / 

Posts new settings for the display. Setting are provided as a JSON object in the request body

```javascript
{
  'question': 'Set the question',
  'red': 'Set the red answer',
  'green': 'Set the green answer',
  'blue': 'Set the blue answer',
  'yellow': 'Set the yellow answer',
  'red-correct': 'Mark the red answer as correct',
  'green-correct': 'Mark the green answer as correct',
  'blue-correct': 'Mark the blue answer as correct',
  'yellow-correct': 'Mark the yellow answer as correct',
  'red-selected': 'Mark the red answer as selected',
  'green-selected': 'Mark the green answer as selected',
  'blue-selected': 'Mark the blue answer as selected',
  'yellow-selected': 'Mark the yellow answer as selected',
  'score': 'Set the score',
  'roundtick': 'Set the current round tick',
  'gametick': 'Set the current game tick',
  'roundsup': '',
  'gameover': '',
  'wrong': ''
  'videoplay': 'Play a video from the path you set here',
  'audioplay': 'Play audio from the path you set here'
}
```

### DELETE /

Quits the display

### POST /start

Starts the round. If the game isn't running yet then it starts the game

### POST /restart

Restarts the display