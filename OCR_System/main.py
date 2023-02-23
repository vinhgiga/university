import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from mainUI import Ui_MainForm
from textUi import Ui_TextForm

import utils

class TextWindow(QtWidgets.QWidget, Ui_TextForm):
    def __init__(self, parent = None):
        super(TextWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_copy_text.clicked.connect(self.copy_text_to_clipboard)
        self.pushButton_save_to_file.clicked.connect(self.save_text_to_file)
        self.clipboard = QtWidgets.QApplication.clipboard()

    def copy_text_to_clipboard(self):
        self.clipboard.setText(self.text.text())
    
    def save_text_to_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save as",os.getcwd(), "Text Files (*.txt);; All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.text.text())


class MainWindow(QtWidgets.QWidget, Ui_MainForm):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_read_file.clicked.connect(self.read_file)

        self.checkBox_remove_noise.clicked.connect(self.show_process_image)
        self.checkBox_convert_to_binary.clicked.connect(self.show_process_image)
        self.checkBox_deskew.clicked.connect(self.show_process_image)
        
        self.pushButton_detectText.clicked.connect(self.detect_text)
        self.pushButton_image.clicked.connect(self.show_original_image)
        self.pushButton_image_process.clicked.connect(self.show_process_image)

        self.init()
    
    def init(self):
        self.cvImage = None
        self.process_cvImage = None
    
    def show_dialog(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.exec_()

    def read_file(self):
        try:
            # print('OK')
            path_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd(), 'Image File (*.png *.jpg *.jpeg)')[0]
            if path_file != '':
                self.cvImage = utils.read_image(path_file)
                self.show_image(self.cvImage)
        except Exception as e:
            print(e)
    
    def process_image(self):
        self.process_cvImage = None
        if self.cvImage is None:
            raise AttributeError("None Image")

        if self.processBar.isChecked():
            if self.checkBox_remove_noise.isChecked():
                self.process_cvImage = utils.denoise(self.cvImage)
            if self.checkBox_convert_to_binary.isChecked():
                if self.process_cvImage is not None:
                    self.process_cvImage = utils.convert_to_binary(self.process_cvImage)
                else:
                    self.process_cvImage = utils.convert_to_binary(self.cvImage)
            if self.checkBox_deskew.isChecked():
                if self.process_cvImage is not None:
                    self.process_cvImage = utils.deskew(self.process_cvImage)
                else:
                    self.process_cvImage = utils.deskew(self.cvImage)

    def detect_text(self):
        self.process_image()
        if self.process_cvImage is not None:
            image = self.process_cvImage 
        else:
            image = utils.convert_to_rgb(self.cvImage)
        
        text = utils.detect_text(image)

        # show info empty text
        if text == '':
            message = 'Không tìm thấy ký tự nào trong ảnh'
            self.show_dialog(message)
        else:
            self.text_window = TextWindow()
            self.text_window.text.setText(text)
            self.text_window.show()
    
    def show_image(self, cvImage):
        if cvImage is None:
            raise AttributeError("None Image")
        else:
            if utils.isgray(cvImage):
                image =  QtGui.QImage(cvImage, cvImage.shape[1],cvImage.shape[0],cvImage.strides[0], QtGui.QImage.Format_Grayscale8)
            else:
                image = QtGui.QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], cvImage.strides[0], QtGui.QImage.Format_BGR888)
            self.image_frame.setPixmap(QtGui.QPixmap.fromImage(image))

    def show_original_image(self):
        try:
            self.show_image(self.cvImage)
        except AttributeError:
            self.show_dialog('Bạn chưa chọn ảnh đầu vào')

    def show_process_image(self):
        try:
            self.process_image()
            self.show_image(self.process_cvImage)
        except AttributeError:
            if self.cvImage is None:
                self.show_dialog('Bạn chưa chọn ảnh đầu vào')
            else:
                self.show_dialog('Vui lòng chọn chức năng xử lý ảnh để hiển thị ảnh đã xử lý')


def main(argv: list):
    try:
        app = QtWidgets.QApplication(argv)
        window = MainWindow()
        window.show()
    except Exception as e:
        print("Exception:", e)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
