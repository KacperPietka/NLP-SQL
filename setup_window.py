from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QMessageBox
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

        self.upload_yml_btn.clicked.connect(self.upload_yml_files)
        self.upload_db_btn.clicked.connect(self.upload_db_files)
        self.start_btn.clicked.connect(self.finish_setup)

        self.yml_files = []
        self.db_files = []


    def upload_yml_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select YAML Files", "", "YAML Files (*.yml *.yaml)")
        if files:
            for f in files:
                self.yml_files.append(f)
                self.yml_list.addItem(f)

    def upload_db_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Databases", "", "SQLite DB (*.db)")
        if files:
            for f in files:
                self.db_files.append(f)
                self.db_list.addItem(f)

    def finalize_uploading(self):
        if self.db_files:
            os.makedirs("databases", exist_ok=True)
            for f in self.db_files:
                if os.path.exists(f):
                    dest = os.path.join("databases", os.path.basename(f))
                    shutil.copy2(f, dest)  # preserves metadata
                else:
                    continue

        if self.yml_files:
            os.makedirs("yml_files", exist_ok=True)
            for f in self.yml_files:
                if os.path.exists(f):
                    dest = os.path.join("yml_files", os.path.basename(f))
                    shutil.copy2(f, dest)
                else:
                    continue

    def check_if_files_uploaded_correctly(self):
        if len(self.db_files) != len(self.yml_files):
            QMessageBox.warning(self, "Upload Error", 
            "The uploaded .yml and .db files must match.\nPlease try again.")
            return False
        else:
            db_names = [os.path.splitext(os.path.basename(f))[0] for f in self.db_files]
            yml_names = [os.path.splitext(os.path.basename(f))[0] for f in self.yml_files]
            if sorted(db_names) != sorted(yml_names):
                QMessageBox.warning(self, "Upload Error", 
                "The uploaded .yml and .db files must match.\nPlease try again.")
                return False
        return True
        

    def finish_setup(self):
        ### Check if all files are correctly uploaded
        if self.check_if_files_uploaded_correctly():
            self.finalize_uploading()
            self.setup_complete.emit(self.yml_files, self.db_files)
        else:
            self.yml_list.clear()
            self.db_list.clear()
            self.yml_files.clear()
            self.db_files.clear()
