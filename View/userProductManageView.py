from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from View.colors import *
from View.userProductEdit import UserManagementSection, ProductManagementSection

class AdminView(QWidget):
    # All signals forwarded from child sections
    view_overview_signal = pyqtSignal()
    add_user_signal = pyqtSignal(str, str, str)
    add_product_signal = pyqtSignal(str, float, int)
    delete_user_signal = pyqtSignal(str)
    delete_product_signal = pyqtSignal(int)
    search_users_signal = pyqtSignal(str)
    search_products_signal = pyqtSignal(str)
    view_transactions_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    open_pos_signal = pyqtSignal()
    back_to_admin_signal = pyqtSignal()  # NEW: Separate signal for going back to admin menu

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header with buttons
        header_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        header = QLabel("User|Product Management")
        header.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Back to Admin button (REPLACED "Back to Menu")
        back_admin_btn = QPushButton("Back to Admin")
        back_admin_btn.setFixedWidth(130)
        back_admin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 8px;
                border-radius: 5px;
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
        back_admin_btn.clicked.connect(self.back_to_admin_signal.emit)  # FIXED: Use separate signal
        back_admin_btn.clicked.connect(lambda: print("Back to Admin button clicked!"))  # DEBUG
        header_layout.addWidget(back_admin_btn)

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedWidth(100)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-family: Poppins;
            }}
            QPushButton:hover {{
                background-color: #6FAAA4;
            }}
            QPushButton:pressed {{
                background-color: #5A9489;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        header_layout.addWidget(logout_btn)

        layout.addLayout(header_layout)

        # Main content in horizontal layout
        main_content = QHBoxLayout()

        # LEFT SIDE - User Management Section
        self.user_section = UserManagementSection()
        self.user_section.add_user_signal.connect(self.add_user_signal.emit)
        self.user_section.delete_user_signal.connect(self.delete_user_signal.emit)
        self.user_section.search_users_signal.connect(self.search_users_signal.emit)
        main_content.addWidget(self.user_section, 1)

        # RIGHT SIDE - Product Management Section
        self.product_section = ProductManagementSection()
        self.product_section.add_product_signal.connect(self.add_product_signal.emit)
        self.product_section.delete_product_signal.connect(self.delete_product_signal.emit)
        self.product_section.search_products_signal.connect(self.search_products_signal.emit)
        main_content.addWidget(self.product_section, 1)

        layout.addLayout(main_content)
        self.setLayout(layout)

    def update_users_table(self, users):
        """Delegate to user section"""
        self.user_section.update_users_table(users)

    def update_products_table(self, products):
        """Delegate to product section"""
        self.product_section.update_products_table(products)