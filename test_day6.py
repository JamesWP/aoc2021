import numpy
import collections
import io

def simulate(data, generations):
  data = data.read()
  timers = numpy.array([ int(timer) for timer in data.split(",")])

  for _ in range(generations):
    timers -= 1

    timers_expired = timers < 0
    number_of_expired_timers = numpy.sum(timers_expired)

    timers[timers_expired] = 6
    timers = numpy.append(timers, numpy.full(number_of_expired_timers, 8))

  return timers.shape[0]

def simulate_mk2(data, generations):
  data = data.read()
  timers = collections.Counter([ int(timer) for timer in data.split(",")])

  for _ in range(generations):
    timer_values = dict(timers)
    timers = collections.Counter()
    for timer, count in timer_values.items():
      if timer>0:
        timers[timer-1] += count

      if timer == 0:
        timers[8] += count        
        timers[6] += count

  return sum(count for num,count in timers.items())

def test_part0():
  with open("input6-test.txt", "r") as data:
    assert simulate_mk2(data, 18) == 26
    data.seek(0, io.SEEK_SET)
    assert simulate_mk2(data, 80) == 5934

def test_part1():
  with open("input6.txt", "r") as data:
   assert simulate_mk2(data, 80) == 359344

def test_part00():
  with open("input6-test.txt", "r") as data:
   assert simulate_mk2(data, 256) == 26984457539


def test_part2():
  with open("input6.txt", "r") as data:
    assert simulate_mk2(data, 256) == 1629570219571
