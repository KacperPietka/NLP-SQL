import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from GUI import ChatWindow
import subprocess

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setFont(QFont("Inter"))
        self.chat_window = ChatWindow()
        self.chat_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    with open(os.devnull, 'wb') as devnull:
        subprocess.Popen(['sh', 'run.sh'], stdout=devnull, stderr=devnull)
    controller = AppController()
    controller.run()
