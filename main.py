import sys
from PyQt6.QtWidgets import QApplication
from setup_window import SetupWindow
from embedding_schema import ChromaSchemaManager
from GUI import ChatWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.schema_manager = ChromaSchemaManager()

        # Show setup window first
        self.setup_window = SetupWindow()
        self.setup_window.setup_complete.connect(self.on_setup_complete)
        self.setup_window.show()

    def on_setup_complete(self, yml_files, db_files):
        """Called when the user finishes setup."""
        # Load YAML schemas safely
        for yml_file in yml_files:
            try:
                self.schema_manager.add_yml(yml_file)
                print(f"✅ Added schema: {yml_file}")
            except Exception as e:
                print(f"⚠️ Could not add {yml_file}: {e}")

        print("✅ All schemas loaded into ChromaDB.")

        # Close setup window and open chat
        self.setup_window.close()
        self.chat_window = ChatWindow(self.schema_manager, db_files)
        self.chat_window.show()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
