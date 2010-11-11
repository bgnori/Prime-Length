#!/usr/bin/python
# coding : UTF-8

import random

from bglib.model.board import AbstractBoard
from bglib.model import Board
from bglib.model import BoardEditor
from bglib.encoding.gnubgid import decode, encode
from bglib.model.constants import *
from bglib.model import *

CLEAN = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


class HashableBoard(Board):
  @classmethod
  def freeze(cls, b):
    if not isinstance(b, AbstractBoard):
      raise TypeError
    return HashableBoard(**b._d)

  def __hash__(self):
    pid, mid = encode(self)
    return hash(pid +':'+ mid)


def NewBoard(gnubgid):
  pid, mid = gnubgid.split(':')
  b = BoardEditor()
  decode(b, pid, mid)
  return HashableBoard.freeze(b)
  

def make_finalStatePosition(gnubgid):
  pid, mid = gnubgid.split(':')
  b = BoardEditor()
  decode(b, pid, mid)
  b.position = b.position[0], CLEAN
  return HashableBoard.freeze(b)


class Result:
  def __init__(self, timing, roll):
    self.timing = timing
    self.roll = roll
  def __add__(self, other):
    return Result(self.timing + other.timing, self.roll+ other.roll)

  def add_timing(self, dt):
    self.timing += dt

  def inc_roll(self):
    self.roll +=1


class Trial:
  def __init__(self, position):
    self.board = BoardEditor(position)
    self.result = Result(0, 0)

  def run(self):
    self.board.rolled = random.randint(1, 6), random.randint(1, 6)
    self.result.inc_roll()
    mf = MoveFactory(self.board)
    if mf.is_leagal_to_pickup_dice():
      if self.board.is_doubles():
        self.result.add_timing(self.board.rolled[0] * 4)
      else:
        self.result.add_timing(self.board.rolled[0] + self.board.rolled[1])
      return True
    #print mf

    pid, mid = "2LYBAAAAAAAAAA:cAkgAAAAAAAA".split(':')
    decode(self.board, pid, mid)
    self.board.position = b.position[0], CLEAN
    return False

  def get_position(self):
    return HashableBoard.freeze(self.board)


class State:
  def __init__(self, position, trial, db):
    print "State.__init__"
    print position
    self.tsum = 0.0
    self.rsum = 0.0
    self.tmax = 0
    self.rmax = 0
    self.trial = trial
    self.position = position
    self.results = []
    self.db = db

  def build(self):
    for i in range(self.trial):
      print 'build:start'
      t = Trial(self.position)
      while t.run():
        pass
      p = t.get_position()
      print 'build:end'
      if p not in db:
        print p
        print db
        raise 'postion error'
      r = self.db[p] + t.result

      self.tsum += r.timing
      self.rsum += r.roll
      if self.tmax < r.timing:
        self.tmax = r.timing
      if self.rmax < r.roll:
        self.rmax = r.roll
      self.results.append(r)

  def dump(self, f):
    print >> f, self.tsum/self.trial, self.rsum/self.trial, self.tmax, self.rmax
    for r in self.results: 
      print >> f, r.timing, r.roll
  

class DB:
  def __init__(self):
    self._imp = {}
  
  def __len__(self):
    return len(self._imp)

  def keycheck(self, key):
    if not isinstance(key, HashableBoard):
      raise TypeError

  def __has__(self, key):
    self.keycheck(key)
    return self._imp[key]
  
  def __contains__(self, key):
    self.keycheck(key)
    return key in self._imp
  
  def __setitem__(self, key, value):
    self.keycheck(key)
    self._imp[key] = value

  def __getitem__(self, key):
    self.keycheck(key)
    return self._imp[key]



if __name__ == "__main__":
  from optparse import OptionParser
  import sys

  db = {"2LYBAAAAAAAAAA:cAkgAAAAAAAA": Result(0, 0) }
  assert "2LYBAAAAAAAAAA:cAkgAAAAAAAA" in db
  '''
  position = "2LYBAAAAAAEAAA:cAkgAAAAAAAA" 
  "one checker behind the five prime"

    position = "2LYBAAAAAAMAAA:cAkgAAAAAAAA"
    "two checkers behind the five prime"
  '''

  parser = OptionParser()
  parser.add_option("-n", "--trial", dest="ntrial", help="number of trial for each state, default is 100", default=100, type="int")
  parser.add_option("-o", "--output", dest='output', help="specifies output file", default="data")
  parser.add_option("-q", "--quiet", dest='quiet', help="verboseness", default=False)

  (options, args) = parser.parse_args()
  if not len(args) == 1:
    print "need initial position in gnubgid"
    sys.exit()


  position = args[0]
  if not options.quiet:
    print >>sys.stderr, "using %s as initial position"%(position,)
    print >>sys.stderr, "number of trial is %i"%(options.ntrial,)

  db = DB()
  b = make_finalStatePosition(position)
  db[b] = Result(0, 0)

  b = NewBoard(position)
  state = State(b, options.ntrial, db)
  state.build()
  f = open(options.output, "w")
  state.dump(f)
  f.close()



