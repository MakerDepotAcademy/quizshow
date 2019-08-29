import os

from flask import Flask, request
from threading import Thread

import components.player as Player
import components.questions as Questions
import components.settings as Settings
from components.display import Display, displayQuestion
from components.pause import Pause

Times = Settings.Time()
Links = Settings.Links()
Scores = Settings.Scores()
Scores.score = Scores.Init_Score

disp = Display(Links.Display_Host)
disp.setRoundTimer(Times.Round_Time)
disp.setGameTimer(Times.Game_Time)

def hook_pause(isPaused):
  if isPaused:
    disp.pause()
  else:
    disp.start()

Pause = Pause(hook_pause)

def gameLoop(pc):
  plyrs = Player.assignPlayers(pc)
  Q = Questions.getQuestions()
  P = Player.cyclePlayers(plyrs)
  while True:
    question = next(Q)
    player = next(P)

    Pause.block_if_paused()
    player.flash(Times.Invite_Sleep)

    Pause.block_if_paused()
    question.show()
    displayQuestion(disp, question)

    Pause.block_if_paused()
    disp.start()

    Pause.block_if_paused()
    ans = player.catchAnswer()
    
    if question.checkAnswer(ans):
      disp.setCorrect(ans)
      Scores.score += Scores.Inc
    else:
      disp.doWrong()
      disp.setSelected(ans)
      Scores.score -= Scores.Dec

    disp.setScore(Scores.score)

    Pause.block_if_paused()
    disp.flush()

def gameTimeout():
  # This will nuke threads too, thanks brad
  i = Times.Game_Time
  while i > 0:
    Pause.block_if_paused()
    time.sleep(1)
    i -= 1
    if i == 0:
      os.kill(os.getpid(), signal.SIGUSR1)
      return

gameTimer = Thread(target=gameTimeout)

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def flask_start_game():
  pc = request.form['playerCount']
  t = Thread(target=gameLoop, args=[int(pc)])
  t.start()
  gameTimer.start()
  return 'started'

@app.route('/pause')
def flask_pause_game():
  Pause.pause()
  if Pause.isPaused():
    return 'Game is paused'
  else:
    return 'Game is running'

app.run(host='0.0.0.0', port=5000)