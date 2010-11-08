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

def find_move(position, rolled):
  '''
    Returns (position, delta_timing)
  '''
  b = BoardEditor()
  pid, mid = position.split(':')
  decode(b, pid, mid)
  b.game_state = ON_GOING
  b.rolled = rolled
  #print b
  mf = MoveFactory(b)
  if mf.is_leagal_to_pickup_dice():
    if rolled[0] == rolled[1]:
      dt = rolled[0] * 4
    else:
      dt = rolled[0]+rolled[1]
    return position, dt
  return "2LYBAAAAAAAAAA:cAkgAAAAAAAA", 0






results = []
db = {"2LYBAAAAAAAAAA:cAkgAAAAAAAA": Result(0, 0) }

assert "2LYBAAAAAAAAAA:cAkgAAAAAAAA" in db

Ntrial = 100000
for i in range(Ntrial):
  position = "2LYBAAAAAAEAAA:cAkgAAAAAAAA" 
  "one checker behind the five prime"

  '''
    position = "2LYBAAAAAAMAAA:cAkgAAAAAAAA"
    "two checkers behind the five prime"
  '''
  timing = 0
  c = 0
  while True:
    r = random.randint(1, 6), random.randint(1, 6)
    c += 1
    next, dt = find_move(position, r)
    if position == next:
      timing += dt
      print 'dt is', dt
      continue
    position = next
    if position not in db:
      raise 'postion error'
    results.append(Result(db[position].timing + timing, db[position].roll + c))
    break

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
  


