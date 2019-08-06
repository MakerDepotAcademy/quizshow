const { ipcRenderer } = require("electron");

const listener = (channel, query) => {
  ipcRenderer.on(channel, (evt, arg) => {
    document.querySelector(query).innerText = arg;
  });
};

const listenerAnswer = label => {
  let q = "#" + label + " #answer";
  listener(label, q);
  listener(label + "correct", q);
};

listener("question", "#question");
listenerAnswer("a");
listenerAnswer("b");
listenerAnswer("c");
listenerAnswer("d");
listener("score", "#score");
listener("roundtick", "#round_time");
listener("gametick", "#game_time");

ipcRenderer.on("roundsup", (evt, arg) => {
  let el = document.querySelector("#roundsup");
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2000);
});

ipcRenderer.on("gameover", (evt, arg) => {
  document.querySelector("#gameover").classList.remove();
});

var vid = document.querySelector('video')
vid.src = process.env.PREAMBLE_VIDEO
vid.load()
vid.play()
vid.addEventListener('ended', () => {
  vid.classList.add('hidden')
  ipcRenderer.send('videoended')
})