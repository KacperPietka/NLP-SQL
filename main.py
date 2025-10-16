import sys
from PyQt6.QtWidgets import QApplication
from setup_window import SetupWindow
from embedding_schema import ChromaSchemaManager
from GUI import ChatWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.schema_manager = ChromaSchemaManager()
        self.chat_window = ChatWindow(self.schema_manager, db_files=[])
        self.chat_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
