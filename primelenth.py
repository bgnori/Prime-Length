#!/usr/bin/python
# coding : UTF-8

import random

from bglib.model import BoardEditor
from bglib.encoding.gnubgid import decode, encode
from bglib.model.constants import *
from bglib.model import *


class Result:
  def __init__(self, timing, roll):
    self.timing = timing
    self.roll = roll
  def __add__(self, other):
    return Result(self.timing + other.timing, self.roll+ other.roll)



class Trial:
  def __init__(self, initial):
    self.position = initial
    self.board = BoardEditor()
    self.board.game_state = ON_GOING
    self.result = Result(0, 0)
    self.rolled = (0, 0)

  def roll(self):
    self.rolled = random.randint(1, 6), random.randint(1, 6)
    self.result.roll += 1

  def find_move(self):
    '''
      Returns (position, delta_timing)
    '''
    pid, mid = self.position.split(':')
    decode(self.board, pid, mid)
    self.board.rolled = self.rolled
    mf = MoveFactory(self.board)
    if mf.is_leagal_to_pickup_dice():
      if self.rolled[0] == self.rolled[1]:
        dt = self.rolled[0] * 4
      else:
        dt = self.rolled[0] + self.rolled[1]
      return position, dt
    return "2LYBAAAAAAAAAA:cAkgAAAAAAAA", 0

  def iterate(self):
    self.roll()
    next, dt = self.find_move()
    if self.position == next:
      self.result.timing += dt
      return True
    self.position = next
    return False




results = []
db = {"2LYBAAAAAAAAAA:cAkgAAAAAAAA": Result(0, 0) }

assert "2LYBAAAAAAAAAA:cAkgAAAAAAAA" in db

Ntrial = 1000000
for i in range(Ntrial):
  position = "2LYBAAAAAAEAAA:cAkgAAAAAAAA" 
  "one checker behind the five prime"

  '''
    position = "2LYBAAAAAAMAAA:cAkgAAAAAAAA"
    "two checkers behind the five prime"
  '''
  t = Trial(position)
  while t.iterate():
    pass
  if t.position not in db:
    raise 'postion error'
  results.append(db[t.position] + t.result)

f = open('stat', 'w')

tsum = 0.0
rsum = 0.0
tmax = 0
rmax = 0
for r in results:
  tsum += r.timing
  rsum += r.roll
  if tmax < r.timing:
    tmax = r.timing
  if rmax < r.roll:
    rmax = r.roll
  print >> f, r.timing, r.roll
print >> f, tsum/Ntrial, rsum/Ntrial, tmax, rmax
f.close()
  


