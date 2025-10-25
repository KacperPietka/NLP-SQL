from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import QSettings
import snowflake.connector
from embedding_schema import ChromaSchemaManager

class SnowflakeConnectWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect to Snowflake")
        self.resize(400, 300)

        self.settings = QSettings("SQLNLPApp", "Snowflake")

        layout = QVBoxLayout(self)

        # --- Input fields ---
        self.account = QLineEdit(self.settings.value("account", ""))
        self.account.setPlaceholderText("Account (e.g. LGFLOEZ-MJ84823.west-europe.azure)")

        self.user = QLineEdit(self.settings.value("user", ""))
        self.user.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setText(self.settings.value("password", ""))

        self.warehouse = QLineEdit(self.settings.value("warehouse", ""))
        self.warehouse.setPlaceholderText("Warehouse")

        self.database = QLineEdit(self.settings.value("database", ""))
        self.database.setPlaceholderText("Database")

        self.schema = QLineEdit(self.settings.value("schema", ""))
        self.schema.setPlaceholderText("Schema")

        # --- Buttons ---
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_to_snowflake)

        layout.addWidget(QLabel("Account:"))
        layout.addWidget(self.account)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.user)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Warehouse:"))
        layout.addWidget(self.warehouse)
        layout.addWidget(QLabel("Database:"))
        layout.addWidget(self.database)
        layout.addWidget(QLabel("Schema:"))
        layout.addWidget(self.schema)
        layout.addWidget(self.connect_btn)

    def connect_to_snowflake(self):
        try:
            conn = snowflake.connector.connect(
                user=self.user.text(),
                password=self.password.text(),
                account=self.account.text(),
                warehouse=self.warehouse.text(),
                database=self.database.text(),
                schema=self.schema.text(),
            )
            cur = conn.cursor()
            cur.execute("SELECT CURRENT_VERSION();")
            QMessageBox.information(self, "Success", f"✅ Connected to Snowflake!")

            # --- Save credentials ---
            self.settings.setValue("account", self.account.text())
            self.settings.setValue("user", self.user.text())
            self.settings.setValue("password", self.password.text())
            self.settings.setValue("warehouse", self.warehouse.text())
            self.settings.setValue("database", self.database.text())
            self.settings.setValue("schema", self.schema.text())


            cur.close()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(None, "Connection failed", f"❌ {e}")
