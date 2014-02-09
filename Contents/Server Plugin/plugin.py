#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2012, Perceptive Automation, LLC. All rights reserved.
# http://www.perceptiveautomation.com

#
# Note that python version 2.5.6 is in use by Indigo.  
#

import indigo

import os
import sys
import time

from Protocol import * 
from Magiccolor import * 

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
  ########################################
  def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.debug = True

  def __del__(self):
    indigo.PluginBase.__del__(self)

  ########################################
  def startup(self):
    self.debugLog(u"startup called - python version %s " % sys.version)

  def shutdown(self):
    self.debugLog(u"shutdown called")

  ########################################
  def validateDeviceConfigUi(self, valuesDict, typeId, devId):
    return (True, valuesDict)

  ########################################
  # Relay / Dimmer Action callback
  ######################
  def actionControlDimmerRelay(self, action, dev):
    m = Magiccolor()
    m.connect()
    p = Protocol()
    ###### TURN ON ######
    if action.deviceAction == indigo.kDimmerRelayAction.TurnOn:
      # Command hardware module (dev) to turn ON here:
      p.keyNum=p.MODE_ON
      p.keyValue=p.findProgram("WHITE")
      m.sendMsg(p)
      sendSuccess = True    # Set to False if it failed.

      if sendSuccess:
        # If success then log that the command was successfully sent.
        indigo.server.log(u"sent \"%s\" %s" % (dev.name, "on"))

        # And then tell the Indigo Server to update the state.
        dev.updateStateOnServer("onOffState", True)
      else:
        # Else log failure but do NOT update state on Indigo Server.
        indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "on"), isError=True)

    ###### TURN OFF ######
    elif action.deviceAction == indigo.kDimmerRelayAction.TurnOff:
      # Command hardware module (dev) to turn OFF here:
      p.keyNum=p.MODE_OFF
      m.sendMsg(p)
      sendSuccess = True    # Set to False if it failed.

      if sendSuccess:
        # If success then log that the command was successfully sent.
        indigo.server.log(u"sent \"%s\" (%s) %s" % (dev.name, dev.address, "off") )

        # And then tell the Indigo Server to update the state:
        dev.updateStateOnServer("onOffState", False)
      else:
        # Else log failure but do NOT update state on Indigo Server.
        indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "off"), isError=True)

    ###### TOGGLE ######
    elif action.deviceAction == indigo.kDimmerRelayAction.Toggle:
      # Command hardware module (dev) to toggle here:
      newOnState = not dev.onState
      
      if newOnState == False:
        p.keyNum=p.MODE_OFF
      else:
        p.keyNum=p.MODE_ON
        p.keyValue=p.findProgram("WHITE")
      m.sendMsg(p)

      sendSuccess = True    # Set to False if it failed.

      if sendSuccess:
        # If success then log that the command was successfully sent.
        indigo.server.log(u"sent \"%s\" %s" % (dev.name, "toggle"))

        # And then tell the Indigo Server to update the state:
        dev.updateStateOnServer("onOffState", newOnState)
      else:
        # Else log failure but do NOT update state on Indigo Server.
        indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "toggle"), isError=True)

    ###### SET BRIGHTNESS ######
    elif action.deviceAction == indigo.kDimmerRelayAction.SetBrightness:
      # Command hardware module (dev) to set brightness here:
      # 
      # We're kinda lame here. We actually use brightness as a program 
      # so that the slider works. oh well!
      newBrightness = action.actionValue
      p.keyNum=p.MODE_ON
      p.keyValue=newBrightness
      m.sendMsg(p)
      sendSuccess = True    # Set to False if it failed.

      if sendSuccess:
        # If success then log that the command was successfully sent.
        indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set brightness", newBrightness))

        # And then tell the Indigo Server to update the state:
        dev.updateStateOnServer("brightnessLevel", newBrightness)
      else:
        # Else log failure but do NOT update state on Indigo Server.
        indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set brightness", newBrightness), isError=True)

    ###### BRIGHTEN BY ######
    elif action.deviceAction == indigo.kDimmerRelayAction.BrightenBy:
      # Command hardware module (dev) to do a relative brighten here:
      newBrightness = dev.brightness + action.actionValue

      p.keyNum=p.MODE_ON
      p.keyValue=newBrightness
      m.sendMsg(p)

      if newBrightness > 100:
        newBrightness = 100
      sendSuccess = True    # Set to False if it failed.

      if sendSuccess:
        # If success then log that the command was successfully sent.
        indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "brighten", newBrightness))

        # And then tell the Indigo Server to update the state:
        dev.updateStateOnServer("brightnessLevel", newBrightness)
      else:
        # Else log failure but do NOT update state on Indigo Server.
        indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "brighten", newBrightness), isError=True)

    ###### DIM BY ######
    elif action.deviceAction == indigo.kDimmerRelayAction.DimBy:
      # Command hardware module (dev) to do a relative dim here:
      newBrightness = dev.brightness - action.actionValue
      if newBrightness < 0:
        newBrightness = 0

      p.keyNum=p.MODE_ON
      p.keyValue=newBrightness
      m.sendMsg(p)

      sendSuccess = True    # Set to False if it failed.

      if sendSuccess:
        # If success then log that the command was successfully sent.
        indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "dim", newBrightness))

        # And then tell the Indigo Server to update the state:
        dev.updateStateOnServer("brightnessLevel", newBrightness)
      else:
        # Else log failure but do NOT update state on Indigo Server.
        indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "dim", newBrightness), isError=True)

  ########################################
  # General Action callback
  ######################
  def actionControlGeneral(self, action, dev):
    ###### BEEP ######
    if action.deviceAction == indigo.kDeviceGeneralAction.Beep:
      # Beep the hardware module (dev) here:
      indigo.server.log(u"does not support \"%s\" %s" % (dev.name, "beep request"))

    ###### ENERGY UPDATE ######
    elif action.deviceAction == indigo.kDeviceGeneralAction.EnergyUpdate:
      # Request hardware module (dev) for its most recent meter data here:
      indigo.server.log(u"does not support \"%s\" %s" % (dev.name, "energy update request"))

    ###### ENERGY RESET ######
    elif action.deviceAction == indigo.kDeviceGeneralAction.EnergyReset:
      # Request that the hardware module (dev) reset its accumulative energy usage data here:
      indigo.server.log(u"does not support \"%s\" %s" % (dev.name, "energy reset request"))

    ###### STATUS REQUEST ######
    elif action.deviceAction == indigo.kDeviceGeneralAction.RequestStatus:
      # Query hardware module (dev) for its current status here:
      indigo.server.log(u"does not support \"%s\" %s" % (dev.name, "status request"))

  ########################################
  # Custom Plugin Action callbacks (defined in Actions.xml)
  ######################
  def setProgramNumber(self, pluginAction, dev):
    try:
      newValue = int(pluginAction.props.get(u"programNumber", 100))
    except ValueError:
      # The int() cast above might fail if the user didn't enter a number:
      indigo.server.log(u"set program Number to device \"%s\" -- invalid value" % (dev.name), isError=True)
      return

    m = Magiccolor()
    m.connect()
    p = Protocol()
    p.keyNum=p.MODE_ON
    p.keyValue=newValue
    m.sendMsg(p)
    sendSuccess = True    # Set to False if it failed.

    if sendSuccess:
      # If success then log that the command was successfully sent.
      indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set program number", newValue))

      # And then tell the Indigo Server to update the state:
      dev.updateStateOnServer("programNumber", newValue)
    else:
      # Else log failure but do NOT update state on Indigo Server.
      indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set program number", newValue), isError=True)

  def setSpeed(self, pluginAction, dev):
    try:
      newValue = int(pluginAction.props.get(u"speed", 100))
    except ValueError:
      # The int() cast above might fail if the user didn't enter a number:
      indigo.server.log(u"set speed to device \"%s\" -- invalid value" % (dev.name), isError=True)
      return

    m = Magiccolor()
    m.connect()
    p = Protocol()
    p.keyNum=p.MODE_SPEED
    p.keyValue=newValue
    m.sendMsg(p)

    sendSuccess = True    # Set to False if it failed.

    if sendSuccess:
      # If success then log that the command was successfully sent.
      indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set speed", newValue))

      # And then tell the Indigo Server to update the state:
      dev.updateStateOnServer("programNumber", newValue)
    else:
      # Else log failure but do NOT update state on Indigo Server.
      indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set speed", newValue), isError=True)

  def setPause(self, pluginAction, dev):
    newValue = pluginAction.props.get(u"pauseRun", False)

    m = Magiccolor()
    m.connect()
    p = Protocol()
    p.keyNum=p.MODE_PAUSE

    indigo.server.log("%d" % newValue)

    if newValue:
      p.keyValue=1
    else:
      p.keyValue=0

    m.sendMsg(p)
    sendSuccess = True    # Set to False if it failed.

    if sendSuccess:
      # If success then log that the command was successfully sent.
      indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "pause", newValue))

      # And then tell the Indigo Server to update the state:
      dev.updateStateOnServer("pauseRun", newValue)
    else:
      # Else log failure but do NOT update state on Indigo Server.
      indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set pause", newValue), isError=True)
