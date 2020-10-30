# This Python file uses the following encoding: utf-8

from PyQt5 import QtWidgets, uic
import os
import sys


class av1angui(QtWidgets.QMainWindow):

    aomArguments = ""

    def __init__(self):

        super(av1angui, self).__init__()
        pth = os.path.join(os.path.dirname(__file__), "form.ui")  # Set path ui
        uic.loadUi(pth, self)  # Load the .ui file
        self.setFixedWidth(900)  # Set Window Width
        self.setFixedHeight(570)  # Set Window Height
        self.setWindowTitle("Av1an")  # Set Window Title
        self.horizontalSliderQuality.valueChanged.connect(self.UiSliderQuality)
        self.horizontalSliderSpeed.valueChanged.connect(self.UiSliderSpeed)
        self.comboBoxEncoder.currentIndexChanged.connect(self.UiEncoder)
        self.checkBoxAdvancedSettings.stateChanged.connect(self.UiAdvancedSettings)
        self.comboBoxTuneAom.show()  # Because it is set 'invisible' in .ui file
        self.tabWidget.setTabEnabled(3, False)
        self.AomArgs()
        self.show()  # Show the GUI

    ''' Ui Elements '''
    def UiSliderQuality(self):
        self.labelQuality.setText(str(self.horizontalSliderQuality.value()))

    def UiSliderSpeed(self):
        if self.comboBoxEncoder.currentIndex() != 5 and self.comboBoxEncoder.currentIndex() != 6:
            self.labelSpeed.setText(str(self.horizontalSliderSpeed.value()))
        else:
            currentIndex = self.horizontalSliderSpeed.value()
            textString = ""
            if currentIndex == 0:
                textString = "placebo"
            elif currentIndex == 1:
                textString = "veryslow"
            elif currentIndex == 2:
                textString = "slower"
            elif currentIndex == 3:
                textString = "slow"
            elif currentIndex == 4:
                textString = "medium"
            elif currentIndex == 5:
                textString = "fast"
            elif currentIndex == 6:
                textString = "faster"
            elif currentIndex == 7:
                textString = "veryfast"
            elif currentIndex == 8:
                textString = "superfast"
            elif currentIndex == 9:
                textString = "ultrafast"
            self.labelSpeed.setText(textString)

    def UiAdvancedSettings(self):
        if self.checkBoxAdvancedSettings.isChecked() == True:
            self.tabWidget.setTabEnabled(3, True)
        else:
            self.tabWidget.setTabEnabled(3, False)

    def UiEncoder(self):
        currentIndex = self.comboBoxEncoder.currentIndex()
        if currentIndex == 0:  # aom
            self.horizontalSliderQuality.setValue(30)
            self.horizontalSliderQuality.setMaximum(63)
            self.horizontalSliderSpeed.setValue(4)
            self.horizontalSliderSpeed.setMaximum(9)
            self.comboBoxTuneAom.show()
            self.comboBoxTuneRav1e.hide()
            self.labelEncoderTune.show()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
        elif currentIndex == 1:  # rav1e
            self.horizontalSliderQuality.setMaximum(255)
            self.horizontalSliderQuality.setValue(100)
            self.horizontalSliderSpeed.setValue(6)
            self.horizontalSliderSpeed.setMaximum(10)
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.show()
            self.labelEncoderTune.show()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
        elif currentIndex == 2:  # svt-av1
            self.horizontalSliderQuality.setValue(30)
            self.horizontalSliderQuality.setMaximum(63)
            self.horizontalSliderSpeed.setValue(7)
            self.horizontalSliderSpeed.setMaximum(8)
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()
            self.labelEncoderTune.hide()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
        elif currentIndex == 3:  # svt-vp9
            self.horizontalSliderQuality.setValue(50)
            self.horizontalSliderQuality.setMaximum(63)
            self.horizontalSliderSpeed.setMaximum(9)
            self.horizontalSliderSpeed.setValue(9)
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()
            self.labelEncoderTune.hide()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
        elif currentIndex == 4:  # vpx-vp9
            self.horizontalSliderQuality.setValue(30)
            self.horizontalSliderQuality.setMaximum(63)
            self.horizontalSliderSpeed.setValue(0)
            self.horizontalSliderSpeed.setMaximum(5)
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()
            self.labelEncoderTune.hide()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
        elif currentIndex == 5:  # x265
            self.horizontalSliderQuality.setValue(22)
            self.horizontalSliderQuality.setMaximum(63)
            self.horizontalSliderSpeed.setValue(4)
            self.horizontalSliderSpeed.setMaximum(9)
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()
            self.labelEncoderTune.show()
            self.comboBoxTunex265.show()
            self.comboBoxTunex264.hide()
        elif currentIndex == 6:  # x264
            self.horizontalSliderQuality.setValue(23)
            self.horizontalSliderQuality.setMaximum(51)
            self.horizontalSliderSpeed.setValue(4)
            self.horizontalSliderSpeed.setMaximum(9)
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()
            self.labelEncoderTune.show()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.show()
        elif currentIndex == 7:  # vvc - experimental
            self.labelEncoderTune.hide()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()

    ''' ----------- '''

    ''' aom arg parsing '''
    def AomArgs(self):
        self.aomArguments = ""
        self.aomArguments += " --bit-depth=" + self.comboBoxBitDepth.currentText()   # Bit-Depth
        self.aomArguments += " --cpu-used=" + self.labelSpeed.text()                 # Speed (cpu-used)
        self.aomArguments += self.AomQualityMode()                                   # Quality (Q / Bitrate)
        print(self.aomArguments)

    def AomQualityMode(self):
        if self.radioButtonConstantQ.isChecked() == True:
            return " --end-usage=q --cq-level=" + self.labelQuality.text()
        elif self.radioButtonBitrate.isChecked() == True:
            if self.checkBoxCBR.isChecked() == True:
                return " --end-usage=cbr --target-bitrate=" + str(self.spinBoxBitrate.Value())
            else:
                return " --end-usage=vbr --target-bitrate=" + str(self.spinBoxBitrate.Value())
        else:
            return " am I retarded? "  # Something bad happened when landing here

    ''' --------------- '''

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = av1angui()
    app.exec()
