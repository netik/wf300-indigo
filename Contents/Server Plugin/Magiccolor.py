#!/usr/bin/python

import sys

# Python class to talk to a WF300 LED Controller
#
# I know little about these devices. They are possibly made by a company called Shenzhi
# Which may actually be LSM Lighting (http://www.lsmledlighting.com/)
#

import os 
import time

from socket import *
from Protocol import * 

class Magiccolor:
  DEBUG = False
  _socket = None
  _ip = "192.168.2.2"
  _port = 5000
  _mode = 0 

  def __init__(self,ip="192.168.2.2",port=5000):
    self._socket = None
    self._ip = ip
    self._port = port
    # mode 3 is SPI Mode
    # TODO: Implement other chips
    self._mode = 3

  def connect(self):
    if self.DEBUG:
      print "connect..." 
      # python >2.6 
#    self._socket = socket.create_connection((self._ip, self._port), 10)
    self._socket = socket(AF_INET, SOCK_STREAM)
    server = ( self._ip, self._port )
    self._socket.connect(server)

    if self.DEBUG:
      print "connected"

  def sendMsg(self,p):
    msg = p.spi_getAll()
    if self.DEBUG:
      x=0
      for b in msg:
        print "%d - %x" % ( x, b )
        x = x + 1
  	# indigo doesn't support bytearray() (old python?) so we're going
  	# to convert int to string here

    msgparts=""
    for m in msg:
      msgparts += chr(m)
    self._socket.send(msgparts)

if __name__ == "__main__":
  m = Magiccolor()
  m.connect()
  p = Protocol()

  # key number 1 turned it on
  # key number 2 turned shit off 
  # key #3 selects mode
  # We don't know how to set speed or brightness.

  if sys.argv[1] == '-l':
    x=0
    y=0
    print "Program listing\n\n"
    for c in p.COLORLIST:
      x=x+1
      if y == 5:
        print 
        y=0
      y=y+1
      
      sys.stdout.write("%02d) %-12s " % (x,c))
    print "\n"
    sys.exit(0)

  if sys.argv[1] == 'pause': 
    p.keyNum=p.MODE_PAUSE
    p.keyValue=1
  elif sys.argv[1] == 'run': 
    p.keyNum=p.MODE_PAUSE
    p.keyValue=0
  elif sys.argv[1] == 'on': 
    p.keyNum=p.MODE_ON
    p.keyValue = p.findProgram('WHITE')
  elif sys.argv[1] == 'off': 
    p.keyNum=p.MODE_OFF
  elif sys.argv[1] == 'speed':
    p.keyNum = p.MODE_SPEED
    try: 
      p.keyValue = int(sys.argv[2])
    except IndexError:
      print 'speed requires a integer 0-100'
      sys.exit(1)
  else:
    if p.findProgram(sys.argv[1]) != None:
      p.keyNum = p.MODE_ON
      p.keyValue = p.findProgram(sys.argv[1])
    else:
      print 'Color/Program name not found'
      sys.exit(1)
  m.sendMsg(p)
