########################################################
########################################################

# GUI created by: martinja
# Contact: javier.martinez.samblas@cern.ch

########################################################
########################################################

# COMRAD AND PYQT IMPORTS

from comrad import (CLineEdit, CCommandButton, CLabel, CDisplay, PyDMChannelDataSource, CurveData, PointData, PlottingItemData, TimestampMarkerData, TimestampMarkerCollectionData, UpdateSource)
from PyQt5.QtGui import (QIcon, QColor, QGuiApplication, QCursor, QStandardItemModel, QStandardItem, QFont)
from PyQt5.QtCore import (QSize, Qt, QRect)
from PyQt5.QtWidgets import (QSizePolicy, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, QScrollArea, QSpacerItem, QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QDialog, QFrame, QWidget)
import connection_custom
import pyjapc

# OTHER IMPORTS

import sys
import os
from time import sleep

########################################################
########################################################

# GLOBALS

UI_FILENAME = "preview_one_device.ui"

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

        # set the device
        self.current_device = "dBLM.TEST4"
        self.LoadDeviceFromTxtPremain()

        # input the property list
        self.field_list = ["BoardId", "FpgaStatus", "MachineId", "monitorNames"]

        # order the property list
        self.field_list.sort()

        # create japc object
        # self.japc = pyjapc.PyJapc(incaAcceleratorName = None) # use this line when launching the main application
        self.japc = pyjapc.PyJapc() # use this line when launching the module for debugging

        # set japc selector
        self.japc.setSelector("")

        # load the gui, build the widgets and handle the signals
        print("{} - Loading the GUI file...".format(UI_FILENAME))
        super().__init__(*args, **kwargs)
        self.setWindowTitle("BLM DIAMOND SETTINGS")
        print("{} - Building the code-only widgets...".format(UI_FILENAME))
        self.buildCodeWidgets()
        print("{} - Handling signals and slots...".format(UI_FILENAME))
        self.bindWidgets()

        return

    #----------------------------------------------#

    # function that builds the widgets that weren't initialized using the UI qt designer file
    def buildCodeWidgets(self):

        # initialize widget dicts
        self.layoutDict = {}
        self.labelDict = {}

        # create the main widget
        self.main_widget = QWidget(self.scrollingContents_properties)
        self.main_widget.setObjectName("main_widget")

        # widget layout
        self.layoutDict["grid_layout_main_widget"] = QGridLayout(self.main_widget)
        self.layoutDict["grid_layout_main_widget"].setObjectName("grid_layout_main_widget")

        # get field values via pyjapc
        field_values = self.japc.getParam("{}/{}".format(self.current_device, "GeneralInformation"))

        # top spacer
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_scrollingContents_properties.addItem(spacer_top)

        # add the top title labels (the first row of the table)
        row = 0

        # set fields label (column == 0)
        column = 0
        self.labelDict["{}_{}".format("main_widget", "title_fields")] = QLabel(self.main_widget)
        self.labelDict["{}_{}".format("main_widget", "title_fields")].setObjectName("label_{}_{}".format("main_widget", "title_fields"))
        self.labelDict["{}_{}".format("main_widget", "title_fields")].setMinimumSize(QSize(0, 32))
        self.labelDict["{}_{}".format("main_widget", "title_fields")].setAlignment(Qt.AlignCenter)
        self.labelDict["{}_{}".format("main_widget", "title_fields")].setText("{}".format("Fields"))
        self.labelDict["{}_{}".format("main_widget", "title_fields")].setStyleSheet("background-color: rgb(220, 220, 220);")
        self.layoutDict["grid_layout_main_widget"].addWidget(self.labelDict["{}_{}".format("main_widget", "title_fields")], row, column, 1, 1)

        # set values label (column == 1)
        column = 1
        self.labelDict["{}_{}".format("main_widget", "title_values")] = QLabel(self.main_widget)
        self.labelDict["{}_{}".format("main_widget", "title_values")].setObjectName("label_{}_{}".format("main_widget", "title_values"))
        self.labelDict["{}_{}".format("main_widget", "title_values")].setMinimumSize(QSize(0, 32))
        self.labelDict["{}_{}".format("main_widget", "title_values")].setAlignment(Qt.AlignCenter)
        self.labelDict["{}_{}".format("main_widget", "title_values")].setText("{}".format("Values"))
        self.labelDict["{}_{}".format("main_widget", "title_values")].setStyleSheet("background-color: rgb(220, 220, 220);")
        self.layoutDict["grid_layout_main_widget"].addWidget(self.labelDict["{}_{}".format("main_widget", "title_values")], row, column, 1, 1)

        # add labels to the layout of the widget
        row = 1
        for field in self.field_list:

            # if the field is monitorNames, process the string a little bit for the sake of aesthetics
            if field == "monitorNames":
                final_field_value = ""
                new_val = list(dict.fromkeys(field_values[field]))
                for i in range(0, len(new_val)):
                    string = new_val[i]
                    if i > 0:
                        final_field_value = final_field_value + ", " + string
                    else:
                        final_field_value = string
                final_field_value = "  {}  ".format(final_field_value)

            # just use the default field value
            else:
                final_field_value = field_values[field]

            # set label (column == 0)
            column = 0
            self.labelDict["label_name_{}_{}".format("main_widget", field)] = QLabel(self.main_widget)
            self.labelDict["label_name_{}_{}".format("main_widget", field)].setObjectName("label_name_{}_{}".format("main_widget", field))
            self.labelDict["label_name_{}_{}".format("main_widget", field)].setAlignment(Qt.AlignCenter)
            self.labelDict["label_name_{}_{}".format("main_widget", field)].setText("{}".format(field))
            self.labelDict["label_name_{}_{}".format("main_widget", field)].setMinimumSize(QSize(120, 32))
            self.layoutDict["grid_layout_main_widget"].addWidget(self.labelDict["label_name_{}_{}".format("main_widget", field)], row, column, 1, 1)

            # set label (column == 1)
            column = 1
            self.labelDict["label_value_{}_{}".format("main_widget", field)] = QLabel(self.main_widget)
            self.labelDict["label_value_{}_{}".format("main_widget", field)].setObjectName("label_value_{}_{}".format("main_widget", field))
            self.labelDict["label_value_{}_{}".format("main_widget", field)].setAlignment(Qt.AlignCenter)
            self.labelDict["label_value_{}_{}".format("main_widget", field)].setText("{}".format(final_field_value))
            self.labelDict["label_value_{}_{}".format("main_widget", field)].setMinimumSize(QSize(120, 32))
            self.layoutDict["grid_layout_main_widget"].addWidget(self.labelDict["label_value_{}_{}".format("main_widget", field)], row, column, 1, 1)

            # get the next field
            row += 1

        # add the widget to the scrolling layout
        self.verticalLayout_scrollingContents_properties.addWidget(self.main_widget)

        # bottom spacer
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_scrollingContents_properties.addItem(spacer_bottom)

        # set minimum dimensions for the main window according to the auto generated table
        self.setMinimumWidth(self.scrollArea_properties.sizeHint().width() * 2.5)
        self.setMinimumHeight(self.scrollArea_properties.sizeHint().height() * 1)

        # make the scroll bar of the get and set panel invisible
        sp_scroll_area_get_set = self.scrollArea_get_set.verticalScrollBar().sizePolicy()
        sp_scroll_area_get_set.setRetainSizeWhenHidden(True)
        self.scrollArea_get_set.verticalScrollBar().setSizePolicy(sp_scroll_area_get_set)
        self.scrollArea_get_set.verticalScrollBar().hide()

        return

    #----------------------------------------------#

    # function that initializes signal-slot dependencies
    def bindWidgets(self):

        # new device binding
        self.pushButton_set.clicked.connect(self.openNewDevice)

        return

    #----------------------------------------------#

    # function that overwrites the txt file so that the premain.py can open the new device panel
    def openNewDevice(self):

        # print the OPEN DEVICE action
        print("{} - Button OPEN DEVICE pressed".format(UI_FILENAME))

        # create the dir in case it does not exist
        if not os.path.exists("aux_txts"):
            os.mkdir("aux_txts")

        # write the file
        with open("aux_txts/open_new_device.txt", "w") as f:
            f.write("True")

        return

    #----------------------------------------------#

    # function that loads the device from the aux txt file
    def LoadDeviceFromTxtPremain(self):

        if os.path.exists("aux_txts/current_device_premain.txt"):
            with open("aux_txts/current_device_premain.txt", "r") as f:
                self.current_device = f.read()

        return

    #----------------------------------------------#

########################################################
########################################################