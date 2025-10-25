import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from GUI import ChatWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setFont(QFont("Inter"))
        self.chat_window = ChatWindow()
        self.chat_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
