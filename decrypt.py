from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from Utils.Cipher import AESCipher


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        global instance
        instance = self
    class DecryptThread(QtCore.QThread):
        _signal = QtCore.pyqtSignal()
        
        def __init__(self):
            super(instance.DecryptThread, self).__init__()
        
        def __del__(self):
            self.wait()
        
        def run(self):
            enc_file_path = sys.argv[1]
            file_path = enc_file_path.rstrip('.enc')
            password = instance.lineEdit.text()
            cipher = AESCipher(passphrase=password)
            try:
                cipher.decrypt_file(enc_file_path, file_path)
            except ValueError:
                QtWidgets.QMessageBox.warning(instance, '错误/Error!', '密码错误/Passphrase incorrect')
            else:
                QtWidgets.QMessageBox.information(instance, '完成/Complete', '解密完成/Decrypted')
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(372, 282)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 70, 81, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(122, 70, 211, 20))
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 180, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 180, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 372, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.thread = self.DecryptThread()
        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.ok)
        self.pushButton_2.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    @QtCore.pyqtSlot()
    def ok(self):
        self.thread.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "请输入密码/Please enter the passphrase:"))
        self.pushButton.setText(_translate("MainWindow", "确定/Continue"))
        self.pushButton_2.setText(_translate("MainWindow", "退出/Quit"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qb = Ui_MainWindow()
    qb.setupUi(qb)
    qb.show()
    sys.exit(app.exec_())
    