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

        return 'fullscreen_rawbuf1.ui'

    #----------------------------------------------#

    # init function
    def __init__(self, *args, **kwargs):

        # set hard-coded device list
        self.diamond_blm_device_list = ["SP.BA1.BLMDIAMOND.2"]

        # sort the device-list alphabetically
        self.diamond_blm_device_list.sort()

        # other aux variables
        self.current_flags_dict = {"1":True, "2":True, "5":True, "6":True}

        print("Loading fullscreen_rawbuf1 file...")
        super().__init__(*args, **kwargs)
        self.setWindowTitle("rawBuf1")

        # init PyDM channels
        self.pydm_channel_capture_rawbuffer_1 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf1)
        self.pydm_channel_capture_rawbuffer_1_flags1 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#flags1_one", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf1)
        self.pydm_channel_capture_rawbuffer_1_flags2 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#flags1_two", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf1)
        self.pydm_channel_capture_rawbuffer_1_timestamps_five = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_timestamps_five", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf1)
        self.pydm_channel_capture_rawbuffer_1_timestamps_six = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_timestamps_six", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf1)

        # transform timestamps from str to float
        self.pydm_channel_capture_rawbuffer_1_timestamps_five._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection
        self.pydm_channel_capture_rawbuffer_1_timestamps_six._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection

        print("Setting initial channels...")
        self.setChannels()

        print("Handling signals and slots...")
        self.bindWidgets()

        return

    #----------------------------------------------#

    # function that initializes signal-slot dependencies
    def bindWidgets(self):

        # checkbox for flag 1
        self.checkBox_one.stateChanged.connect(self.updateFlags1)

        # checkbox for flag 2
        self.checkBox_two.stateChanged.connect(self.updateFlags2)

        # checkbox for flag 5
        #self.checkBox_five.stateChanged.connect(self.updateFlags5)

        # checkbox for flag 6
        #self.checkBox_six.stateChanged.connect(self.updateFlags6)

        return

    # ----------------------------------------------#

    def updateFlags1(self, state):

        if state == Qt.Checked:

            print('flag (1) button checked')
            self.current_flags_dict["1"] = True
            self.CStaticPlot_Capture_rawBuf1.clear_items()
            if self.current_flags_dict["1"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags1)
            if self.current_flags_dict["2"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags2)
            if self.current_flags_dict["5"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_five)
            if self.current_flags_dict["6"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_six)
            self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        else:

            print('flag (1) button unchecked')
            self.current_flags_dict["1"] = False
            self.CStaticPlot_Capture_rawBuf1.removeItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags1)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        return

    def updateFlags2(self, state):

        if state == Qt.Checked:

            print('flag (2) button checked')
            self.current_flags_dict["2"] = True
            self.CStaticPlot_Capture_rawBuf1.clear_items()
            if self.current_flags_dict["1"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags1)
            if self.current_flags_dict["2"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags2)
            if self.current_flags_dict["5"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_five)
            if self.current_flags_dict["6"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_six)
            self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        else:

            print('flag (2) button unchecked')
            self.current_flags_dict["2"] = False
            self.CStaticPlot_Capture_rawBuf1.removeItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags2)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        return

    """
    def updateFlags5(self, state):

        if state == Qt.Checked:

            print('flag (5) button checked')
            self.current_flags_dict["5"] = True
            self.CStaticPlot_Capture_rawBuf1.clear_items()
            if self.current_flags_dict["1"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags1)
            if self.current_flags_dict["2"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags2)
            if self.current_flags_dict["5"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_five)
            if self.current_flags_dict["6"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_six)
            self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        else:

            print('flag (5) button unchecked')
            self.current_flags_dict["5"] = False
            self.CStaticPlot_Capture_rawBuf1.removeItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_five)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        return

    def updateFlags6(self, state):

        if state == Qt.Checked:

            print('flag (6) button checked')
            self.current_flags_dict["6"] = True
            self.CStaticPlot_Capture_rawBuf1.clear_items()
            if self.current_flags_dict["1"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags1)
            if self.current_flags_dict["2"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_flags2)
            if self.current_flags_dict["5"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_five)
            if self.current_flags_dict["6"]:
                self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_six)
            self.CStaticPlot_Capture_rawBuf1.addItem(self.CURVE_pydm_channel_capture_rawbuffer_1)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        else:

            print('flag (6) button unchecked')
            self.current_flags_dict["6"] = False
            self.CStaticPlot_Capture_rawBuf1.removeItem(self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_six)
            self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
            self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
            self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
            self.pydm_channel_capture_rawbuffer_1.context_changed()

        return
    """

    # ----------------------------------------------#

    # function that set the right channels for each widget depending on the selected device
    def setChannels(self):

        # set channels for Capture tab rawBuffer1
        self.CContextFrame_CaptureTab_rawBuf1.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf1.selector = ""
        self.CStaticPlot_Capture_rawBuf1.clear_items()
        self.CURVE_pydm_channel_capture_rawbuffer_1_flags1 = self.CStaticPlot_Capture_rawBuf1.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1_flags1, color=QColor("#06D6A0"))
        self.CURVE_pydm_channel_capture_rawbuffer_1_flags2 = self.CStaticPlot_Capture_rawBuf1.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1_flags2, color=QColor("#EF476F"))
        self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_five = self.CStaticPlot_Capture_rawBuf1.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_1_timestamps_five)
        self.CURVE_pydm_channel_capture_rawbuffer_1_timestamps_six = self.CStaticPlot_Capture_rawBuf1.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_1_timestamps_six)
        self.CURVE_pydm_channel_capture_rawbuffer_1 = self.CStaticPlot_Capture_rawBuf1.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1, color=QColor("#FFFFFF"))
        self.pydm_channel_capture_rawbuffer_1_flags1.context_changed()
        self.pydm_channel_capture_rawbuffer_1_flags2.context_changed()
        self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
        self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()
        self.pydm_channel_capture_rawbuffer_1.context_changed()

        # let's uncheck flags1 and flags2 at the beginning
        self.checkBox_one.setChecked(False)
        self.updateFlags1(False)
        self.checkBox_two.setChecked(False)
        self.updateFlags2(False)

        return

########################################################
########################################################
