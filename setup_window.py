from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget
)
from PyQt6.QtCore import pyqtSignal
import os
import shutil

class SetupWindow(QWidget):
    setup_complete = pyqtSignal(list, list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Databases and Schemas")
        self.resize(500, 400)

        layout = QVBoxLayout()

        self.yml_list = QListWidget()
        self.db_list = QListWidget()

        self.upload_yml_btn = QPushButton("Upload YAML Schema Files")
        self.upload_db_btn = QPushButton("Upload Database Files (.db)")
        self.start_btn = QPushButton("OK")

        layout.addWidget(QLabel("Schema Files"))
        layout.addWidget(self.yml_list)
        layout.addWidget(self.upload_yml_btn)

        layout.addWidget(QLabel("Database Files"))
        layout.addWidget(self.db_list)
        layout.addWidget(self.upload_db_btn)

        layout.addWidget(self.start_btn)
        self.setLayout(layout)

        # Connections
        self.upload_yml_btn.clicked.connect(self.upload_yml_files)
        self.upload_db_btn.clicked.connect(self.upload_db_files)
        self.start_btn.clicked.connect(self.finish_setup)

        self.yml_files = []
        self.db_files = []


    def upload_yml_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select YAML Files", "", "YAML Files (*.yml *.yaml)")
        if files:
            os.makedirs("yml_files", exist_ok=True)
            for f in files:
                dest = os.path.join("yml_files", os.path.basename(f))
                shutil.copy(f, dest)
                self.yml_files.append(dest)
                self.yml_list.addItem(dest)

    def upload_db_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Databases", "", "SQLite DB (*.db)")
        if files:
            os.makedirs("databases", exist_ok=True)
            for f in files:
                dest = os.path.join("databases", os.path.basename(f))
                shutil.copy(f, dest)
                self.db_files.append(dest)
                self.db_list.addItem(dest)


    def finish_setup(self):
        self.setup_complete.emit(self.yml_files, self.db_files)
