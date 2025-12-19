from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon
from View.colors import *


class AdminMenuView(QWidget):
    # Signals for navigation
    open_overview_signal = pyqtSignal()
    open_transactions_signal = pyqtSignal()
    open_pos_signal = pyqtSignal()
    open_user_product_mgmt_signal = pyqtSignal()
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30,30,30,30)
        main_layout.setSpacing(30)

        # Header with logo and title
        header_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        # Title
        title = QLabel("Admin Menu")
        title.setFont(QFont("Poppins", 28, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedWidth(100)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Poppins;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #6FAAA4;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        header_layout.addWidget(logout_btn)

        main_layout.addLayout(header_layout)

        # Grid layout for 4 menu buttons (2x2)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)

        # Button 1: Overview
        overview_btn = self.create_menu_button(
            "Overview",
            r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\homeHollow.png",
            "View system overview and statistics"
        )
        overview_btn.clicked.connect(self.open_overview_signal.emit)
        grid_layout.addWidget(overview_btn, 0, 0)

        # Button 2: Transactions
        transactions_btn = self.create_menu_button(
            "Transactions",
            r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\tranHollow.png",
            "View transaction history"
        )
        transactions_btn.clicked.connect(self.open_transactions_signal.emit)
        grid_layout.addWidget(transactions_btn, 0, 1)

        # Button 3: POS
        pos_btn = self.create_menu_button(
            "Point of Sale",
            r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\posHollow.png",  # You can use a different icon
            "Open POS system"
        )
        pos_btn.clicked.connect(self.open_pos_signal.emit)
        grid_layout.addWidget(pos_btn, 1, 0)

        # Button 4: User & Product Management
        mgmt_btn = self.create_menu_button(
            "User & Product\nManagement",
            r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\userProductHolllow.png",  # You can use a different icon
            "Manage users and products"
        )
        mgmt_btn.clicked.connect(self.open_user_product_mgmt_signal.emit)
        grid_layout.addWidget(mgmt_btn, 1, 1)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def create_menu_button(self, title, icon_path, description):
        """Create a styled menu button with icon and text"""
        btn = QPushButton()
        btn.setMinimumSize(300, 250)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border-radius: 15px;
                border: 2px solid {ACCENT};
                text-align: center;
            }}
            QPushButton:hover {{
                border: 3px solid {PRIMARY};
                background-color: {BACKGROUND};
            }}
            QPushButton:pressed {{
                background-color: {ACCENT};
                border: 2px solid {PRIMARY};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {ACCENT};
            }}
        """)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout for button content
        layout = QVBoxLayout(btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        else:
            icon_label.setText("📊")
            icon_label.setFont(QFont("Arial", 60))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {PRIMARY};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Poppins", 11))
        desc_label.setStyleSheet("color: #666666;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        return btn