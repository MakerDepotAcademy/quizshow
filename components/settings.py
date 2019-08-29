import toml

_config = toml.loads('../config.cfg')


class Section():

  def __init__(self, name):
    self._section = _config[name]

  def show(self):
    print(self._section)


class Time(Section):

  def __init__(self):
    Section.__init__(self, 'TIME')
    self.Game_Time = int(self._section['GAME_TIME'])
    self.Round_Time = int(self._section['ROUND_TIME'])
    self.Invite_Sleep = int(self._section['INVITE_SLEEP'])


class BoardStack(Section):

  def __init__(self):
    Section.__init__(self, 'BOARDS')
    self.Board_Stack = [int(i) for i in self._section['BOARD_STACK'].split(',')]
    self.Board_Player_Limit = _config['BOARD_PLAYER_LIMIT']


class Scores(Section):

  def __init__(self):
    Section.__init__(self, 'SCORES')
    self.Inc = int(self._section['INC'])
    self.Dec = int(self._section['DEC'])
    self.Init_Score = int(self._section['INIT'])


class Database(Section):

  def __init__(self):
    Section.__init__(self, 'DATABASE')
    self.URL = self._section['URL']


class Links(Section):

  def __init__(self):
    Section.__init__(self, 'LINKS')
    self.Display_Host = self._section['DISP']
    self.Me = self._section['ME']
    self.Preamble_Video = self._section['PREAMBLE_VID']
    self.Sounds = self._section['AUDIO_FOLDER']