# This Python file uses the following encoding: utf-8

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFileDialog, QMessageBox
# from multiprocessing.dummy import Pool
# from functools import partial
# from subprocess import call
import os
import sys
# import time
# import subprocess
# import asyncio


class av1angui(QtWidgets.QMainWindow):

    def __init__(self):

        super(av1angui, self).__init__()
        pth = os.path.join(os.path.dirname(__file__), "form.ui")  # Set path ui
        uic.loadUi(pth, self)  # Load the .ui file
        self.setFixedWidth(900)  # Set Window Width
        self.setFixedHeight(570)  # Set Window Height
        self.setWindowTitle("Av1an")  # Set Window Title
        self.show()  # Show the GUI


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = av1angui()
    app.exec_()
