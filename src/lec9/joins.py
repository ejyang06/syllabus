"""
Columbia W4111 
Simple implementations of join algorithms 

  note: these are all poor man's implementations to give a flavor
  of how different join algorithms work.

eugene wu
ewu@cs.columbia.edu
"""
import timeit
from collections import defaultdict
from random import randint, seed
seed(0)

outer = [ [randint(0, 1000), randint(0, 1000)] 
            for i in xrange(100000)]
inner = [ [randint(0, 1000), randint(0, 1000)] 
            for i in xrange(100000)]



def build_index(table):
  """
  given a table (list of (int, int) tuples)
  create an index of
    key -> [rows...]

  """
  index = defaultdict(list)
  for row in table:
    index[row[0]].append(row)
  return index


def nlj(outer, inner):
  """
  Nested Loops Join
  """
  for row in outer:
    for irow in inner:
      if row[0] == irow[0]:
        yield (row, irow)

def inlj(outer, index):
  """
  Indexed Nested Loops Join
  """
  for row in outer:
    for irow in index.get(row[0], []):
      yield (row, irow)


def hinlj(outer, inner):
  """
  poor man's indexed nested loops join 
  includes cost of building hash index on inner
  """
  return inlj(outer, build_index(inner))


def hhj(outer, inner):
  """
  poor man's grace hash join
  """
  return hj(build_index(outer), build_index(inner))

def hj(oindex, iindex):
  """
  roughly Grace Hash Join without building hash indexes
  """
  for outkey in oindex:
    for irow in iindex.get(outkey, []):
      for orow in oindex[outkey]:
        yield (orow, irow)


def smj(outer, inner):
  """
  Sort Merge Join
  """
  # sort
  outer = sorted(outer)
  inner = sorted(inner)

  oread = []
  iread = []

  i, j, p = 0, 0, 0
  while i < len(outer) and j < len(inner):
    irow = inner[p]
    while i < len(outer) and outer[i][0] < irow[0]:
      i += 1
    if i >= len(outer): break

    orow = outer[i]
    while p < len(inner) and orow[0] > inner[p][0]:
      p += 1
    if p >= len(inner): break

    j = p
    while i < len(outer) and p < len(inner) and outer[i][0] == inner[p][0]:
      j = p
      orow = outer[i]
      while j < len(inner) and orow[0] == inner[j][0]:
        yield (orow, inner[j])
        j += 1
      i += 1
    p = j



def test(join_func, outer, inner):
  f = lambda: list(join_func(outer, inner))
  print join_func.__name__, "\t", timeit.timeit(f, number=1)

iindex = build_index(inner)
oindex = build_index(outer)

test(nlj, outer, inner)
test(inlj, outer, iindex)
#test(hinlj, outer, inner)
test(hj, oindex, iindex)
#test(hhj, outer, inner)
test(smj, outer, inner)