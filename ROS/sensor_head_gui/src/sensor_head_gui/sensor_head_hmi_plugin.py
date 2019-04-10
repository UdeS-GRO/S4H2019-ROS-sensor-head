import os
import rospkg
import rospy
import rosnode
from rospkg import RosPack
from qt_gui.plugin import Plugin
import subprocess
from python_qt_binding import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets

from .sensor_head_hmi import SensorHeadHMIWidget


class SensorHeadGUI(Plugin):
    """
        Application window controller
    """

    def __init__(self, context):
        super(SensorHeadGUI, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('SensorHeadGUI')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print('arguments: ', args)
            print('unknowns: ', unknowns)

        # Create QWidget
        self._widget = SensorHeadHMIWidget()
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() +
                                        (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

