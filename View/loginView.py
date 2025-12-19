from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QRadioButton, QButtonGroup, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from View.colors import *


class LoginView(QWidget):
    login_signal = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout (centers everything)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # White box container
        white_box = QFrame()
        white_box.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
            }}
        """)
        white_box.setFixedWidth(400)

        layout = QVBoxLayout(white_box)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title = QLabel("Terminal 360")
        title.setFont(QFont("Poppins", 22, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PRIMARY};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(10)

        # Username
        username_label = QLabel("Username")
        username_label.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        username_label.setStyleSheet("color: black;")
        layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ACCENT};
                border-radius: 8px;
                font-size: 13px;
                font-family: Poppins;
                color: black;
                background-color: {BACKGROUND};
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY};
            }}
        """)
        layout.addWidget(self.username_input)

        layout.addSpacing(5)

        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: black;")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ACCENT};
                border-radius: 8px;
                font-size: 13px;
                font-family: Poppins;
                color: black;
                background-color: {BACKGROUND};
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY};
            }}
        """)
        layout.addWidget(self.password_input)

        layout.addSpacing(10)

        # Role selection
        self.role_group = QButtonGroup()
        self.admin_radio = QRadioButton("Admin")
        self.staff_radio = QRadioButton("Staff")
        self.admin_radio.setChecked(True)
        self.admin_radio.setStyleSheet(f"""
                    QRadioButton {{
                        color: black; 
                        font-family: Poppins; 
                        font-size: 12px;
                        spacing: 8px;
                    }}
                    QRadioButton::indicator {{
                        width: 18px;
                        height: 18px;
                    }}
                """)
        self.staff_radio.setStyleSheet(f"""
                    QRadioButton {{
                        color: black; 
                        font-family: Poppins; 
                        font-size: 12px;
                        spacing: 8px;
                    }}
                    QRadioButton::indicator {{
                        width: 18px;
                        height: 18px;
                    }}
                """)

        self.role_group.addButton(self.admin_radio)
        self.role_group.addButton(self.staff_radio)

        role_layout = QHBoxLayout()
        role_layout.setSpacing(30)
        role_layout.addWidget(self.admin_radio)
        role_layout.addWidget(self.staff_radio)
        role_layout.addStretch()
        layout.addLayout(role_layout)

        layout.addSpacing(5)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(45)
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                font-family: Poppins;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004450;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        login_btn.clicked.connect(self.on_login)
        layout.addWidget(login_btn)

        # Add white box to main layout
        main_layout.addWidget(white_box)

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = "admin" if self.admin_radio.isChecked() else "staff"
        self.login_signal.emit(username, password, role)

    def clear_fields(self):
        """Clear username and password fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.admin_radio.setChecked(True)

