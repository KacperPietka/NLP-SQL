import sys
import os
from embedding_schema import ChromaSchemaManager
from GUI import ChatWindow
from PyQt6.QtWidgets import QApplication



if __name__ == "__main__":
    schema_manager = ChromaSchemaManager()
    schema_file = "yml_files/example_schema.yml"

    if os.path.exists(schema_file):
        try:
            schema_manager.add_yml(schema_file)
            print("✅ Schema loaded into ChromaDB.")
        except Exception as e:
            print(f"⚠️ Could not add schema: {e}")
    else:
        print(f"❌ Schema file not found: {schema_file}")

    app = QApplication(sys.argv)
    window = ChatWindow(schema_manager)
    window.show()
    sys.exit(app.exec())