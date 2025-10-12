from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QListWidget, QLabel
)
from PyQt6.QtGui import QFont
from html import escape
import os
from NL_TO_SQL_LLM import NLToSQLModel
from SQL_EXECUTE import execute_sql_query
from SQL_Result_explainer import SQLResultExplainer


class ChatWindow(QWidget):
    def __init__(self, schema_manager):
        super().__init__()
        self.schema_manager = schema_manager
        self.setWindowTitle("SQL-NLP Chat")
        self.resize(800, 600)

        # Layouts
        main_layout = QHBoxLayout()
        sidebar = QVBoxLayout()
        chat_area = QVBoxLayout()

        # Sidebar (History)
        self.history_list = QListWidget()
        label_history = QLabel("🗂️ Last Questions")
        label_font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        label_history.setFont(label_font)
        sidebar.addWidget(label_history)
        sidebar.addWidget(self.history_list)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_font = QFont("Segoe UI", 11)
        chat_font.setBold(True)  # 🔥 make all chat text bold
        self.chat_display.setFont(chat_font)
        chat_area_label = QLabel("💬 SQL-NLP Chat Assistant")
        chat_area_label.setFont(label_font)
        chat_area.addWidget(chat_area_label)
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

            self.chat_display.append(
                f"""
                <div style="margin-top:10px; margin-bottom:10px; color:white;">
                    <b style="color:#00b4d8;">Assistant:</b> Sure, here you are!
                    <div>
                        <b>SQL Query:
                        <pre style="color:#00ff99; font-family:Consolas, monospace; white-space:pre-wrap; margin:4px 0;">{clean_sql}</pre>
                        <br></br>
                        <b>Explanation:
                        <div style="color:white; line-height:1.4; margin-top:4px;">
                            {clean_explanation}
                        </div>
                        <br></br>
                    </div>
                </div>
                """
            )
        except Exception as e:
            self.chat_display.append(f"<b>Assistant:</b> ❌ Error: {str(e)}")



        
