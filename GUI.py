from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QListWidget, QLabel
)
from PyQt6.QtGui import QFont
import sys

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL-NLP Chat")
        self.resize(800, 600)

        # Layouts
        main_layout = QHBoxLayout()
        sidebar = QVBoxLayout()
        chat_area = QVBoxLayout()

        # Sidebar (History)
        self.history_list = QListWidget()
        sidebar.addWidget(QLabel("🗂️ Last Questions"))
        sidebar.addWidget(self.history_list)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        chat_area.addWidget(QLabel("💬 SQL-NLP Chat Assistant"))
        chat_area.addWidget(self.chat_display)

        # Input row (QLineEdit + Send button)
        input_row = QHBoxLayout()

        self.input_bar = QLineEdit()
        self.input_bar.setPlaceholderText("Ask a question about your data...")
        self.input_bar.setFont(QFont("Segoe UI", 12))
        self.input_bar.setMinimumHeight(40)

        self.send_button = QPushButton("SEND")
        self.send_button.setFont(QFont("Segoe UI", 11))
        self.send_button.setFixedHeight(40)
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

    def send_message(self):
        question = self.input_bar.text().strip()
        if not question:
            return

        self.chat_display.append(f"<b>You:</b> {question}")
        self.history_list.addItem(question)
        self.input_bar.clear()

        try:
            sql_query, context = generate_sql_from_question(question)
            self.chat_display.append(f"<b>Assistant:</b><br>SQL → <code>{sql_query}</code><br><br>")
        except Exception as e:
            self.chat_display.append(f"<b>Assistant:</b> ❌ Error: {str(e)}")

        
