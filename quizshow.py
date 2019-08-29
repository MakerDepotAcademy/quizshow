import components.questions as Questions
import components.player as Player
from components.display import Display, displayQuestion
import components.settings as Settings
from components.pause import Pause


Times = Settings.Time()
Links = Settings.Links()
Scores = Settings.Scores()
Scores.score = Scores.Init_Score

disp = Display(Links.Display_Host)
disp.setRoundTimer(Times.Round_Time)
disp.setGameTimer(Times.Game_Time)

plyrs = Player.assignPlayers(5)

def hook_pause(isPaused):
  pass

Pause = Pause(hook_pause)

for question, player in zip(Questions.getQuestions(), Player.cyclePlayers(plyrs)):
  Pause.block_if_paused()
  player.flash(Times.Invite_Sleep)

  Pause.block_if_paused()
  displayQuestion(disp, question)

  Pause.block_if_paused()
  disp.start()

  Pause.block_if_paused()
  ans = player.catchAnswer()

  Pause.block_if_paused()
  if question.checkAnswer(ans):
    disp.setCorrect(ans)
    Scores.score += Scores.Inc
  else:
    disp.doWrong()
    disp.setSelected(ans)
    Scores.score -= Scores.Dec

  disp.setScore(Scores.score)
  disp.flush()
