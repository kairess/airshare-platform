import sys, socket, os
import airshare
import requests
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton

SERVER_ADDR = 'http://172.30.1.48:32456'
PORT = 23456

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel(self)
        lbl.setText('Your computer name (English):' + application_path)

        self.qle = QLineEdit(self)

        self.btn = QPushButton('Connect', self)
        self.btn.clicked.connect(self.connect)

        self.btn2 = QPushButton('Disconnect', self)
        self.btn2.setEnabled(False)
        self.btn2.clicked.connect(self.disconnect)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(self.qle)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.btn2)

        self.setLayout(vbox)
        self.setWindowTitle('Airshare Client')
        self.show()

    def connect(self):
        code = str(self.qle.text())
        if not code or not code.isalpha():
            return False

        local_ip_addr = socket.inet_ntoa(airshare.utils.get_local_ip_address())

        data = {
            'code': code,
            'ip_addr': local_ip_addr,
            'port': PORT,
        }

        r = requests.post('%s/register' % (SERVER_ADDR,), data)

        try:
            webbrowser.open('%s/browse' % SERVER_ADDR)
        except:
            print('%s/browse' % SERVER_ADDR)

        self.btn.setEnabled(False)
        self.btn2.setEnabled(True)
        
        self.process = airshare.receiver.receive_server_proc(code=code, port=PORT)
        self.process.start()

    def disconnect(self):
        self.process.terminate()

        self.btn.setEnabled(True)
        self.btn2.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
