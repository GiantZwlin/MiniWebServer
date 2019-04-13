import sys
import socket
import time
from datetime import datetime

from server import Server
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QLabel
import threading


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('1.1.1.1', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class Console(QWidget):
    def __init__(self):
        super().__init__()
        self.open_server = QPushButton("Open Server")
        self.close_server = QPushButton("Close Server")
        self.log_field = QTextEdit()
        ip = get_host_ip()
        self.ip_label = QLabel(" This server is listening to {}:{}".format(ip, 8080))
        self.server = Server(ip, 8080)
        self.state = False
        self.log = ''
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("Web Server Console")
        self.open_server.clicked.connect(self.control)
        self.close_server.clicked.connect(self.control)

        label = QLabel(" Log:")
        h_box = QHBoxLayout()

        h_box.addWidget(self.open_server)
        h_box.addWidget(self.close_server)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addWidget(self.ip_label)
        v_box.addWidget(label)
        v_box.addWidget(self.log_field)
        self.setGeometry(300, 400, 300, 200)

        self.setLayout(v_box)
        self.show()

    def control(self):
        sender = self.sender()
        if sender == self.open_server:
            if not self.server.status:
                t = threading.Thread(target=self.server.start)
                t.start()
                self.log += "{}: Server start!\n".format(str(datetime.today())[:-7])
            else:
                self.log += "{}: Server already start!\n".format(str(datetime.today())[:-7])
        if sender == self.close_server:
            if self.server.status:
                self.server.close()
                time.sleep(1)
                self.log += "{}: Server close!\n".format(str(datetime.today())[:-7])
            else:
                self.log += "{}: Server not start yet!\n".format(str(datetime.today())[:-7])
        self.log_field.setText(self.log)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Console()
    sys.exit(app.exec_())
