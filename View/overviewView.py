import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPixmap, QColor
from View.colors import *

class MetricBox(QFrame):
    """A styled box to display a metric with icon and value"""

    def __init__(self, title, value, icon_path):
        super().__init__()
        self.title = title
        self.value_text = value
        self.icon_path = icon_path
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 14px;
                padding: 12px;
            }}
            QFrame:hover {{
                background-color: #fbffff;
                border: 1px solid {ACCENT};
            }}
        """)
        self.setMinimumSize(260, 160)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(self.icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        layout.addSpacing(10)

        # Value
        self.value_label = QLabel(self.value_text)
        self.value_label.setFont(QFont("Poppins", 26, QFont.Weight.DemiBold))
        self.value_label.setStyleSheet(f"color: {PRIMARY};")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setWordWrap(False)
        layout.addWidget(self.value_label)

        layout.addSpacing(3)

        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Poppins", 14))
        title_label.setStyleSheet("color: #666666;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addStretch()
        self.setLayout(layout)

        # convenience tooltip
        self.setToolTip(f"{self.title}: {self.value_text}")

    def update_value(self, value):
        """Update the displayed value"""
        self.value_label.setText(value)


class OverviewView(QWidget):
    logout_signal = pyqtSignal()
    back_to_admin_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        # page background
        self.setStyleSheet(f"background-color: {BACKGROUND};")

        # Header with logo and buttons
        header_layout = QHBoxLayout()

        # Logo (use relative path so UI works across machines)
        logo_label = QLabel()
        icons_dir = os.path.join(os.path.dirname(__file__), "icons")
        logo_path = os.path.join(icons_dir, "T360logo.png")
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        title_group = QVBoxLayout()
        header = QLabel("System Overview")
        header.setFont(QFont("Poppins", 22, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")
        title_group.addWidget(header)
        header_layout.addLayout(title_group)

        header_layout.addStretch()

        # Back to Admin button
        back_btn = QPushButton("Back to Admin")
        back_btn.setFixedWidth(150)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
                font-family: Poppins;
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
        back_btn.clicked.connect(self.back_to_admin_signal.emit)
        header_layout.addWidget(back_btn)

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

        # Metrics grid (responsive: will flow into available space)
        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(20)

        # Create metric boxes
        self.users_box = MetricBox(
            "Total Users",
            "0",
            os.path.join(icons_dir, "userHollow.png")
        )

        self.sold_items_box = MetricBox(
            "Sold Items",
            "0",
            os.path.join(icons_dir, "saleHollow.png")
        )

        self.profit_box = MetricBox(
            "Total Profit",
            "₱0.00",
            os.path.join(icons_dir, "profit.png")
        )

        self.stock_box = MetricBox(
            "Available Stock",
            "0",
            os.path.join(icons_dir, "inventoryHollow.png")
        )

        # Add boxes to grid (2x2 layout)
        metrics_layout.addWidget(self.users_box, 0, 0)
        metrics_layout.addWidget(self.sold_items_box, 0, 1)
        metrics_layout.addWidget(self.profit_box, 1, 0)
        metrics_layout.addWidget(self.stock_box, 1, 1)

        layout.addLayout(metrics_layout)
        layout.addStretch()

        self.setLayout(layout)

    def update_overview(self, users_count, sold_items, total_profit, available_stock):
        """Update all metrics"""
        self.users_box.update_value(str(users_count))
        self.sold_items_box.update_value(str(sold_items))
        self.profit_box.update_value(f"₱{total_profit:,.2f}")
        self.stock_box.update_value(str(available_stock))