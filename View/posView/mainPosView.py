from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from View.colors import *
from View.posView.cartView import cartView


class mainPosView(QWidget):
    add_to_cart_signal = pyqtSignal(int, int)
    remove_from_cart_signal = pyqtSignal(int)
    complete_sale_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    back_to_admin_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_admin_mode = False
        self.cart_view = cartView()
        self.init_ui()

    def set_admin_mode(self, is_admin):
        """Show or hide the back to admin button based on user role"""
        self.is_admin_mode = is_admin
        self.back_to_admin_btn.setVisible(is_admin)

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)
        header = QLabel("Point of Sale")
        header.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Back to Admin button (hidden by default for staff)
        self.back_to_admin_btn = QPushButton("Back to Admin")
        self.back_to_admin_btn.setFixedWidth(130)
        self.back_to_admin_btn.setStyleSheet(f"""
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
        self.back_to_admin_btn.clicked.connect(self.back_to_admin_signal.emit)
        self.back_to_admin_btn.setVisible(False)
        header_layout.addWidget(self.back_to_admin_btn)

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

        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QHBoxLayout()

        # Products section (LEFT)
        products_layout = QVBoxLayout()
        products_label = QLabel("Products")
        products_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        products_label.setStyleSheet("color: black;")
        products_layout.addWidget(products_label)

        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Qty"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.products_table.setStyleSheet(f"""
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
        products_layout.addWidget(self.products_table)

        add_btn = QPushButton("Add to Cart")
        add_btn.setStyleSheet(f"""
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
            QPushButton:pressed {{
                background-color: #004450;
                padding: 11px 9px 9px 11px;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        add_btn.clicked.connect(self.on_add_to_cart)
        products_layout.addWidget(add_btn)

        content_layout.addLayout(products_layout, 2)

        # Cart section (RIGHT) - using CartView
        self.cart_view.remove_from_cart_signal.connect(self.remove_from_cart_signal.emit)
        self.cart_view.complete_sale_signal.connect(self.complete_sale_signal.emit)
        content_layout.addWidget(self.cart_view, 1)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def update_products(self, products):
        self.products_table.setRowCount(len(products))
        for i, product in enumerate(products):
            id_item = QTableWidgetItem(str(product.id))
            id_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 0, id_item)

            name_item = QTableWidgetItem(product.name)
            name_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 1, name_item)

            price_item = QTableWidgetItem(f"₱{product.price:,.2f}")
            price_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 2, price_item)

            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 3, stock_item)

            # QLineEdit for quantity input
            qty_input = QLineEdit()
            qty_input.setText("1")
            qty_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_input.setValidator(QIntValidator(1, max(1, product.stock)))
            qty_input.setMaximumWidth(200)
            qty_input.setStyleSheet("""
                            QLineEdit {
                                color: black;
                                font-family: Poppins;
                                background-color: white;
                                padding: 4px;
                                border: 1px solid #ccc;
                                border-radius: 3px;
                            }
                            QLineEdit:hover {
                                border: 1px solid #999;
                            }
                            QLineEdit:focus {
                                border: 1px solid #007074;
                                outline: none;
                            }
                        """)
            self.products_table.setCellWidget(i, 4, qty_input)

    def update_cart(self, cart, total):
        """Delegate to CartView"""
        self.cart_view.update_cart(cart, total)

    def on_add_to_cart(self):
        row = self.products_table.currentRow()
        if row >= 0:
            product_id = int(self.products_table.item(row, 0).text())
            qty_input = self.products_table.cellWidget(row, 4)
            quantity = int(qty_input.text()) if qty_input.text() else 1
            self.add_to_cart_signal.emit(product_id, quantity)