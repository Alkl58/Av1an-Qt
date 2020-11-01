# This Python file uses the following encoding: utf-8

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
import sys


class av1angui(QtWidgets.QMainWindow):

    videoInput = None
    videoInputSet = False
    videoOutput = None
    videoOutputSet = False
    aomArguments = None

    def __init__(self):

        super(av1angui, self).__init__()
        pth = os.path.join(os.path.dirname(__file__), "form.ui")  # Set path ui
        uic.loadUi(pth, self)  # Load the .ui file
        self.setFixedWidth(900)  # Set Window Width
        self.setFixedHeight(570)  # Set Window Height
        self.setWindowTitle("Av1an")  # Set Window Title
        self.pushButtonDebuggingTemp.clicked.connect(self.setVideoFilters) # !!!! REMOVE BEFORE RELEASE !!!! !!!! REMOVE BEFORE RELEASE !!!! !!!! REMOVE BEFORE RELEASE !!!!
        self.horizontalSliderQuality.valueChanged.connect(self.UiSliderQuality)
        self.horizontalSliderSpeed.valueChanged.connect(self.UiSliderSpeed)
        self.comboBoxEncoder.currentIndexChanged.connect(self.UiEncoder)
        self.checkBoxAdvancedSettings.stateChanged.connect(self.UiAdvancedSettings)
        self.pushButtonOpenSource.clicked.connect(self.OpenVideoSource)
        self.pushButtonSaveTo.clicked.connect(self.SaveVideoTo)
        self.pushButtonStart.clicked.connect(self.Av1anStartEncode)
        self.comboBoxTuneAom.show()  # Because it is set 'invisible' in .ui file
        self.tabWidget.setTabEnabled(3, False)
        self.AomArgs()
        self.show()  # Show the GUI

    # ══════════════ Dynamic UI Changes ═══════════════
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



    # ═════════════════════════════════════════════════
    # ═══════════════ Button Functions ════════════════
    # Button Open Video Source
    def OpenVideoSource(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Video...", "", "Video File (*.mp4 *.mkv *.webm *.flv *.mpg *.mpeg *.ts *.m2ts *.mov)")
        if fileName: # if fileName is not Null
            self.videoInput = fileName
            self.videoInputSet = True
    # Button Save Video to
    def SaveVideoTo(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Video File", "", "Matroska (*.mkv);; WebM (*.webm)")
        if fileName:
            self.videoOutput = fileName
            self.videoOutputSet = True
    # ═════════════════════════════════════════════════
    # ═════════════════ MessageBoxes ══════════════════
    def showDialog(self, title, text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
    # ═════════════════════════════════════════════════
    # ════════════════ Video Filters ══════════════════
    def setVideoFilters(self):
        crop = self.groupBoxCrop.isChecked() == True
        resize = self.groupBoxScale.isChecked() == True
        deinterlace = self.groupBoxDeinterlace.isChecked() == True
        amountFilters = 0
        filterCommand = None

        if crop: amountFilters += 1
        if resize: amountFilters += 1
        if deinterlace: amountFilters += 1

        if crop or resize or deinterlace:
            tempCounter = 0
            filterCommand = " -vf "
            if crop:
                filterCommand += self.VideoCrop()
                tempCounter += 1
            if deinterlace:
                if tempCounter == 1:
                    filterCommand += ","
                filterCommand += self.VideoDeinterlace()
                tempCounter += 1
            if resize:
                if tempCounter == 1 or tempCounter == 2:
                    filterCommand += ","
                filterCommand += self.VideoResize() # !!! Has to be last, else ffmpeg logic fails

    def VideoCrop(self):
        if self.groupBoxCrop.isChecked() == True:
            widthNew = str(self.spinBoxCropRight.value() + self.spinBoxCropLeft.value())
            heightNew = str(self.spinBoxCropTop.value() + self.spinBoxCropBottom.value())
            return "crop=iw-" + widthNew + ":ih-" + heightNew + ":" + str(self.spinBoxCropLeft.value()) + ":" + str(self.spinBoxCropTop.value())
        else:
            return None  # Needs to be set, else it will crop if in the same instance it was active

    def VideoResize(self):
        if self.groupBoxScale.isChecked() == True:
            return "scale=" + str(self.spinBoxScaleWidth.value()) + ":" + str(self.spinBoxScaleHeight.value()) + " -sws_flags " + self.comboBoxResizeFilters.currentText()
        else:
            return None

    def VideoDeinterlace(self):
        if self.groupBoxDeinterlace.isChecked() == True:
            return "yadif=" + self.comboBoxDeinterlace.currentText()
        else:
            return None
    # ═════════════════════════════════════════════════
    # ══════════════════ AOM Args ═════════════════════

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
            return " error "  # Something bad happened when landing here

    # ═════════════════════════════════════════════════
    # ════════════════ Av1an Entry ════════════════════
    def Av1anStartEncode(self):
        if self.videoInputSet is True and self.videoOutputSet is True:
            self.setVideoFilters()
        else:
            self.showDialog("Attention", "Please set Input and Output!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = av1angui()
    app.exec()
