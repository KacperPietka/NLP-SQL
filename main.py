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
        # Run the GUI event loop
        exit_code = self.app.exec()

        # When user closes the window, stop Ollama
        with open(os.devnull, 'wb') as devnull:
            subprocess.Popen(['sh', 'run.sh', "exit"], stdout=devnull, stderr=devnull)

        sys.exit(exit_code)


if __name__ == "__main__":
    # Start Ollama before launching GUI
    with open(os.devnull, 'wb') as devnull:
        subprocess.Popen(['sh', 'run.sh', "run"], stdout=devnull, stderr=devnull)

    controller = AppController()
    controller.run()
