import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPixmap, QIcon, QAction, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from View.components import *

class UserManagementTab(QWidget):
    # Updated: now emits 7 fields (username, password, role, first_name, last_name, email, phone_number)
    add_user_signal = pyqtSignal(str, str, str, str, str, str, str)
    delete_user_signal = pyqtSignal(str)
    reactivate_user_signal = pyqtSignal(str)
    search_users_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # ── Left Panel: Add New User Form ──────────────────────────────
        user_frame = CardFrame()
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(20, 25, 20, 25)
        user_layout.setSpacing(12)

        user_layout.addWidget(SectionLabel("Add New User"))
        user_layout.addWidget(SubtitleLabel("Create a new user account"))

        user_layout.addWidget(FieldLabel("First Name"))
        self.new_first_name = StyledInput("Enter first name")
        user_layout.addWidget(self.new_first_name)

        user_layout.addWidget(FieldLabel("Last Name"))
        self.new_last_name = StyledInput("Enter last name")
        user_layout.addWidget(self.new_last_name)

        user_layout.addWidget(FieldLabel("Username"))
        self.new_username = StyledInput("Enter username")
        user_layout.addWidget(self.new_username)

        user_layout.addWidget(FieldLabel("Password"))
        self.new_password = StyledInput("Enter password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        user_layout.addWidget(self.new_password)

        user_layout.addWidget(FieldLabel("Email"))
        self.new_email = StyledInput("Enter email address")
        user_layout.addWidget(self.new_email)

        user_layout.addWidget(FieldLabel("Phone Number"))
        self.new_phone = StyledInput("09XXXXXXXXX")
        user_layout.addWidget(self.new_phone)

        user_layout.addWidget(FieldLabel("Role"))
        self.new_role = StyledComboBox()
        self.new_role.addItems(["admin", "staff"])
        user_layout.addWidget(self.new_role)

        add_btn = PrimaryButton("Add User", "✓")
        add_btn.clicked.connect(self.on_add_user)
        user_layout.addWidget(add_btn)
        user_layout.addStretch()

        # ── Right Panel: Users Table ───────────────────────────────────
        view_frame = CardFrame()
        view_layout = QVBoxLayout(view_frame)
        view_layout.setContentsMargins(25, 25, 25, 25)
        view_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)

        logo_label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "Assets", "userLogo.svg")
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        header_layout.addWidget(logo_label)
        header_layout.addWidget(SectionLabel("Manage Users", 18))
        header_layout.addStretch()
        view_layout.addLayout(header_layout)

        self.search_input = SearchInput("Search users by name, username, or email...")

        search_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "Assets", "searchIcon.svg")
        search_icon = QIcon(search_icon_path)
        search_action = QAction(search_icon, "", self.search_input)
        self.search_input.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)
        self.search_input.textChanged.connect(
            lambda: self.search_users_signal.emit(self.search_input.text()))
        view_layout.addWidget(self.search_input)

        # Table: Full Name | Username | Email | Phone | Role | Actions
        self.users_table = StyledTable(6, ["Full Name", "Username", "Email", "Phone", "Role", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        view_layout.addWidget(self.users_table)

        main_layout.addWidget(user_frame, 28)
        main_layout.addWidget(view_frame, 72)

    def show_error(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def show_question(self, title, message):
        reply = QMessageBox.question(
            self, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    def on_add_user(self):
        first_name = self.new_first_name.text().strip()
        last_name = self.new_last_name.text().strip()
        username = self.new_username.text().strip()
        password = self.new_password.text()
        email = self.new_email.text().strip()
        phone = self.new_phone.text().strip()
        role = self.new_role.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Invalid Input", "Username and password are required.")
            return
        if not first_name or not last_name:
            QMessageBox.warning(self, "Invalid Input", "First name and last name are required.")
            return
        if not email:
            QMessageBox.warning(self, "Invalid Input", "Email is required.")
            return
        if not phone.startswith("09") or len(phone) != 11 or not phone.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Phone number must start with 09 and be 11 digits.")
            return

        self.add_user_signal.emit(username, password, role, first_name, last_name, email, phone)
        self.new_first_name.clear()
        self.new_last_name.clear()
        self.new_username.clear()
        self.new_password.clear()
        self.new_email.clear()
        self.new_phone.clear()

    def update_users_table(self, users, current_username=None):
        self.users_table.setRowCount(len(users))
        for i, user in enumerate(users):
            is_current_user = (current_username and user.username == current_username)
            is_inactive = (user.active == 0)

            # ── Col 0: Full Name ──────────────────────────────────────
            full_name = user.full_name if user.full_name.strip() else user.username
            if is_current_user:
                full_name += " (You)"
            elif is_inactive:
                full_name += " (Inactive)"

            name_item = QTableWidgetItem(full_name)
            name_item.setFont(QFont("Poppins", 10,
                                    QFont.Weight.Bold if is_current_user else QFont.Weight.Medium))
            if is_inactive:
                name_item.setForeground(QColor("#999999"))
            elif is_current_user:
                name_item.setForeground(QColor("#006D77"))
            else:
                name_item.setForeground(QColor("#2c3e50"))
            self.users_table.setItem(i, 0, name_item)

            # ── Col 1: Username ───────────────────────────────────────
            uname_item = QTableWidgetItem(user.username)
            uname_item.setFont(QFont("Poppins", 9))
            uname_item.setForeground(QColor("#999999") if is_inactive else QColor("#555555"))
            self.users_table.setItem(i, 1, uname_item)

            # ── Col 2: Email ──────────────────────────────────────────
            email_item = QTableWidgetItem(user.email or "—")
            email_item.setFont(QFont("Poppins", 9))
            email_item.setForeground(QColor("#999999") if is_inactive else QColor("#2c3e50"))
            self.users_table.setItem(i, 2, email_item)

            # ── Col 3: Phone ──────────────────────────────────────────
            phone_item = QTableWidgetItem(user.phone_number or "—")
            phone_item.setFont(QFont("Poppins", 9))
            phone_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            phone_item.setForeground(QColor("#999999") if is_inactive else QColor("#2c3e50"))
            self.users_table.setItem(i, 3, phone_item)

            # ── Col 4: Role ───────────────────────────────────────────
            role_item = QTableWidgetItem(user.role.upper())
            if is_inactive:
                role_item.setForeground(QColor("#999999"))
            elif user.role == "admin":
                role_item.setForeground(QColor("#006D77"))
            else:
                role_item.setForeground(QColor("#6c757d"))
            role_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.users_table.setItem(i, 4, role_item)

            # ── Col 5: Actions ────────────────────────────────────────
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.setContentsMargins(5, 5, 5, 5)

            if is_current_user:
                disabled_btn = QPushButton("You")
                disabled_btn.setEnabled(False)
                disabled_btn.setMinimumHeight(40)
                disabled_btn.setMinimumWidth(120)
                disabled_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #D0D0D0;
                        color: #888888;
                        padding: 1px 1px;
                        border-radius: 6px;
                        font-family: Poppins;
                        font-size: 9pt;
                        font-weight: bold;
                        border: none;
                    }
                """)
                btn_layout.addWidget(disabled_btn)
            elif is_inactive:
                reactivate_btn = ReactivateButton()
                reactivate_btn.clicked.connect(
                    lambda checked, u=user.username: self.reactivate_user_signal.emit(u))
                btn_layout.addWidget(reactivate_btn)
            else:
                delete_btn = DeleteButton("Deactivate")
                delete_btn.clicked.connect(
                    lambda checked, u=user.username: self.delete_user_signal.emit(u))
                btn_layout.addWidget(delete_btn)

            self.users_table.setCellWidget(i, 5, btn_container)

        self.users_table.setColumnWidth(1, 110)
        self.users_table.setColumnWidth(3, 120)
        self.users_table.setColumnWidth(4, 90)
        self.users_table.setColumnWidth(5, 140)