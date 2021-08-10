########################################################
########################################################

# GUI created by: martinja
# Contact: javier.martinez.samblas@cern.ch

########################################################
########################################################

# COMRAD AND PYQT IMPORTS

from comrad import (CDisplay, PyDMChannelDataSource, CurveData, PointData, PlottingItemData, TimestampMarkerData, TimestampMarkerCollectionData, UpdateSource)
from PyQt5.QtGui import (QIcon, QColor, QGuiApplication)
from PyQt5.QtCore import (QSize, Qt)
import connection_custom

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

        # init PyDM channels
        self.pydm_channel_capture_rawbuffer_0 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_0_FFT = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0_FFT", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf0_FFT)
        self.pydm_channel_capture_rawbuffer_1 = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf1)
        self.pydm_channel_capture_rawbuffer_1_FFT = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_FFT", data_type_to_emit=CurveData, parent=self.CStaticPlot_Capture_rawBuf1_FFT)
        self.pydm_channel_capture_rawbuffer_0_timestamps_five = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0_timestamps_five", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_0_timestamps_six = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0_timestamps_six", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_1_timestamps_five = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_timestamps_five", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf0)
        self.pydm_channel_capture_rawbuffer_1_timestamps_six = PyDMChannelDataSource(channel_address="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_timestamps_six", data_type_to_emit=TimestampMarkerCollectionData, parent=self.CStaticPlot_Capture_rawBuf0)

        # transform timestamps from str to float
        self.pydm_channel_capture_rawbuffer_0_timestamps_five._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection
        self.pydm_channel_capture_rawbuffer_0_timestamps_six._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection
        self.pydm_channel_capture_rawbuffer_1_timestamps_five._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection
        self.pydm_channel_capture_rawbuffer_1_timestamps_six._transform = connection_custom.PlottingItemDataFactory._to_ts_marker_collection

        print("Setting initial channels...")
        self.setChannels(i = 0)

        print("Building the code-only widgets...")
        self.buildCodeWidgets()

        print("Handling signals and slots...")
        self.bindWidgets()

        #self.pushButton.clicked.connect(self.restart)

        return

    #----------------------------------------------#

    def restart(self):

        print("restart")
        EXIT_CODE_REBOOT = -123
        QGuiApplication.exit(EXIT_CODE_REBOOT)

        return

    # ----------------------------------------------#

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

        # set channels for Capture tab rawBuffer0
        self.CContextFrame_CaptureTab_rawBuf0.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf0.selector = ""
        self.CStaticPlot_Capture_rawBuf0.clear_items()
        self.CStaticPlot_Capture_rawBuf0.addCurve(data_source = self.pydm_channel_capture_rawbuffer_0)
        #self.CStaticPlot_Capture_rawBuf0.addTimestampMarker(data_source = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0_timestamps_five")
        #self.CStaticPlot_Capture_rawBuf0.addTimestampMarker(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer0_timestamps_six")
        self.CStaticPlot_Capture_rawBuf0.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_0_timestamps_five)
        self.CStaticPlot_Capture_rawBuf0.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_0_timestamps_six)
        self.pydm_channel_capture_rawbuffer_0.context_changed()
        self.pydm_channel_capture_rawbuffer_0_timestamps_five.context_changed()
        self.pydm_channel_capture_rawbuffer_0_timestamps_six.context_changed()

        # set channels for Capture tab rawBuffer1
        self.CContextFrame_CaptureTab_rawBuf1.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf1.selector = ""
        self.CStaticPlot_Capture_rawBuf1.clear_items()
        self.CStaticPlot_Capture_rawBuf1.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1)
        #self.CStaticPlot_Capture_rawBuf1.addTimestampMarker(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_timestamps_five")
        #self.CStaticPlot_Capture_rawBuf1.addTimestampMarker(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#rawBuffer1_timestamps_six")
        self.CStaticPlot_Capture_rawBuf1.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_1_timestamps_five)
        self.CStaticPlot_Capture_rawBuf1.addTimestampMarker(data_source = self.pydm_channel_capture_rawbuffer_1_timestamps_six)
        self.pydm_channel_capture_rawbuffer_1.context_changed()
        self.pydm_channel_capture_rawbuffer_1_timestamps_five.context_changed()
        self.pydm_channel_capture_rawbuffer_1_timestamps_six.context_changed()

        # set channels for Capture tab rawBuffer0_FFT
        self.CContextFrame_CaptureTab_rawBuf0_FFT.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf0_FFT.selector = ""
        self.CStaticPlot_Capture_rawBuf0_FFT.clear_items()
        self.CStaticPlot_Capture_rawBuf0_FFT.addCurve(data_source=self.pydm_channel_capture_rawbuffer_0_FFT)
        self.CStaticPlot_Capture_rawBuf0_FFT.addCurve(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#peaks_freq0_xplots", color=QColor('yellow'), line_style=Qt.NoPen, symbol="o", symbol_size=8)
        #self.CStaticPlot_Capture_rawBuf1_FFT.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1_FFT_xplots_overtones, color=QColor('yellow'), line_style=Qt.NoPen, symbol="o")
        self.pydm_channel_capture_rawbuffer_0_FFT.context_changed()

        # set channels for Capture tab rawBuffer1_FFT
        self.CContextFrame_CaptureTab_rawBuf1_FFT.inheritSelector = False
        self.CContextFrame_CaptureTab_rawBuf1_FFT.selector = ""
        self.CStaticPlot_Capture_rawBuf1_FFT.clear_items()
        self.CStaticPlot_Capture_rawBuf1_FFT.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1_FFT)
        self.CStaticPlot_Capture_rawBuf1_FFT.addCurve(data_source="rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.diamond_blm_device_list[0] + "/" + "bufferFFT#peaks_freq1_xplots", color=QColor('yellow'), line_style=Qt.NoPen, symbol="o", symbol_size=8)
        #self.CStaticPlot_Capture_rawBuf1_FFT.addCurve(data_source=self.pydm_channel_capture_rawbuffer_1_FFT_xplots_overtones, color=QColor('yellow'), line_style=Qt.NoPen, symbol="o")
        self.pydm_channel_capture_rawbuffer_1_FFT.context_changed()

        # set channels for CLabel overtones of rawbuf0
        self.CContextFrame_CaptureTab_Overtones_FFT0.inheritSelector = False
        self.CContextFrame_CaptureTab_Overtones_FFT0.selector = ""
        self.CLabel_Overtones0_1.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq0"
        self.CLabel_Overtones0_2.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq0"
        self.CLabel_Overtones0_3.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq0"
        self.CLabel_Overtones0_4.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq0"
        self.CLabel_Overtones0_5.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq0"

        # set channels for CLabel overtones of rawbuf1
        self.CContextFrame_CaptureTab_Overtones_FFT1.inheritSelector = False
        self.CContextFrame_CaptureTab_Overtones_FFT1.selector = ""
        self.CLabel_Overtones1_1.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq1"
        self.CLabel_Overtones1_2.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq1"
        self.CLabel_Overtones1_3.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq1"
        self.CLabel_Overtones1_4.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq1"
        self.CLabel_Overtones1_5.channel = "rda3://UCAP-NODE-BI-DIAMOND-BLM/UCAP.VD." + self.current_device + "/" + "bufferFFT#peaks_freq1"

        return

    #----------------------------------------------#

########################################################
########################################################