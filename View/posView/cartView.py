from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                             QLineEdit, QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor, QDoubleValidator
from View.colors import *


class cartView(QWidget):
    remove_from_cart_signal = pyqtSignal(int)
    complete_sale_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_total = 0.0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Cart label
        cart_label = QLabel("Cart")
        cart_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        cart_label.setStyleSheet("color: black;")
        layout.addWidget(cart_label)

        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(["Product", "Price", "Qty", "Total"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cart_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                color: black;
                font-family: Poppins;
                gridline-color: #ddd;
                selection-background-color: {ACCENT};
                selection-color: white;
            }}
            QTableWidget::item {{
                padding: 5px;
                border-bottom: 1px solid #eee;
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
                padding: 8px;
                border: none;
                border-right: 1px solid #005662;
            }}
            QHeaderView::section:last {{
                border-right: none;
            }}
        """)
        layout.addWidget(self.cart_table)

        # Total label
        self.total_label = QLabel("Total: ₱0.00")
        self.total_label.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        self.total_label.setStyleSheet(f"color: {PRIMARY};")
        layout.addWidget(self.total_label)

        # Cash input section
        cash_layout = QHBoxLayout()
        cash_label = QLabel("Cash:")
        cash_label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        cash_label.setStyleSheet("color: black;")
        cash_layout.addWidget(cash_label)

        self.cash_input = QLineEdit()
        self.cash_input.setPlaceholderText("Enter cash amount")
        # Add validator back for better UX
        validator = QDoubleValidator(0.0, 999999.99, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.cash_input.setValidator(validator)
        self.cash_input.textChanged.connect(self.calculate_change)
        self.cash_input.setStyleSheet("""
            QLineEdit {
                color: black;
                font-family: Poppins;
                font-size: 14px;
                background-color: white;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:hover {
                border: 2px solid #999;
            }
            QLineEdit:focus {
                border: 2px solid #007074;
                outline: none;
            }
        """)
        cash_layout.addWidget(self.cash_input)
        layout.addLayout(cash_layout)

        # Change label
        self.change_label = QLabel("Change: ₱0.00")
        self.change_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        self.change_label.setStyleSheet("color: #7CB9B4;")
        layout.addWidget(self.change_label)

        # Buttons
        btn_layout = QHBoxLayout()

        # Remove button with hover effect
        self.remove_btn = QPushButton("Remove Item")
        self.remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Poppins;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #6FAAA4;
                transform: scale(1.05);
            }}
            QPushButton:pressed {{
                background-color: #5A9489;
                padding: 11px 9px 9px 11px;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        self.remove_btn.clicked.connect(self.on_remove_from_cart)
        btn_layout.addWidget(self.remove_btn)

        # Complete sale button with hover effect
        self.complete_btn = QPushButton("Complete Sale")
        self.complete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-family: Poppins;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
                transform: scale(1.05);
            }}
            QPushButton:pressed {{
                background-color: #004450;
                padding: 11px 9px 9px 11px;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        self.complete_btn.clicked.connect(self.on_complete_sale)
        btn_layout.addWidget(self.complete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def calculate_change(self):
        """Calculate and display change based on cash input"""
        try:
            cash_text = self.cash_input.text().strip()

            # Don't process empty or invalid input
            if not cash_text or cash_text == '.' or cash_text == '-' or cash_text == '':
                self.change_label.setText("Change: ₱0.00")
                self.change_label.setStyleSheet("color: #7CB9B4;")
                return

            # Try to convert to float
            cash_amount = float(cash_text)

            # Ensure current_total is valid and convert to float
            if self.current_total is None or self.current_total < 0:
                self.current_total = 0.0

            # Convert current_total to float to match cash_amount type
            total_float = float(self.current_total)

            # Calculate change
            change = cash_amount - total_float

            if change >= 0:
                self.change_label.setText(f"Change: ₱{change:,.2f}")
                self.change_label.setStyleSheet("color: #7CB9B4;")
            else:
                self.change_label.setText(f"Insufficient: ₱{abs(change):,.2f}")
                self.change_label.setStyleSheet("color: #D32F2F;")

        except Exception as e:
            # Catch ALL errors and handle gracefully
            print(f"Error in calculate_change: {e}")
            self.change_label.setText("Change: ₱0.00")
            self.change_label.setStyleSheet("color: #7CB9B4;")

    def on_complete_sale(self):
        """Validate cash input before emitting complete sale signal"""
        # Safety check
        if not hasattr(self, 'cash_input') or self.cash_input is None:
            QMessageBox.warning(self, "Error", "Cash input not initialized")
            return

        # Get and validate cash input
        cash_text = self.cash_input.text().strip()

        if not cash_text or cash_text == '.' or cash_text == '-' or cash_text == '':
            QMessageBox.warning(self, "Error", "Please enter cash amount")
            self.cash_input.setFocus()
            return

        try:
            cash_amount = float(cash_text)
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Error", "Invalid cash amount")
            self.cash_input.setFocus()
            return

        # Convert current_total to float for comparison
        total_float = float(self.current_total)

        # Check if cash is sufficient
        if cash_amount < total_float:
            shortage = total_float - cash_amount
            QMessageBox.warning(self, "Insufficient Cash",
                                f"Cash is short by ₱{shortage:,.2f}")
            self.cash_input.setFocus()
            return

        # All validations passed, emit signal
        self.complete_sale_signal.emit()

    def update_cart(self, cart, total):
        """Update cart display"""
        self.current_total = total
        self.cart_table.setRowCount(len(cart))
        for i, item in enumerate(cart):
            product_item = QTableWidgetItem(item.product.name)
            product_item.setForeground(QColor("black"))
            self.cart_table.setItem(i, 0, product_item)

            price_item = QTableWidgetItem(f"₱{item.product.price:,.2f}")
            price_item.setForeground(QColor("black"))
            self.cart_table.setItem(i, 1, price_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setForeground(QColor("black"))
            self.cart_table.setItem(i, 2, qty_item)

            total_item = QTableWidgetItem(f"₱{item.get_total():,.2f}")
            total_item.setForeground(QColor("black"))
            self.cart_table.setItem(i, 3, total_item)

        self.total_label.setText(f"Total: ₱{total:,.2f}")
        # Recalculate change when cart updates
        self.calculate_change()

    def on_remove_from_cart(self):
        row = self.cart_table.currentRow()
        if row >= 0:
            self.remove_from_cart_signal.emit(row)

    def clear_cash_input(self):
        """Clear cash input and change display (useful after completing a sale)"""
        self.cash_input.clear()
        self.change_label.setText("Change: ₱0.00")
        self.change_label.setStyleSheet("color: #7CB9B4;")