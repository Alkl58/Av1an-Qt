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
    rav1eArguments = None
    svtav1Arguments = None

    def __init__(self):

        super(av1angui, self).__init__()
        pth = os.path.join(os.path.dirname(__file__), "form.ui")  # Set path ui
        uic.loadUi(pth, self)  # Load the .ui file
        self.setFixedWidth(900)  # Set Window Width
        self.setFixedHeight(580)  # Set Window Height
        self.setWindowTitle("Av1an-Qt")  # Set Window Title
        self.pushButtonDebuggingTemp.clicked.connect(self.SvtAV1Args) # !!!! REMOVE BEFORE RELEASE
        self.horizontalSliderQuality.valueChanged.connect(self.UiSliderQuality)
        self.horizontalSliderSpeed.valueChanged.connect(self.UiSliderSpeed)
        self.comboBoxEncoder.currentIndexChanged.connect(self.UiEncoder)
        self.checkBoxAdvancedSettings.stateChanged.connect(self.UiAdvancedSettings)
        self.groupBoxCustomSettings.clicked.connect(self.UiCustomSettings)
        self.pushButtonOpenSource.clicked.connect(self.OpenVideoSource)
        self.pushButtonSaveTo.clicked.connect(self.SaveVideoTo)
        self.pushButtonStart.clicked.connect(self.Av1anStartEncode)
        self.comboBoxTuneAom.show()  # Because it is set 'invisible' in .ui file
        self.groupBoxAomSettings.show()  # Because it is set 'invisible' in .ui file
        self.groupBoxSVTAV1Settings.hide()  # to-do: hide in ui file
        self.tabWidget.setTabEnabled(4, False)
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
            self.tabWidget.setTabEnabled(4, True)
        else:
            self.tabWidget.setTabEnabled(4, False)

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
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.hide()
            self.groupBoxAomSettings.show()
            self.checkBoxCBR.show()            
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
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.show()
            self.groupBoxSVTAV1Settings.hide()
            self.checkBoxCBR.hide()
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
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.show()
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
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.hide()
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
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.hide()
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
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.hide()
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
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.hide()
        elif currentIndex == 7:  # vvc - experimental
            self.labelEncoderTune.hide()
            self.comboBoxTunex265.hide()
            self.comboBoxTunex264.hide()
            self.comboBoxTuneAom.hide()
            self.comboBoxTuneRav1e.hide()
            self.groupBoxAomSettings.hide()
            self.groupBoxRav1eSettings.hide()
            self.groupBoxSVTAV1Settings.hide()

    def UiCustomSettings(self):
        if self.groupBoxCustomSettings.isChecked() == True:
            currentIndex = self.comboBoxEncoder.currentIndex()
            if currentIndex == 0:   # aom
                self.AomArgs()
                self.textEditCustomSettings.setText(self.aomArguments)
                self.groupBoxAomSettings.setEnabled(False)
            if currentIndex == 1:
                self.Rav1eArgs()
                self.textEditCustomSettings.setText(self.rav1eArguments)
                self.groupBoxRav1eSettings.setEnabled(False)
            if currentIndex == 2:
                self.SvtAV1Args()
                self.textEditCustomSettings.setText(self.svtav1Arguments)
                self.groupBoxSVTAV1Settings.setEnabled(False)
        else:
            self.groupBoxAomSettings.setEnabled(True)
            self.groupBoxRav1eSettings.setEnabled(True)
            self.groupBoxSVTAV1Settings.setEnabled(True)

    # ═════════════════════════════════════════════════
    # ═══════════════ Button Functions ════════════════
    # Button Open Video Source
    def OpenVideoSource(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Video...", "", "Video File (*.mp4 *.mkv *.webm *.flv *.mpg *.mpeg *.ts *.m2ts *.mov)")
        if fileName: # if fileName is not Null
            self.videoInput = fileName
            self.videoInputSet = True# ═════════════════════════════════════════════════
    # Button Save Video to
    def SaveVideoTo(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Video File", "", "Matroska (*.mkv);; WebM (*.webm)")
        if fileName:
            self.videoOutput = fileName
            self.videoOutputSet = True
    # ═════════════════════════════════════════════════
    # ═════════════════ MessageBoxe ═══════════════════
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
        rotate = self.groupBoxRotate.isChecked() == True
        amountFilters = 0
        filterCommand = None

        if crop: amountFilters += 1
        if resize: amountFilters += 1
        if deinterlace: amountFilters += 1

        if crop or resize or deinterlace or rotate:
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
            if rotate:
                if tempCounter == 1 or tempCounter == 2:
                    filterCommand += ","
                filterCommand += self.VideoRotate()
            if resize:
                if tempCounter == 1 or tempCounter == 2 or tempCounter == 3:
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

    def VideoRotate(self):
        if self.groupBoxRotate.isChecked() == True:
            if self.comboBoxRotateFilter.currentIndex() == 0:
                return "transpose=1"
            elif self.comboBoxRotateFilter.currentIndex() == 1:
                return "transpose=2"
            elif self.comboBoxRotateFilter.currentIndex() == 2:
                return "transpose=2,transpose=2"
            else:
                return None # unimplemented

    # ═════════════════════════════════════════════════
    # ══════════════════ AOM Args ═════════════════════

    def AomArgs(self):
        self.aomArguments = ""
        self.aomArguments += " --bit-depth=" + self.comboBoxBitDepth.currentText()   # Bit-Depth
        self.aomArguments += " --cpu-used=" + self.labelSpeed.text()                 # Speed (cpu-used)
        self.aomArguments += self.AomQualityMode()                                   # Quality (Q / Bitrate)
        if self.checkBoxAdvancedSettings.isChecked() == True:
            self.aomArguments += " --threads=" + str(self.spinBoxAomThreads.value())                            # Threads
            self.aomArguments += " --tile-columns=" + str(self.spinBoxAomTileColumns.value())                   # Tile Columns
            self.aomArguments += " --tile-rows=" + str(self.spinBoxAomTileRows.value())                         # Tile Rows
            self.aomArguments += " --kf-min-dist=" + str(self.spinBoxAomMinGOP.value())                         # Min GOP
            self.aomArguments += " --kf-max-dist=" + str(self.spinBoxAomMaxGOP.value())                         # Max GOP
            self.aomArguments += " --lag-in-frames=" + str(self.spinBoxAomLagInFrames.value())                  # Lag in Frames
            self.aomArguments += " --color-primaries=" + self.comboBoxAomColorPrimaries.currentText()           # Color Primaries
            self.aomArguments += " --transfer-characteristics=" + self.comboBoxAomColorTransfer.currentText()   # Color Transfer
            self.aomArguments += " --matrix-coefficients=" + self.comboBoxAomColorMatrix.currentText()          # Color Matrix
            self.aomArguments += " --" + self.comboBoxAomColorFormat.currentText()                              # Color Format
            self.aomArguments += " --aq-mode=" + str(self.comboBoxAomAQ.currentIndex())                         # AQ-Mode
            self.aomArguments += " --sharpness=" + str(self.spinBoxAomSharpness.value())                        # Sharpness Loop Filter
            self.aomArguments += " --enable-keyframe-filtering=" + str(self.spinBoxAomKFFiltering.value())      # Keyframe Filtering
            self.aomArguments += " --max-reference-frames=" + str(self.spinBoxAomRefFrames.value())             # Reference Frames
            if self.checkBoxAomForwardKeyframes.isChecked() == True:
                self.aomArguments += " --enable-fwd-kf=1"                                                       # Forward Reference Frames
            else:
                self.aomArguments += " --enable-fwd-kf=0"
            if self.checkBoxAomRowMT.isChecked() == True:
                self.aomArguments += " --row-mt=1"                                                              # Row Based Multi-Threading
            else:
                self.aomArguments += " --row-mt=0"
            if self.checkBoxAomAltRef.isChecked() == True:
                self.aomArguments += " --auto-alt-ref=1"                                                        # Auto Alt Ref Frames
            else:
                self.aomArguments += " --auto-alt-ref=0"
            if self.checkBoxAomBoost.isChecked() == True:
                self.aomArguments += " --frame-boost=1"                                                         # Frame Boost
            else:
                self.aomArguments += " --frame-boost=0"


    def AomQualityMode(self):
        if self.radioButtonConstantQ.isChecked() == True:
            return " --end-usage=q --cq-level=" + self.labelQuality.text()
        elif self.radioButtonBitrate.isChecked() == True:
            if self.checkBoxCBR.isChecked() == True:
                return " --end-usage=cbr --target-bitrate=" + str(self.spinBoxBitrate.value())
            else:
                return " --end-usage=vbr --target-bitrate=" + str(self.spinBoxBitrate.value())
        else:
            return " error "  # Something bad happened when landing here

    # ═════════════════════════════════════════════════
    # ═════════════════ Rav1e Args ════════════════════

    # Bit-Depth and Pixel Format has to be set while piping

    def Rav1eArgs(self):
        self.rav1eArguments = ""
        self.rav1eArguments += self.Rav1eQualityMode()
        self.rav1eArguments += " --speed " + self.labelSpeed.text()

        if self.checkBoxAdvancedSettings.isChecked() is True:
            self.rav1eArguments += " --threads " + str(self.spinBoxRav1eThreads.value())
            self.rav1eArguments += " --tile-cols " + str(self.spinBoxRav1eTileCols.value())
            self.rav1eArguments += " --tile-rows " + str(self.spinBoxRav1eTileRows.value())
            self.rav1eArguments += " --min-keyint " + str(self.spinBoxRav1eMinGOP.value())
            self.rav1eArguments += " --keyint " + str(self.spinBoxRav1eMaxGOP.value())
            self.rav1eArguments += " --rdo-lookahead-frames " + str(self.spinBoxRav1eLookahead.value())
            self.rav1eArguments += " --primaries " + self.comboBoxRav1eColorPrimaries.currentText()
            self.rav1eArguments += " --transfer " + self.comboBoxRav1eColorTransfer.currentText()
            self.rav1eArguments += " --matrix " + self.comboBoxRav1eColorMatrix.currentText()

            if self.groupBoxRav1eContentLight.isChecked() is True:
                self.rav1eArguments += " --content-light " + str(self.spinBoxRav1eContentCll.value()) + "," + str(self.spinBoxRav1eContentFall.value())

            if self.groupBoxRav1eMastering.isChecked() is True:
                self.rav1eArguments += " --mastering-display G(" + self.lineEditRav1eGx.text() + ","
                self.rav1eArguments += self.lineEditRav1eGy.text() + ")B(" + self.lineEditRav1eBx.text() + ","
                self.rav1eArguments += self.lineEditRav1eBy.text() + ")R(" + self.lineEditRav1eRx.text() + ","
                self.rav1eArguments += self.lineEditRav1eRy.text() + ")WP(" + self.lineEditRav1eWPx.text() + ","
                self.rav1eArguments += self.lineEditRav1eWPy.text() + ")L(" + self.lineEditRav1eLmax.text() + ","
                self.rav1eArguments += self.lineEditRav1eLmin.text() + ")"


    def Rav1eQualityMode(self):
        if self.radioButtonConstantQ.isChecked() == True:
            return " --quantizer " + self.labelQuality.text()
        else:
            return " --bitrate " + str(self.spinBoxBitrate.value())

    # ═════════════════════════════════════════════════
    # ════════════════ SVT-AV1 Args ═══════════════════

    def SvtAV1Args(self):
        self.svtav1Arguments = ""
        self.svtav1Arguments += self.SvtAV1QualityMode()
        self.svtav1Arguments += " --preset " + self.labelSpeed.text()

        if self.checkBoxAdvancedSettings.isChecked() is True:
            self.svtav1Arguments += " --lp " + str(self.spinBoxSVTAV1Threads.value())
            self.svtav1Arguments += " --tile-columns " + str(self.spinBoxSVTAV1TileCols.value())
            self.svtav1Arguments += " --tile-rows " + str(self.spinBoxSVTAV1TileRows.value())
            self.svtav1Arguments += " --keyint " + str(self.spinBoxSVTAV1GOP.value())
            self.svtav1Arguments += " --adaptive-quantization " + str(self.comboBoxSVTAV1AQMode.currentIndex())
            self.svtav1Arguments += " --color-format " + str(self.comboBoxSVTAV1Color.currentIndex() + 1)
            self.svtav1Arguments += " --profile " + str(self.comboBoxSVTAV1Profile.currentIndex())

            if self.checkBoxSVTAV1HDR.isChecked() is True:
                self.svtav1Arguments += " --enable-hdr 1"

            if self.checkBoxSVTAV116Bit.isChecked() is True:
                self.svtav1Arguments += " --16bit-pipeline 1"


    def SvtAV1QualityMode(self):
        if self.radioButtonConstantQ.isChecked() == True:
            return " --rc 0 -q " + self.labelQuality.text()
        elif self.checkBoxCBR.isChecked() == False:
            return " --rc 1 --tbr " + str(self.spinBoxBitrate.value())
        else:
            return " --rc 2 --tbr " + str(self.spinBoxBitrate.value())

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
