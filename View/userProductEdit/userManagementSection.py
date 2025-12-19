from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QColor
from View.colors import *


class UserManagementSection(QWidget):
    add_user_signal = pyqtSignal(str, str, str)
    delete_user_signal = pyqtSignal(str)
    search_users_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Add User Section
        user_frame = QFrame()
        user_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        user_layout = QVBoxLayout(user_frame)

        user_title = QLabel("Add User")
        user_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        user_title.setStyleSheet("color: black;")
        user_layout.addWidget(user_title)

        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("Username")
        self.new_username.setStyleSheet("font-family: Poppins; color: black; padding: 5px; background-color: white;")
        user_layout.addWidget(self.new_username)

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setStyleSheet("font-family: Poppins; color: black; padding: 5px; background-color: white;")
        user_layout.addWidget(self.new_password)

        self.new_role = QComboBox()
        self.new_role.addItems(["admin", "staff"])
        self.new_role.setStyleSheet("font-family: Poppins; color: black; padding: 5px; background-color: white;")
        user_layout.addWidget(self.new_role)

        add_user_btn = QPushButton("Add User")
        add_user_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Poppins;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        add_user_btn.clicked.connect(self.on_add_user)
        user_layout.addWidget(add_user_btn)

        layout.addWidget(user_frame)

        # View Users Section
        view_users_frame = QFrame()
        view_users_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        view_users_layout = QVBoxLayout(view_users_frame)

        view_users_title = QLabel("Manage Users")
        view_users_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        view_users_title.setStyleSheet("color: black;")
        view_users_layout.addWidget(view_users_title)

        # Search users
        self.search_user_input = QLineEdit()
        self.search_user_input.setPlaceholderText("Search username...")
        self.search_user_input.setStyleSheet(
            "font-family: Poppins; color: black; padding: 5px; background-color: white;")
        self.search_user_input.textChanged.connect(lambda: self.search_users_signal.emit(self.search_user_input.text()))
        view_users_layout.addWidget(self.search_user_input)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["Username", "Role", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 5px;
                color: black;
                font-family: Poppins;
            }
            QHeaderView::section {
                background-color: #006D77;
                color: white;
                font-family: Poppins;
                font-weight: bold;
                padding: 5px;
            }
        """)
        view_users_layout.addWidget(self.users_table)

        layout.addWidget(view_users_frame)
        self.setLayout(layout)

    def on_add_user(self):
        username = self.new_username.text()
        password = self.new_password.text()
        role = self.new_role.currentText()

        if username and password:
            self.add_user_signal.emit(username, password, role)
            self.new_username.clear()
            self.new_password.clear()

    def update_users_table(self, users):
        """Update the users table display"""
        self.users_table.setRowCount(len(users))
        for i, user in enumerate(users):
            # Username
            username_item = QTableWidgetItem(user.username)
            username_item.setForeground(QColor("black"))
            self.users_table.setItem(i, 0, username_item)

            # Role
            role_item = QTableWidgetItem(user.role)
            role_item.setForeground(QColor("black"))
            self.users_table.setItem(i, 1, role_item)

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #E63946;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 3px;
                    font-family: Poppins;
                }}
                QPushButton:hover {{
                    background-color: #D62828;
                }}
                QPushButton:focus {{
                outline: none;
                border: none;
                }}  
                QPushButton:focus {{
                outline: none;
                border: none;
            }}
            """)
            delete_btn.clicked.connect(lambda checked, u=user.username: self.delete_user_signal.emit(u))
            self.users_table.setCellWidget(i, 2, delete_btn)