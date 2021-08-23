########################################################
########################################################

# GUI created by: martinja
# Contact: javier.martinez.samblas@cern.ch

########################################################
########################################################

# COMRAD AND PYQT IMPORTS

from comrad import (CDisplay, PyDMChannelDataSource, CurveData, PointData, PlottingItemData, TimestampMarkerData, TimestampMarkerCollectionData)
from PyQt5.QtGui import (QIcon, QColor)
from PyQt5.QtCore import (QSize, Qt)
import connection_custom

# OTHER IMPORTS

import sys
import os
import time

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
        self.diamond_blm_device_list = ["SP.BA1.BLMDIAMOND.2"]

        # sort the device-list alphabetically
        self.diamond_blm_device_list.sort()

        # other aux variables
        self.current_flags_dict = {"1,2":True, "5,6":True}

        print("Loading fullscreen_rawbuf0 file...")
        super().__init__(*args, **kwargs)
        self.setWindowTitle("rawBuf0")

        # init PyDM channels
        self.pydm_channel_capture_rawbuffer_0 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_0_flags_1_2 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#flags0_one_two", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_0_timestamps = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0_timestamps", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf0)

        # transform timestamps from str to float
        self.pydm_channel_capture_rawbuffer_0_timestamps._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection

        print("Setting initial channels...")
        self.setChannels()

        print("Handling signals and slots...")
        self.bindWidgets()

        return

    #----------------------------------------------#

    # function that initializes signal-slot dependencies
    def bindWidgets(self):

        # checkbox for flags 1 and 2
        self.checkBox_bunch.stateChanged.connect(self.updateFlags_1_2)

        """
        # checkbox for flags 5 and 6
        self.checkBox_turn.stateChanged.connect(self.updateFlags_5_6)
        """

        return

    #----------------------------------------------#

    def updateFlags_1_2(self, state):

        if state == Qt.Checked:

            print('flags (1 and 2) button checked')
            self.current_flags_dict["1,2"] = True
            self.CStaticPlot_Capture_rawBuf0.clear_items()
            if self.current_flags_dict["1,2"]:
                self.CStaticPlot_Capture_rawBuf0.addItem(self.CURVE_pydm_channel_capture_rawbuffer_0_flags_1_2)
            if self.current_flags_dict["5,6"]:
                self.CStaticPlot_Capture_rawBuf0.addItem(self.CURVE_pydm_channel_capture_rawbuffer_0_timestamps)
            self.CStaticPlot_Capture_rawBuf0.addItem(self.CURVE_pydm_channel_capture_rawbuffer_0)
            self.pydm_channel_capture_rawbuffer_0_flags_1_2.context_changed()
            self.pydm_channel_capture_rawbuffer_0_timestamps.context_changed()
            self.pydm_channel_capture_rawbuffer_0.context_changed()

        else:

            print('flags (1 and 2) button unchecked')
            self.current_flags_dict["1,2"] = False
            self.CStaticPlot_Capture_rawBuf0.removeItem(self.CURVE_pydm_channel_capture_rawbuffer_0_flags_1_2)
            self.pydm_channel_capture_rawbuffer_0_flags_1_2.context_changed()
            self.pydm_channel_capture_rawbuffer_0_timestamps.context_changed()
            self.pydm_channel_capture_rawbuffer_0.context_changed()

        return

    """
    def updateFlags_5_6(self, state):

        if state == Qt.Checked:

            print('flags (5 and 6) button checked')
            self.current_flags_dict["5,6"] = True
            self.CStaticPlot_Capture_rawBuf0.clear_items()
            if self.current_flags_dict["1,2"]:
                self.CStaticPlot_Capture_rawBuf0.addItem(self.CURVE_pydm_channel_capture_rawbuffer_0_flags_1_2)
            if self.current_flags_dict["5,6"]:
                self.CStaticPlot_Capture_rawBuf0.addItem(self.CURVE_pydm_channel_capture_rawbuffer_0_timestamps)
            self.CStaticPlot_Capture_rawBuf0.addItem(self.CURVE_pydm_channel_capture_rawbuffer_0)
            self.pydm_channel_capture_rawbuffer_0_flags_1_2.context_changed()
            self.pydm_channel_capture_rawbuffer_0_timestamps.context_changed()
            self.pydm_channel_capture_rawbuffer_0.context_changed()

        else:

            print('flags (5 and 6) button unchecked')
            self.current_flags_dict["5,6"] = False
            self.CStaticPlot_Capture_rawBuf0.removeItem(self.CURVE_pydm_channel_capture_rawbuffer_0_timestamps)
            self.pydm_channel_capture_rawbuffer_0_flags_1_2.context_changed()
            self.pydm_channel_capture_rawbuffer_0_timestamps.context_changed()
            self.pydm_channel_capture_rawbuffer_0.context_changed()

        return
    """

    #----------------------------------------------#

    # function that set the right channels for each widget depending on the selected device
    def setChannels(self):

        # set channels for Capture tab rawBuffer0
        self.CContextFrame_CaptureTab_rawBuf0.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf0.selector = ""
        self.CStaticPlot_Capture_rawBuf0.clear_items()
        self.CURVE_pydm_channel_capture_rawbuffer_0_flags_1_2 = self.CStaticPlot_Capture_rawBuf0.addCurve(data_source=self.pydm_channel_capture_rawbuffer_0_flags_1_2, color=QColor("#EF476F"))
        self.CURVE_pydm_channel_capture_rawbuffer_0_timestamps = self.CStaticPlot_Capture_rawBuf0.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_0_timestamps)
        self.CURVE_pydm_channel_capture_rawbuffer_0 = self.CStaticPlot_Capture_rawBuf0.addCurve(data_source=self.pydm_channel_capture_rawbuffer_0, color=QColor("#FFFFFF"))
        self.pydm_channel_capture_rawbuffer_0_flags_1_2.context_changed()
        self.pydm_channel_capture_rawbuffer_0_timestamps.context_changed()
        self.pydm_channel_capture_rawbuffer_0.context_changed()

        # let's uncheck flags1 and flags2 at the beginning
        self.checkBox_bunch.setChecked(False)
        self.updateFlags_1_2(False)

        return

########################################################
########################################################