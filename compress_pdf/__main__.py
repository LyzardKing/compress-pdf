#! /usr/bin/env python3

import logging
import os
import signal
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QDialog, QButtonGroup
from PyQt5.QtWidgets import QPushButton, QRadioButton, QAction, QLineEdit, QMessageBox, QLabel

logging.basicConfig(level=logging.ERROR, format="%(message)s")
logger = logging.getLogger(__name__)

levels = {1: "prepress", 2:"screen", 3:"ebook"}

class Root(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        self.setFixedSize(800, 500)
        self.title = "PDF-Compressor is an Open Source Project by IT'S FOSS"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 500

        self.setWindowIcon(QtGui.QIcon("its.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.button = QPushButton('Select File', self)
        self.button.clicked.connect(self.select_pdf)
        self.button.move(200, 250)

        self.button2 = QPushButton('Compress', self)
        self.button2.clicked.connect(lambda:self.compress(self.groupButton.checkedId()))
        self.button2.move(500, 250)
        self.button2.setEnabled(False)
        self.button2.setStyleSheet("background-color: #808080; ")

        self.radio1 = QRadioButton('Low Compression', self)
        self.radio1.move(330, 180)
        self.radio1.resize(200, 20)
        self.radio1.setChecked(True)

        self.radio2 = QRadioButton('Medium Compression', self)
        self.radio2.move(330, 210)
        self.radio2.resize(200, 20)

        self.radio3 = QRadioButton('High Compression', self)
        self.radio3.move(330, 240)
        self.radio3.resize(200, 20)

        self.groupButton = QButtonGroup()
        self.groupButton.addButton(self.radio1, 1)
        self.groupButton.addButton(self.radio2, 2)
        self.groupButton.addButton(self.radio3, 3)

        self.image = QLabel(self)
        self.image.setPixmap(QtGui.QPixmap("pdff.png"))
        self.image.resize(100, 100)
        self.image.move(230, 150)
        self.image.show()

        self.image2 = QLabel(self)
        self.image2.setPixmap(QtGui.QPixmap("inboxx.png"))
        self.image2.resize(100, 100)
        self.image2.move(525, 150)
        self.image2.show()

        self.image3 = QLabel(self)
        self.image3.setPixmap(QtGui.QPixmap("its.png"))
        self.image3.resize(50, 50)
        self.image3.move(180, 385)
        self.image3.show()

        self.label = QLabel(self)
        self.label.setText("PDF-Compressor is an Open Source Project by It's FOSS")
        self.label.move(250, 400)
        self.label.resize(400, 20)

        self.show()

    def select_pdf(self):
        self.file = QFileDialog.getOpenFileName(self, "Select a Pdf File", "/home/", "Pdf Files (*.pdf)")[0]
        self.button.setText(os.path.basename(self.file))
        self.button2.setStyleSheet("background-color: green ")
        self.button2.setEnabled(True)

    def compress(self, check):
        logger.info("Starting compress method")
        try:
            compress(self.file, check)
        except subprocess.CalledProcessError as e:
            self.error_dialog()
        else:
            # Subprocess should fail if an error occurred.
            # If we end up here we can pull up the success page
            self.success_dialog()

    def error_dialog(self):
        message_dialog = QMessageBox()
        message_dialog.setIconPixmap(QtGui.QPixmap("its.png"))
        message_dialog.setWindowTitle("Error")
        message_dialog.setText("Something went wrong!")
        message_dialog.setStandardButtons(QMessageBox.Ok)
        message_dialog.exec_()

    def success_dialog(self):
        message_dialog = QMessageBox()
        message_dialog.setIconPixmap(QtGui.QPixmap("its.png"))
        message_dialog.setWindowTitle("Success")
        message_dialog.setText("Your file has been compressed.\nIt coexists with your input file.")
        message_dialog.setStandardButtons(QMessageBox.Ok)
        message_dialog.exec_()


def compress(file, check):
    '''Method that runs the actual compression'''
    logger.info("Running compress ghostscript function")
    filename = os.path.split(file)[-1]
    output_file = file.replace(filename, filename.split(".")[0] + "-compressed.pdf")
    level = levels[check]
    command = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", f"-dPDFSETTINGS=/{level}",
                "-dNOPAUSE", "-dQUIET", "-dBATCH", f'-sOutputFile="{output_file}"', f'"{file}"']
    logger.info("Compress command complete")
    subprocess.run(command, check=True)

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    root = Root()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
