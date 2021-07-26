########################################################
########################################################

# GUI created by: martinja
# Contact: javier.martinez.samblas@cern.ch

########################################################
########################################################

# COMRAD AND PYQT IMPORTS

from comrad import CDisplay
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QSize)

# OTHER IMPORTS

import sys
import os

########################################################
########################################################

class MyDisplay(CDisplay):

	#----------------------------------------------#

	# function to read the ui file
	def ui_filename(self):

		return 'main.ui'

	#----------------------------------------------#

	# init function
	def __init__(self, *args, **kwargs):

		# set hard-coded device list
		self.diamond_blm_device_list = ["SP.BA1.BLMDIAMOND.2", 
										"SP.BA2.BLMDIAMOND.2",
										"SP.BA4.BLMDIAMOND.2",
										"SP.BA6.BLMDIAMOND.2",
										"SP.UA23.BLMDIAMOND.3",
										"SP.UA87.BLMDIAMOND.3"]

		# sort the device-list alphabetically
		self.diamond_blm_device_list.sort()

		print("Loading UI file...")
		super().__init__(*args, **kwargs)

		print("Setting initial selector...")
		self.current_selector = "SPS.USER.ALL"

		print("Setting initial channels...")
		self.setChannels(i = 0)
		
		print("Building the code-only widgets...")
		self.buildCodeWidgets()

		print("Handling signals and slots...")
		self.bindWidgets()

		return

	#----------------------------------------------#
	
	# function that builds the widgets that weren't initialized using the UI qt designer file
	def buildCodeWidgets(self):

		# comboBox for selecting the device
		self.comboBox_DeviceSelection.addItems(self.diamond_blm_device_list)
		icon_green_tick = QIcon("../icons/green_tick.png")
		icon_red_cross = QIcon("../icons/red_cross.png")
		for index in range(0, len(self.diamond_blm_device_list)):
			self.comboBox_DeviceSelection.setItemIcon(index, icon_green_tick)
			self.comboBox_DeviceSelection.setIconSize(QSize(32, 16))

	#----------------------------------------------#

	# function that initializes signal-slot dependencies
	def bindWidgets(self):

		# comboBox for selecting the device
		self.comboBox_DeviceSelection.currentIndexChanged.connect(self.setChannels)

		return

	#----------------------------------------------#

	# function that set the right channels for each widget depending on the selected device
	def setChannels(self, i = 0):

		# read and set the device name from the device list
		self.current_device = self.diamond_blm_device_list[i]

		print("Setting channels for device number {}: {} ".format(i, self.current_device))

		# set channels for GeneralInformation tab
		self.CLabel_GeneralInformation_AcqStamp.channel = self.current_device + "/" + "GeneralInformation#acqStamp"
		self.CLabel_GeneralInformation_AutoGain.channel = self.current_device + "/" + "GeneralInformation#AutoGain"
		self.CLabel_GeneralInformation_BeamMomentum.channel = self.current_device + "/" + "GeneralInformation#BeamMomentum"
		self.CLabel_GeneralInformation_BoardId.channel = self.current_device + "/" + "GeneralInformation#BoardId"
		self.CLabel_GeneralInformation_BstShift.channel = self.current_device + "/" + "GeneralInformation#BstShift"		
		self.CLabel_GeneralInformation_BunchSample.channel = self.current_device + "/" + "GeneralInformation#BunchSample"
		self.CLabel_GeneralInformation_CycleName.channel = self.current_device + "/" + "GeneralInformation#cycleName"
		self.CLabel_GeneralInformation_CycleStamp.channel = self.current_device + "/" + "GeneralInformation#cycleStamp"
		self.CLabel_GeneralInformation_FpgaCompilation.channel = self.current_device + "/" + "GeneralInformation#FpgaCompilation"
		self.CLabel_GeneralInformation_FpgaFirmware.channel = self.current_device + "/" + "GeneralInformation#FpgaFirmware"
		self.CLabel_GeneralInformation_FpgaStatus.channel = self.current_device + "/" + "GeneralInformation#FpgaStatus"
		self.CLabel_GeneralInformation_MachineId.channel = self.current_device + "/" + "GeneralInformation#MachineId"
		self.CLabel_GeneralInformation_MonitorNames.channel = self.current_device + "/" + "GeneralInformation#monitorNames"
		self.CLabel_GeneralInformation_TurnBc.channel = self.current_device + "/" + "GeneralInformation#TurnBc"
		self.CLabel_GeneralInformation_TurnDropped.channel = self.current_device + "/" + "GeneralInformation#TurnDropped"
		self.CLabel_GeneralInformation_TurnSample.channel = self.current_device + "/" + "GeneralInformation#TurnSample"

		# set channels for GeneralInformation tab
		self.CStaticPlot_Capture_rawBuf0.channel = self.current_device + "/" + "Capture#rawBuf0"
		self.CStaticPlot_Capture_rawBuf1.channel = self.current_device + "/" + "Capture#rawBuf1"

		return

	#----------------------------------------------#

########################################################
########################################################


