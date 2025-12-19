from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QDialog, QTextEdit)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor, QPixmap
from View.colors import *


class TransactionDetailsDialog(QDialog):
    """Dialog to show detailed transaction information"""

    def __init__(self, transaction, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.setWindowTitle(f"Transaction Details - {transaction.order_id}")
        self.setMinimumSize(600, 400)
        # Add this line to set the dialog background color
        self.setStyleSheet(f"QDialog {{ background-color: {BACKGROUND}; }}")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel(f"Order: {self.transaction.order_id}")
        header.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")
        layout.addWidget(header)

        # Transaction info
        info_text = f"""
        <style>
            body {{ font-family: Poppins; }}
            .label {{ color: {PRIMARY}; font-weight: bold; }}
            .value {{ color: black; }}
        </style>
        <p><span class="label">Staff Name:</span> <span class="value">{self.transaction.staff_name}</span></p>
        <p><span class="label">Date:</span> <span class="value">{self.transaction.date}</span></p>
        <p><span class="label">Total Items:</span> <span class="value">{self.transaction.get_total_items()}</span></p>
        <p><span class="label">Total Amount:</span> <span class="value">₱{self.transaction.total_amount:,.2f}</span></p>
        """

        info_label = QLabel(info_text)
        info_label.setStyleSheet("background-color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)

        # Items table
        items_label = QLabel("Items Sold:")
        items_label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        items_label.setStyleSheet("color: black;")
        layout.addWidget(items_label)

        items_table = QTableWidget()
        items_table.setColumnCount(4)
        items_table.setHorizontalHeaderLabels(["ID", "Product", "Qty", "Price"])
        items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        items_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border-radius: 5px;
                color: black;
                font-family: Poppins;
            }}
            QHeaderView::section {{
                background-color: {PRIMARY};
                color: white;
                font-family: Poppins;
                font-weight: bold;
                padding: 5px;
            }}
        """)

        items_table.setRowCount(len(self.transaction.items))
        for i, item in enumerate(self.transaction.items):
            id_item = QTableWidgetItem(str(item['product_id']))
            id_item.setForeground(QColor("black"))
            items_table.setItem(i, 0, id_item)

            name_item = QTableWidgetItem(item['product_name'])
            name_item.setForeground(QColor("black"))
            items_table.setItem(i, 1, name_item)

            qty_item = QTableWidgetItem(str(item['quantity']))
            qty_item.setForeground(QColor("black"))
            items_table.setItem(i, 2, qty_item)

            price_item = QTableWidgetItem(f"₱{item['price']:,.2f}")
            price_item.setForeground(QColor("black"))
            items_table.setItem(i, 3, price_item)

        layout.addWidget(items_table)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Poppins;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)


class TransactionView(QWidget):
    search_transactions_signal = pyqtSignal(str)
    delete_transaction_signal = pyqtSignal(str)  # NEW: Signal for deleting transactions
    back_to_admin_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header with back button
        header_layout = QHBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        header = QLabel("Transaction History")
        header.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Back button
        back_btn = QPushButton("Back to Admin")
        back_btn.setFixedWidth(150)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-family: Poppins;
                font-weight: bold;
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
        back_btn.clicked.connect(self.back_to_admin_signal.emit)
        header_layout.addWidget(back_btn)

        layout.addLayout(header_layout)

        # Search
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setFont(QFont("Poppins", 12))
        search_label.setStyleSheet("color: black;")
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Order ID or Staff Name...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px;
                border: 2px solid {ACCENT};
                border-radius: 5px;
                font-family: Poppins;
                color: black;
                background-color: white;
            }}
        """)
        self.search_input.textChanged.connect(lambda: self.search_transactions_signal.emit(self.search_input.text()))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Transactions table - NOW WITH 8 COLUMNS (added Delete column)
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(8)
        self.transactions_table.setHorizontalHeaderLabels([
            "Order ID", "Staff Name", "Items Sold", "Item IDs", "Amount", "Date", "Actions", "Delete"
        ])
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.transactions_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border-radius: 5px;
                color: black;
                font-family: Poppins;
                selection-background-color: {ACCENT};
                selection-color: white;
            }}
            QTableWidget::item:hover {{
                background-color: {BACKGROUND};
            }}
            QTableWidget::item:selected {{
                background-color: {ACCENT};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {PRIMARY};
                color: white;
                font-family: Poppins;
                font-weight: bold;
                padding: 5px;
            }}
        """)
        layout.addWidget(self.transactions_table)

        self.setLayout(layout)

    def update_transactions_table(self, transactions):
        """Update the transactions table display"""
        self.transactions_table.setRowCount(len(transactions))
        for i, transaction in enumerate(transactions):
            # Order ID
            order_item = QTableWidgetItem(transaction.order_id)
            order_item.setForeground(QColor("black"))
            self.transactions_table.setItem(i, 0, order_item)

            # Staff Name
            staff_item = QTableWidgetItem(transaction.staff_name)
            staff_item.setForeground(QColor("black"))
            self.transactions_table.setItem(i, 1, staff_item)

            # Items Sold (count)
            items_count = QTableWidgetItem(str(transaction.get_total_items()))
            items_count.setForeground(QColor("black"))
            self.transactions_table.setItem(i, 2, items_count)

            # Item IDs
            item_ids = ", ".join(map(str, transaction.get_item_ids()))
            ids_item = QTableWidgetItem(item_ids)
            ids_item.setForeground(QColor("black"))
            self.transactions_table.setItem(i, 3, ids_item)

            # Amount
            amount_item = QTableWidgetItem(f"₱{transaction.total_amount:,.2f}")
            amount_item.setForeground(QColor("black"))
            self.transactions_table.setItem(i, 4, amount_item)

            # Date
            date_item = QTableWidgetItem(transaction.date)
            date_item.setForeground(QColor("black"))
            self.transactions_table.setItem(i, 5, date_item)

            # View Details button
            view_btn = QPushButton("View Details")
            view_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {PRIMARY};
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-family: Poppins;
                }}
                QPushButton:hover {{
                    background-color: #005662;
                }}
                QPushButton:focus {{
                    outline: none;
                    border: none;
                }}
            """)
            view_btn.clicked.connect(lambda checked, t=transaction: self.show_transaction_details(t))
            self.transactions_table.setCellWidget(i, 6, view_btn)

            # NEW: Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #DC3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-family: Poppins;
                }}
                QPushButton:hover {{
                    background-color: #C82333;
                }}
                QPushButton:focus {{
                    outline: none;
                    border: none;
                }}
            """)
            # Use a separate method to handle the click
            delete_btn.clicked.connect(lambda checked=False, oid=transaction.order_id: self.handle_delete_click(oid))
            self.transactions_table.setCellWidget(i, 7, delete_btn)

    def show_transaction_details(self, transaction):
        """Show detailed transaction dialog"""
        dialog = TransactionDetailsDialog(transaction, self)
        dialog.exec()

    def handle_delete_click(self, order_id):
        """Handle delete button click"""
        print(f"Delete button clicked for order: {order_id}")  # Debug print
        self.delete_transaction_signal.emit(order_id)