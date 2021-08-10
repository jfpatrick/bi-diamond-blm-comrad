########################################################
########################################################

# GUI created by: martinja
# Contact: javier.martinez.samblas@cern.ch

########################################################
########################################################

# COMRAD AND PYQT IMPORTS

from comrad import (CDisplay, PyDMChannelDataSource, CurveData, PointData, PlottingItemData, TimestampMarkerData)
from PyQt5.QtGui import (QIcon, QColor)
from PyQt5.QtCore import (QSize, Qt)

# OTHER IMPORTS

import sys
import os

########################################################
########################################################

class MyDisplay(CDisplay):

    #----------------------------------------------#

    # function to read the ui file
    def ui_filename(self):

        return 'fullscreen_rawbuf0.ui'

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

        print("Loading fullscreen_rawbuf0 file...")
        super().__init__(*args, **kwargs)

        # init PyDM channels
        self.pydm_channel_capture_rawbuffer_0 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_0_flags1 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#flags0_one", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf0)

        print("Setting initial channels...")
        self.setChannels(i=0)

        self.checkBox_one.stateChanged.connect(self.removeFlags1)

        return

    #----------------------------------------------#

    def removeFlags1(self, state):

        if state == Qt.Checked:

            print('flag (1) button checked')

            self.CStaticPlot_Capture_rawBuf0.clear_items()
            self.CStaticPlot_Capture_rawBuf0.addCurve(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#flags0_one", color="red")
            self.CStaticPlot_Capture_rawBuf0.addCurve(data_source=self.pydm_channel_capture_rawbuffer_0)
            self.pydm_channel_capture_rawbuffer_0_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_0.context_changed()

        else:

            print('flag (1) button unchecked')

            self.CStaticPlot_Capture_rawBuf0.clear_items()
            self.pydm_channel_capture_rawbuffer_0_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_0.context_changed()

        return

    # ----------------------------------------------#

    # function that set the right channels for each widget depending on the selected device
    def setChannels(self, i = 0):

        # read and set the device name from the device list
        self.current_device = self.diamond_blm_device_list[i]

        print("Setting channels for device number {}: {} ".format(i, self.current_device))

        # set channels for Capture tab rawBuffer0
        self.CContextFrame_CaptureTab_rawBuf0.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf0.selector = ""
        self.CStaticPlot_Capture_rawBuf0.clear_items()
        self.CStaticPlot_Capture_rawBuf0.addCurve(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#flags0_one", color="red")
        self.CStaticPlot_Capture_rawBuf0.addCurve(data_source=self.pydm_channel_capture_rawbuffer_0)
        self.pydm_channel_capture_rawbuffer_0_flags1.context_changed()
        self.pydm_channel_capture_rawbuffer_0.context_changed()

        return

########################################################
########################################################
