#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2012, Perceptive Automation, LLC. All rights reserved.
# http://www.perceptiveautomation.com

import indigo

import os
import sys
import time

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
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	########################################
	def validateDeviceConfigUi(self, valuesDict, typeId, devId):
		return (True, valuesDict)

	########################################
	# Relay / Dimmer Action callback
	######################
	def actionControlDimmerRelay(self, action, dev):
		###### TURN ON ######
		if action.deviceAction == indigo.kDimmerRelayAction.TurnOn:
			# Command hardware module (dev) to turn ON here:
			# ** IMPLEMENT ME **
			sendSuccess = True		# Set to False if it failed.

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
			# ** IMPLEMENT ME **
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s" % (dev.name, "off"))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("onOffState", False)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "off"), isError=True)

		###### TOGGLE ######
		elif action.deviceAction == indigo.kDimmerRelayAction.Toggle:
			# Command hardware module (dev) to toggle here:
			# ** IMPLEMENT ME **
			newOnState = not dev.onState
			sendSuccess = True		# Set to False if it failed.

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
			# ** IMPLEMENT ME **
			newBrightness = action.actionValue
			sendSuccess = True		# Set to False if it failed.

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
			# ** IMPLEMENT ME **
			newBrightness = dev.brightness + action.actionValue
			if newBrightness > 100:
				newBrightness = 100
			sendSuccess = True		# Set to False if it failed.

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
			# ** IMPLEMENT ME **
			newBrightness = dev.brightness - action.actionValue
			if newBrightness < 0:
				newBrightness = 0
			sendSuccess = True		# Set to False if it failed.

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
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "beep request"))

		###### ENERGY UPDATE ######
		elif action.deviceAction == indigo.kDeviceGeneralAction.EnergyUpdate:
			# Request hardware module (dev) for its most recent meter data here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "energy update request"))

		###### ENERGY RESET ######
		elif action.deviceAction == indigo.kDeviceGeneralAction.EnergyReset:
			# Request that the hardware module (dev) reset its accumulative energy usage data here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "energy reset request"))

		###### STATUS REQUEST ######
		elif action.deviceAction == indigo.kDeviceGeneralAction.RequestStatus:
			# Query hardware module (dev) for its current status here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "status request"))

	########################################
	# Custom Plugin Action callbacks (defined in Actions.xml)
	######################
	def setBacklightBrightness(self, pluginAction, dev):
		try:
			newBrightness = int(pluginAction.props.get(u"brightness", 100))
		except ValueError:
			# The int() cast above might fail if the user didn't enter a number:
			indigo.server.log(u"set backlight brightness action to device \"%s\" -- invalid brightness value" % (dev.name,), isError=True)
			return

		# Command hardware module (dev) to set backlight brightness here:
		# ** IMPLEMENT ME **
		sendSuccess = True		# Set to False if it failed.

		if sendSuccess:
			# If success then log that the command was successfully sent.
			indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set backlight brightness", newBrightness))

			# And then tell the Indigo Server to update the state:
			dev.updateStateOnServer("backlightBrightness", newBrightness)
		else:
			# Else log failure but do NOT update state on Indigo Server.
			indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set backlight brightness", newBrightness), isError=True)
