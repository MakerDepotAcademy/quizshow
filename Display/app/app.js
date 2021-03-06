const { ipcRenderer } = require("electron");

const listener = (channel, query, action) => {
  ipcRenderer.on(channel, (evt, arg) => {
    console.log([channel, arg])
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
  listener(label + "-correct", q);
  listener(label + "-selected", q, opts => {
    let t = document.querySelector(opts.query).innerText
    document.querySelector(opts.query).innerText = "** " + t + " **"
  })
};

listener("question", "#question");
listenerAnswer("red");
listenerAnswer("green");
listenerAnswer("blue");
listenerAnswer("yellow");
listener("score", "#score");
listener("roundtick", "#round_time");
listener("gametick", "#game_time");

ipcRenderer.on("roundsup", (evt, arg) => {
  let el = document.querySelector("#roundsup");
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2000);
});

ipcRenderer.on("gameover", (evt, arg) => {
  document.querySelector("#gameover").classList.remove("hidden");
});

ipcRenderer.on("wrong", (evt, arg) => {
  let el = document.querySelector("#wrong");
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 1500);
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
