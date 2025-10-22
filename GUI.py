from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QListWidget, QLabel, QDialog
)
from PyQt6.QtGui import QFont, QTextCursor, QTextBlockFormat
from PyQt6.QtCore import Qt
from setup_window import SetupWindow
from html import escape
import os
from NL_TO_SQL_LLM import NLToSQLModel
from SQL_EXECUTE import execute_sql_query
from SQL_Result_explainer import SQLResultExplainer


class ChatWindow(QWidget):
    def __init__(self, schema_manager, db_files):
        super().__init__()
        self.db_files = db_files or []
        self.schema_manager = schema_manager
        self.setWindowTitle("SQL-NLP Chat")
        self.resize(800, 600)
        self.current_files = []

        # Layouts
        main_layout = QHBoxLayout()
        sidebar = QVBoxLayout()
        chat_area = QVBoxLayout()

        # Uploading button
        self.upload_button = QPushButton("Upload files")
        self.upload_button.setFixedHeight(45)
        self.upload_button.clicked.connect(self.upload_files)

        # Current list
        self.current_list_display = QPushButton("Current files")
        self.current_list_display.setFixedHeight(30)
        self.current_list_display.clicked.connect(self.display_current_files)

        # Sidebar (History)
        self.history_list = QListWidget()
        label_history = QLabel("Last Questions")
        label_font = QFont()
        label_font.setBold(True)
        label_history.setFont(label_font)
        sidebar.addWidget(label_history)
        sidebar.addWidget(self.history_list)
        sidebar.addWidget(self.upload_button)

        # Chat area header (label + "Current files" button aligned right)
        chat_header = QHBoxLayout()
        chat_area_label = QLabel("SQL-NLP Chat Assistant")
        chat_area_label.setFont(label_font)
        chat_header.addWidget(chat_area_label)
        chat_header.addStretch()  # pushes the button to the right
        chat_header.addWidget(self.current_list_display)
        chat_area.addLayout(chat_header)


        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_area.addWidget(self.chat_display)

        # Input row (QLineEdit + Send button)
        input_row = QHBoxLayout()


        self.input_bar = QLineEdit()
        self.input_bar.setPlaceholderText("Ask a question about your data...")
        self.input_bar.setMinimumHeight(40)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(45)
        self.send_button.setFixedWidth(100)


        input_row.addWidget(self.input_bar, stretch=1)
        input_row.addWidget(self.send_button)

        chat_area.addLayout(input_row)

        # Combine layouts
        main_layout.addLayout(sidebar, 2)
        main_layout.addLayout(chat_area, 7)
        self.setLayout(main_layout)

        # Connect button
        self.send_button.clicked.connect(self.send_message)
        self.input_bar.returnPressed.connect(self.send_message)  # Press Enter to send

        # Styling the push buttons and the input bar
        self.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;  /* dark background */
            color: white;
            font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
        }

        QTextEdit {
            background-color: #2b2b2b;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 6px;
        }

        QListWidget {
            background-color: #2b2b2b;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 4px;
        }

        QPushButton {
            font-size: 14px;
            font-weight: 600;
            color: white;
            border-radius: 8px;
            background-color: #3a3a3a;
            padding: 8px 12px;
        }

        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }

        QLineEdit {
            background-color: #2b2b2b;
            color: white;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 6px;
        }
""")

    
    def upload_files(self):
        """Open the SetupWindow to upload YAML and DB files."""
        self.setup_window = SetupWindow()
        self.setup_window.setup_complete.connect(self.on_files_uploaded)
        self.setup_window.show()

    def on_files_uploaded(self, yml_files, db_files):
        """Triggered after user uploads files in the setup window."""
        for yml_file in yml_files:
            try:
                self.schema_manager.add_yml(yml_file)
                self.chat_display.append(f"<b>Loaded {len(yml_files)} yml files.</b>")
            except Exception as e:
                self.chat_display.append(f"<b>Failed to add:</b> {yml_file} ({e})")
        self.db_files = db_files
        self.chat_display.append(f"<b> Loaded {len(db_files)} database files.</b>")
        self.setup_window.close()
    
    def display_current_files(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Current Files")
        dialog.resize(400, 300)

        layout = QVBoxLayout(dialog)
        list_widget = QListWidget()

        # Add files
        if os.path.exists("databases"):
            for f in os.listdir("databases"):
                list_widget.addItem(f"DB: {f}")
        if os.path.exists("yml_files"):
            for f in os.listdir("yml_files"):
                list_widget.addItem(f"YML: {f}")

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)

        layout.addWidget(list_widget)
        layout.addWidget(close_button)

        dialog.exec()


    def send_message(self):
        question = self.input_bar.text().strip()
        if not question:
            return

        self.history_list.addItem(question)
        self.input_bar.clear()

        try:
            # Retrieve schema + context
            context = self.schema_manager.get_context(question)
            schema = self.schema_manager.get_schema(question)
            nl_to_sql_model = NLToSQLModel(question, schema, context)
            sql_query = nl_to_sql_model.run() ### returns SQL query string

            results_of_the_query = execute_sql_query(sql_query) ### returns JSON results

            interpret_sql_model = SQLResultExplainer(question, sql_query, results_of_the_query, schema, context)
            interpretation = interpret_sql_model.run() ### returns explanation string
            
            clean_sql = escape(sql_query)
            clean_explanation = escape(interpretation)

             # --- USER MESSAGE (right aligned) ---
            cursor = self.chat_display.textCursor()
            user_format = QTextBlockFormat()
            user_format.setAlignment(Qt.AlignmentFlag.AlignRight)
            cursor.insertBlock(user_format)
            cursor.insertHtml(f"<span style='color:#00b4d8;'><b>You:</b> {question}</span>")

            cursor.insertHtml("<br>") 

            # --- ASSISTANT MESSAGE (left aligned) ---
            bot_format = QTextBlockFormat()
            bot_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
            cursor.insertBlock(bot_format)
            cursor.insertHtml(f"<span style='color:#ffffff;'>{clean_explanation}</span>")

            self.chat_display.setTextCursor(cursor)
            cursor.insertHtml("<br>") 

        except Exception as e:
            self.chat_display.append(f"<b>Assistant:</b> ❌ Error: {str(e)}")



        
