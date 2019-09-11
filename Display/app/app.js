const { ipcRenderer } = require("electron");

const listener = (channel, query, action) => {
  ipcRenderer.on(channel, (evt, arg) => {
    console.log(channel, arg)
    if (!action) {
      document.querySelector(query).innerText = arg;
    }
    else {
      action({
        'channel': channel,
        'query': query,
        'arg': arg
      })
    }
  });
};

const listenerAnswer = label => {
  let q = "#" + label + " #answer";
  listener(label, q);
  listener(label + ".correct", q, opts => {
    var c = document.querySelector('#correct')
    var e = document.querySelector(opts.query)
    c.classList.remove('hidden')
    e.innerText = '((' + e.innerText + '))'
    setTimeout(() => {
      c.classList.add('hidden')
    }, 1500);
  });

  listener(label + ".selected", q, opts => {
    var e = document.querySelector(opts.query)
    e.innerText = "** " + e.innerText + " **"
  })
};

const listenflash = label => {
  ipcRenderer.on(label, (evt, arg) => {
    var e = document.querySelector('#' + label)
    e.classList.remove('hidden')
    setTimeout(() => {
      e.classList.add('hidden')
    }, 2000);
  });
}

listener('question', '#question');
listenerAnswer('red');
listenerAnswer('green');
listenerAnswer('blue');
listenerAnswer('yellow');
listener('score', '#score');
listener('roundtick', '#round_time');
listener('gametick', '#game_time');
listenflash('roundsup')
listenflash('gameover')
listenflash('wrong')
listenflash('player')

listener('player', '#player', opts => {
  var e = document.querySelector('#playername')
  e.innerText = opts.arg
})

var vid = document.querySelector('video')
vid.addEventListener('ended', () => {
  vid.classList.add('hidden')
  ipcRenderer.send('videodone')
})

var aud = document.querySelector('audio')
aud.addEventListener('ended', () => {
  ipcRenderer.send('audiodone')
})

ipcRenderer.on("videoplay", (evt, arg) => {
  vid.src = arg
  vid.classList.remove('hidden')
  vid.load()
  vid.play()
})

ipcRenderer.on("audioplay", (evt, arg) => {
  aud.src = arg
  aud.load()
  aud.play()
})
