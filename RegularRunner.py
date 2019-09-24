import datetime, threading, time
import sys, os
import random 

next_call = time.time()
variable = 5.0

def RandomMovement():
  increment = (random.randint(1,200) - 100.0) / 100.0
  return increment

def DoIt():
  global next_call
  global variable
  increment = RandomMovement()
  variable = variable + increment
  print datetime.datetime.now(), variable, increment
  next_call = next_call + 1
  threading.Timer( next_call - time.time(), DoIt ).start()
#  os.system("date")

DoIt()