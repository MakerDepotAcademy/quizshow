require('dotenv').config()

const { app, BrowserWindow, ipcMain } = require('electron')
const EventEmitter = require('events')
const request = require('request')
const fs = require('fs')
var bodyParser = require('body-parser')
var api = require('express')()
var win
var score = 0, roundTicksLimit = roundTicks = -1, gameTicksLimit = gameTicks = -1, roundTicker, gameTicker
GameEvents = new EventEmitter()

function updateUI(channel, msg, res) {
  if (win) {
    win.webContents.send(channel, msg);
    res && res.status(200).send('Display updated')
    console.log('Updated UI', channel, msg)
    return true;
  }
  else {
    res && res.status(500).send('Error communicating with render process')
    console.error('No display')
    return false;
  }
}

api.post('/', bodyParser.json(), (req, res) => {
  if (!win) {
    console.error('Display not working')
    res.status(500).send('Display is not working')
  }
  else if (gameTicks < 0 && gameTicks != -1) {
    console.log('Process blocked, game over')
    res.status(400).send('Game over')
  }
  else {
    /**
   * {
   *    "channel": "arg",
   *    ...
   * }
   */

    for (let key in req.body){
      let body = req.body[key]

      if (key == 'subscribe') {
        console.log('Adding new subscription', body)
        GameEvents.on(body.event, () => {
          try {
            request(body)
          }
          catch (e) {
            console.error(e)
          }
        })
        continue
      }

      if (key.includes('timer')) {
        if (key.includes('round')) {
          roundTicks = roundTicksLimit = body
        }
        if (key.includes('game')) {
          gameTicks = gameTicksLimit = body
        }
        continue
      }

      console.log('Processing ', key)
      if (!updateUI(key, body)) {
        res.status(500).send(`Channel ${key} failed`)
        console.error('Process failed')
        return
      }
    }

    res.send('Done')
  }
  
})

api.delete('/', (req, res) => {
  console.log('Quitting')
  app.quit();
  res.status(200).send('Quitting display')
})

const clearTimer = (round, game) => {
  if (round) {
    console.log('Clearing round timer')
    clearInterval(roundTicker)
    roundTicker = null
    roundTicks = roundTicksLimit
  }
  if (game) {
    console.log('Clearing game timer')
    clearInterval(gameTicker)
    gameTicker = null
    gameticks = gameTicksLimit
  }
}

api.post('/pause', (req, res) => {
  console.log('pause')
  clearInterval(gameTicker)
  clearInterval(roundTicker)
  roundTicker = null
  gameTicker = null
  res.send('Paused')
})

api.post('/start', (req, res) => {
  if (roundTicksLimit == -1 || gameTicksLimit == -1) {
    res.status(400).send('Times not set')
    console.error('Timers not set')
    return
  }
  if (!roundTicker) {
    console.log('Starting round ticker')
    roundTicker = setInterval(() => {
      updateUI('roundtick', roundTicks)
      if (roundTicks-- < 1) {
        console.log('Rounds up')
        updateUI('roundsup', '')
        clearTimer(true, false)
        GameEvents.emit('roundover')
      }
    }, 1000)
  }
  if (!gameTicker) {
    console.log('Starting game ticker')
    gameTicker = setInterval(() => {
      updateUI('gametick', gameTicks)
      if (gameTicks-- < 1) {
        console.log('Game over')
        updateUI('gameover', '')
        clearTimer(true, true)
        GameEvents.emit('gameover')
      }
    }, 1000)
  }

  res.status(200)

  if (gameTicks == gameTicksLimit) {
    res.send('Game started')
  }
  else {
    res.send('Round started')
  }
})

api.post('/restart', (req, res) => {
  clearTimer(true, true)
  win.reload()
  res.send('restarted')
})

app.on('ready', () => {
  // Create the browser window.
  win = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false,
    webPreferences: {
      nodeIntegration: true
    },
    webSecurity: false
  })
  win.maximize()
  win.loadFile('app/index.html')
  win.on('closed', () => {
    win = null
  })

  api.listen(8080, '0.0.0.0', () => console.log('Listening...'))
})

