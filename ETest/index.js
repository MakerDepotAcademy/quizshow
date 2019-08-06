require('dotenv').config()

const { app, BrowserWindow, ipcMain } = require('electron')
const EventEmitter = require('events')
const request = require('request')
var bodyParser = require('body-parser')
var api = require('express')()
var win
var score = 0, roundTicksLimit = roundTicks = parseInt(process.env.ROUND_SECONDS), gameTicksLimit = gameTicks = parseInt(process.env.GAME_SECONDS), roundTicker, gameTicker
GameEvents = new EventEmitter()

function updateUI(channel, msg, res) {
  if (win) {
    win.webContents.send(channel, msg);
    res && res.status(200).send('Display updated')
    return true;
  }
  else {
    res && res.status(500).send('Error communicating with render process')
    console.error('No display')
    return false;
  }
}

api.use(bodyParser.urlencoded({ extended: false }))

api.use((req, res, next) => {
  req.body = Object.keys(req.body)[0]
  next()
})

api.use((req, res, next) => {
  if (gameTicks < 1) {
    res.status(401).send('Game over')
  }
  else {
    next()
  }
})

api.get('/', (req, res) => {
  if (win) {
    res.status(200).send('Display is working')
  }
  else {
    res.status(500).send('Display is not working')
  }
})

api.delete('/', (req, res) => {
  app.quit();
  res.status(200).send('Quitting display')
})

api.post('/question', (req, res) => {
  updateUI('question', req.body, res)
})

api.post('/answer/:label', (req, res) => {
  updateUI(req.params.label, req.body, res)
})

api.post('/start', (req, res) => {
  roundTicker = setInterval(() => {
    updateUI('roundtick', roundTicks)
    if (roundTicks-- < 1) {
      updateUI('roundsup', '')
      roundTicks = roundTicksLimit
      clearInterval(roundTicker)
      GameEvents.emit('roundover')
    }
  }, 1000)

  if (!gameTicker) {
    gameTicker = setInterval(() => {
      updateUI('gametick', gameTicks)
      if (gameTicks-- < 1) {
        updateUI('gameover', '')
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

api.post('/answer/:label/correct', (req, res) => {
  clearInterval(roundTicker)
  updateUI(req.params.label + 'correct', 'CORRECT', res)
})

const parseIntBody = (req, res, next) => {
  req.body = parseInt(req.body)
  next()
}

const scoreChanged = (req, res, next) => {
  updateUI('score', score, res);
  GameEvents.emit('scorechanged')
}

api.post('/score', parseIntBody, (req, res, next) => {
  score = req.body
}, scoreChanged)

api.post('/score/inc', parseIntBody, (req, res, next) => {
  score += req.body
}, scoreChanged)

api.post('/score/dec', parseIntBody, (req, res, next) => {
  score -= req.body
}, scoreChanged)

api.get('/score', (req, res) => {
  res.status(200).send("" + score)
})

ipcMain.once('videoended', (evt, arg) => {
  GameEvents.emit('videoended')
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
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

api.listen(8080, '0.0.0.0')