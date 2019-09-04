require('dotenv').config()

const { app, BrowserWindow, ipcMain } = require('electron')
const fs = require('fs')
const WebSocket = require('ws');

var win
var score = 0, roundTicksLimit = roundTicks = -1, gameTicksLimit = gameTicks = -1, roundTicker, gameTicker

function updateUI(channel, msg, ws) {
  if (win) {
    win.webContents.send(channel, msg);
    console.log('UI', channel, msg)
    return true;
  }
  else {
    ws.send({
      'error': true,
      'msg': 'Display not working'
    })
    console.error('No display')
    return false;
  }
}

const wss = new WebSocket.Server({
  port: 8080,
  host: '0.0.0.0'
}, () => console.log('Listening...'));

wss.on('connection', ws => {
  console.log('Connected')
  ws.on('message', msg => {
    console.log(msg)
    msg = JSON.parse(msg)
    for (let key in msg) {
      updateUI(key, msg[key], ws)
    }
  })
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

