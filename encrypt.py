from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from tqdm.tk import trange
from Utils.Cipher import AESCipher

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        global instance
        instance = self
    class EncryptThread(QtCore.QThread):
        _signal = QtCore.pyqtSignal()
        
        def __init__(self):
            super(instance.EncryptThread, self).__init__()
        
        def __del__(self):
            self.wait()
        
        def run(self):
            file_path = sys.argv[1]
            enc_file_path = file_path + '.enc'
            # print(super)
            password = instance.lineEdit.text()
            cipher = AESCipher(passphrase=password)
            cipher.encrypt_file(file_path, enc_file_path)
            QtWidgets.QMessageBox.information(instance, '完成/Completed', '加密完成/Encrypted')
    
    
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(372, 282)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.setFont(font)
        self.centralwidget = QtWidgets.QWidget(self)
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
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 372, 19))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.thread = self.EncryptThread()
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        self.pushButton.clicked.connect(self.ok)
        self.pushButton_2.clicked.connect(self.close)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    @QtCore.pyqtSlot()
    def ok(self):
        #self.thread._signal.connect(self.pushButton)
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
    qb.setupUi()
    qb.show()
    sys.exit(app.exec_())
    