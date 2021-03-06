########################################################
########################################################

# GUI created by: martinja
# Contact: javier.martinez.samblas@cern.ch

########################################################
########################################################

# COMRAD AND PYQT IMPORTS

from comrad import (CDisplay, PyDMChannelDataSource, CurveData, PointData, PlottingItemData, TimestampMarkerData, TimestampMarkerCollectionData, UpdateSource)
from PyQt5.QtGui import (QIcon, QColor, QGuiApplication, QCursor, QStandardItemModel, QStandardItem, QBrush)
from PyQt5.QtCore import (QSize, Qt, QTimer)
from PyQt5.QtWidgets import (QSizePolicy)
from PyQt5.Qt import QItemSelectionModel

# OTHER IMPORTS

import sys
import os
from time import sleep
import pyccda
import pyjapc
import jpype as jp

########################################################
########################################################

# GLOBALS

UI_FILENAME = "premain.ui"

########################################################
########################################################

class MyDisplay(CDisplay):

    #----------------------------------------------#

    # function to read the ui file
    def ui_filename(self):

        return UI_FILENAME

    #----------------------------------------------#

    # init function
    def __init__(self, *args, **kwargs):

        # aux variable for the after-fully-loaded-comrad operations
        self.is_comrad_fully_loaded = False

        # import cern package for handling exceptions
        self.cern = jp.JPackage("cern")

        # setup pyccda to get the device list
        self.pyccda_sync_api = pyccda.SyncAPI()

        # the query instructions are here:
        # https://gitlab.cern.ch/controls-configuration-service/controls-configuration-data-api/accsoft-ccs-ccda/-/blob/dev/accsoft-ccs-pyccda/generator/docs/generate_query_ref.py
        # and the device-query-related instructions here:
        # https://gitlab.cern.ch/controls-configuration-service/controls-configuration-data-api/accsoft-ccs-ccda/-/blob/dev/accsoft-ccs-ccda-client-domain/src/main/java/cern/accsoft/ccs/ccda/client/model/device/query/DeviceQueryField.java

        # query the devices
        self.device_list = []
        for device in self.pyccda_sync_api.Device().search('name=="*BLMDIAMOND*"; deviceClassInfo.name=="*BLMDIAMONDVFC*"; accelerator=="SPS"'):
            self.device_list.append(device.name)

        # add the test device
        if not "dBLM.TEST4" in self.device_list:
            self.device_list.append("dBLM.TEST4")

        # order the device list
        self.device_list.sort()

        # set current device
        self.current_device = ""

        # set the current window
        self.current_window = "premain"

        # set current selector
        my_device = "SPS.USER.SFTPRO1"
        if "dBLM.TEST" not in self.current_device:
            self.current_selector = my_device
        else:
            self.current_selector = ""

        # create japc object
        # self.japc = pyjapc.PyJapc(incaAcceleratorName = None)  # use this line when launching the main application
        self.japc = pyjapc.PyJapc() # use this line when launching the module for debugging

        # set japc selector
        self.japc.setSelector(self.current_selector)

        # get the devices that work
        self.getWorkingDevices()

        # load the gui and set the title,
        print("{} - Loading the GUI file...".format(UI_FILENAME))
        super().__init__(*args, **kwargs)
        self.setWindowTitle("BLM DIAMOND")

        # init main window
        self.CEmbeddedDisplay.filename = ""

        # build the widgets and handle the signals
        print("{} - Building the code-only widgets...".format(UI_FILENAME))
        self.buildCodeWidgets()
        print("{} - Handling signals and slots...".format(UI_FILENAME))
        self.bindWidgets()

        # init the summary
        self.selectAndClickTheRoot()

        # at this point comrad should be fully loaded
        self.is_comrad_fully_loaded = True

        return

    #----------------------------------------------#

    # function that builds the widgets that weren't initialized using the UI qt designer file
    def buildCodeWidgets(self):

        # build the device-list treeview
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)
        self.createTreeFromDeviceList()
        self.treeView.header().hide()
        self.treeView.setUniformRowHeights(True)
        self.treeView.expandAll()

        return

    #----------------------------------------------#

    # function that initializes signal-slot dependencies
    def bindWidgets(self):

        # either shows the preview or the summary whenever an item from the treeview is clicked
        self.treeView.clicked.connect(self.itemFromTreeviewClicked)

        # close main device window when pressing the close toolbutton
        self.toolButton_main_close.clicked.connect(self.closeMain)

        # open settings window (mainly for the getters and setters)
        self.toolButton_main_settings.clicked.connect(self.goToSettingsWindow)

        # back to the last window (which can be preview or main)
        self.toolButton_main_back.clicked.connect(self.backToLastWindow)

        # set up a timer to open the devices when the OPEN DEVICE button is pressed
        self.timer_open_device = QTimer(self)
        self.timer_open_device.setInterval(1000)
        self.timer_open_device.timeout.connect(self.isOpenDevicePushButtonPressed)
        self.timer_open_device.start()

        # set up a timer to HACK comrad after it is fully loaded
        self.timer_hack_operations_after_comrad_is_fully_loaded = QTimer(self)
        self.timer_hack_operations_after_comrad_is_fully_loaded.setInterval(1000)
        self.timer_hack_operations_after_comrad_is_fully_loaded.timeout.connect(self.doOperationsAfterComradIsFullyLoaded)
        self.timer_hack_operations_after_comrad_is_fully_loaded.start()

        return

    #----------------------------------------------#

    # function that checks which devices are properly working and which are not
    def getWorkingDevices(self):

        # declare the working devices list
        self.working_devices = []

        # save the exceptions in a dict
        self.exception_dict = {}

        # iterate over the devices
        for device in self.device_list:

            # print the device for logging and debugging
            print("{} - Checking the availability of {}".format(UI_FILENAME, device))

            # try out if japc returns an error or not
            try:

                # try to acquire the data from pyjapc
                all_data_from_pyjapc = self.japc.getParam("{}/{}".format(device, "Capture"), noPyConversion=False)

            # in case we get an exception, don't add the device to the working list
            except self.cern.japc.core.ParameterException as xcp:

                # ignore in case that the exception was caused by the test device
                if str(device) != "dBLM.TEST4":

                    # print the exception
                    print("{} - Exception: cern.japc.core.ParameterException - {}".format(UI_FILENAME, xcp))
                    print("{} - Device {} is not working...".format(UI_FILENAME, device))

                    # save the exception as xcp
                    self.exception_dict[str(device)] = xcp

                    # continue to the next device
                    continue

            # append the device
            self.working_devices.append(device)

            # save the exception as empty
            self.exception_dict[str(device)] = ""

        return

    #----------------------------------------------#

    # function that adds the items to the tree view
    def createTreeFromDeviceList(self):

        # init row and column counts
        self.model.setRowCount(0)
        self.model.setColumnCount(0)

        # set up the root
        root = QStandardItem("SPS")

        # append items to the root
        for device in self.device_list:

            # define the item to append
            itemToAppend = QStandardItem("{}".format(device))

            # determine the icon (working or not)
            if device in self.working_devices:
                itemToAppend.setIcon(QIcon("../icons/green_tick.png"))
            else:
                itemToAppend.setForeground(QBrush(Qt.red, Qt.SolidPattern))
                itemToAppend.setIcon(QIcon("../icons/red_cross.png"))

            # append it to the tree
            root.appendRow(itemToAppend)

        # append the root to the model
        self.model.appendRow(root)

        # get the index of the root (THIS HAS TO BE THE LAST LINE OF CODE AFTER THE TREE IS CREATED SO THAT THE INDEX ACTUALLY POINTS TO THE RIGHT ELEMENT OF THE TREE)
        self.index_of_the_root = root.index()

        return

    #----------------------------------------------#

    # function that selects and clicks the root (e.g. SPS) to init the summary
    def selectAndClickTheRoot(self):

        # initialize the summary by selecting and clicking the root
        self.treeView.selectionModel().select(self.index_of_the_root, QItemSelectionModel.Select)
        self.itemFromTreeviewClicked(self.index_of_the_root)

        return

    #----------------------------------------------#

    # function that shows the device preview when a device is clicked
    def itemFromTreeviewClicked(self, index):

        # read the name of the device
        item = self.treeView.selectedIndexes()[0]
        selected_text = str(item.model().itemFromIndex(index).text())
        print("{} - Clicked from treeView: {}".format(UI_FILENAME, selected_text))

        # if the item IS NOT the root, then show the preview
        if selected_text != "SPS" and selected_text != "LHC":

            # get the parent (cycle) text (e.g. LHC or SPS)
            parent_text = str(item.model().itemFromIndex(index).parent().text())

            # update the current device
            self.current_device = selected_text
            self.writeDeviceIntoTxtForMainScreen()

            # update text label
            if self.current_device in self.working_devices:
                self.label_device_panel.setText("DEVICE PANEL <font color=green>{}</font> : <font color=green>{}</font>".format(parent_text, self.current_device))
            else:
                self.label_device_panel.setText( "DEVICE PANEL <font color=red>{}</font> : <font color=red>{}</font>".format(parent_text, self.current_device))

            # open main container
            self.CEmbeddedDisplay.filename = ""
            self.CEmbeddedDisplay.hide()
            self.CEmbeddedDisplay.show()
            self.CEmbeddedDisplay.filename = "preview_one_device.py"
            self.CEmbeddedDisplay.open_file(force=True)

            # enable tool buttons
            self.toolButton_main_settings.setEnabled(False)
            self.toolButton_main_close.setEnabled(True)
            self.toolButton_main_back.setEnabled(False)

            # update the current window
            self.current_window = "preview"

        # if the item IS the root, then show the summary
        else:

            # send and write the device list
            self.writeDeviceListIntoTxtForSummary()

            # update text label
            self.label_device_panel.setText("DEVICE PANEL <font color=green>{}</font> : <font color=green>{}</font>".format(selected_text, "SUMMARY"))

            # open main container
            self.CEmbeddedDisplay.filename = ""
            self.CEmbeddedDisplay.hide()
            self.CEmbeddedDisplay.show()
            self.CEmbeddedDisplay.filename = "preview_summary.py"
            self.CEmbeddedDisplay.open_file(force=True)

            # enable tool buttons
            self.toolButton_main_settings.setEnabled(False)
            self.toolButton_main_close.setEnabled(True)
            self.toolButton_main_back.setEnabled(False)

            # update the current window
            self.current_window = "summary"

    #----------------------------------------------#

    # function that closes the main device window
    def closeMain(self):

        # print the action
        print("{} - Button CLOSE pressed".format(UI_FILENAME))

        # close main container
        if self.CEmbeddedDisplay.filename != "":

            # update main panel
            self.CEmbeddedDisplay.filename = ""
            self.CEmbeddedDisplay.hide()
            self.CEmbeddedDisplay.show()

            # update text label
            self.label_device_panel.setText("DEVICE PANEL <font color=red>{}</font> : <font color=red>{}</font>".format("NO CYCLE SELECTED", "NO DEVICE SELECTED"))

            # disable tool buttons
            self.toolButton_main_settings.setEnabled(False)
            self.toolButton_main_close.setEnabled(False)
            self.toolButton_main_back.setEnabled(False)

            # update the current window
            self.current_window = "premain"

        return

    #----------------------------------------------#

    # function that opens the settings window that shows the different configurable parameters of the device
    def goToSettingsWindow(self):

        # print the action
        print("{} - Button SETTINGS pressed".format(UI_FILENAME))

        # open settings window
        if self.CEmbeddedDisplay.filename != "":

            # update main panel
            self.CEmbeddedDisplay.filename = ""
            self.CEmbeddedDisplay.hide()
            self.CEmbeddedDisplay.show()
            self.CEmbeddedDisplay.filename = "settings_dialog_auto.py"
            self.CEmbeddedDisplay.open_file(force=True)

            # disable and enable tool buttons
            self.toolButton_main_settings.setEnabled(False)
            self.toolButton_main_close.setEnabled(True)
            self.toolButton_main_back.setEnabled(True)

            # update the current window
            self.current_window = "settings"

    #----------------------------------------------#

    # function that re-opens the last window
    def backToLastWindow(self):

        # print the action
        print("{} - Button BACK pressed".format(UI_FILENAME))

        # if you were in settings, go back to main
        if self.current_window == "settings":

            # check you are not in premain
            if self.CEmbeddedDisplay.filename != "":

                # update main panel
                self.CEmbeddedDisplay.filename = ""
                self.CEmbeddedDisplay.hide()
                self.CEmbeddedDisplay.show()
                self.CEmbeddedDisplay.filename = "main_auto.py"
                self.CEmbeddedDisplay.open_file(force=True)

                # disable and enable tool buttons
                self.toolButton_main_settings.setEnabled(True)
                self.toolButton_main_close.setEnabled(True)
                self.toolButton_main_back.setEnabled(True)

                # update the current window
                self.current_window = "main"

        # if you were in main, go back to preview
        elif self.current_window == "main":

            # check you are not in premain
            if self.CEmbeddedDisplay.filename != "":

                # update main panel
                self.CEmbeddedDisplay.filename = ""
                self.CEmbeddedDisplay.hide()
                self.CEmbeddedDisplay.show()
                self.CEmbeddedDisplay.filename = "preview_one_device.py"
                self.CEmbeddedDisplay.open_file(force=True)

                # disable and enable tool buttons
                self.toolButton_main_settings.setEnabled(False)
                self.toolButton_main_close.setEnabled(True)
                self.toolButton_main_back.setEnabled(False)

                # update the current window
                self.current_window = "preview"

        return

    #----------------------------------------------#

    # function that checks if the OPEN DEVICE button was pressed and open the device in case it was
    def isOpenDevicePushButtonPressed(self):

        # init the boolean
        wasTheButtonPressed = "False"

        # read the txt file
        if os.path.exists("aux_txts/open_new_device.txt"):
            with open("aux_txts/open_new_device.txt", "r") as f:
                wasTheButtonPressed = f.read()
                if wasTheButtonPressed == "True":
                    with open("aux_txts/open_new_device.txt", "w") as f:
                        f.write("False")

        # if the button was pressed then open the device panel
        if wasTheButtonPressed == "True":

            # open main container
            self.CEmbeddedDisplay.filename = ""
            self.CEmbeddedDisplay.hide()
            self.CEmbeddedDisplay.show()
            self.CEmbeddedDisplay.filename = "main_auto.py"
            self.CEmbeddedDisplay.open_file(force=True)

            # enable tool buttons
            self.toolButton_main_settings.setEnabled(True)
            self.toolButton_main_close.setEnabled(True)
            self.toolButton_main_back.setEnabled(True)

            # update the current window
            self.current_window = "main"

        return

    #----------------------------------------------#

    # function that writes the device name into a txt file
    def writeDeviceIntoTxtForMainScreen(self):

        # create the dir in case it does not exist
        if not os.path.exists("aux_txts"):
            os.mkdir("aux_txts")

        # write the current device
        with open("aux_txts/current_device_premain.txt", "w") as f:
            f.write(str(self.current_device))

        # write the exception of the current device
        with open("aux_txts/exception_premain.txt", "w") as f:
            f.write("{}\n".format(self.exception_dict[str(self.current_device)]))

        return

    #----------------------------------------------#

    # function that writes the device list into a txt so that the summary python file can read it
    def writeDeviceListIntoTxtForSummary(self):

        # create the dir in case it does not exist
        if not os.path.exists("aux_txts"):
            os.mkdir("aux_txts")

        # write the file: device_list_premain
        with open("aux_txts/device_list_premain.txt", "w") as f:
            for dev in self.device_list:
                f.write("{}\n".format(dev))

        # write the file: working_devices_premain
        with open("aux_txts/working_devices_premain.txt", "w") as f:
            for dev in self.working_devices:
                f.write("{}\n".format(dev))

        return

    #----------------------------------------------#

    # function that does all operations that are required after comrad is fully loaded
    def doOperationsAfterComradIsFullyLoaded(self):

        # click the root and stop the timer when comrad is fully loaded
        if self.is_comrad_fully_loaded:
            self.selectAndClickTheRoot()
            self.timer_hack_operations_after_comrad_is_fully_loaded.stop()

        return

    #----------------------------------------------#

########################################################
########################################################