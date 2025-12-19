from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QColor
from View.colors import *


class ProductManagementSection(QWidget):
    add_product_signal = pyqtSignal(str, float, int)
    delete_product_signal = pyqtSignal(int)
    search_products_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Add Product Section
        product_frame = QFrame()
        product_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        product_layout = QVBoxLayout(product_frame)

        product_title = QLabel("Add Product")
        product_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        product_title.setStyleSheet("color: black;")
        product_layout.addWidget(product_title)

        self.product_name = QLineEdit()
        self.product_name.setPlaceholderText("Product Name")
        self.product_name.setStyleSheet("font-family: Poppins; color: black; padding: 5px; background-color: white;")
        product_layout.addWidget(self.product_name)

        self.product_price = QLineEdit()
        self.product_price.setPlaceholderText("Price (numbers only)")
        self.product_price.setStyleSheet("font-family: Poppins; color: black; padding: 5px; background-color: white;")
        product_layout.addWidget(self.product_price)

        self.product_stock = QSpinBox()
        self.product_stock.setRange(0, 10000)
        self.product_stock.setPrefix("Stock: ")
        self.product_stock.setStyleSheet("font-family: Poppins; color: black; padding: 5px; background-color: white;")
        product_layout.addWidget(self.product_stock)

        add_product_btn = QPushButton("Add Product")
        add_product_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Poppins;
            }}
        """)
        add_product_btn.clicked.connect(self.on_add_product)
        product_layout.addWidget(add_product_btn)

        layout.addWidget(product_frame)

        # View Products Section
        view_products_frame = QFrame()
        view_products_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        view_products_layout = QVBoxLayout(view_products_frame)

        view_products_title = QLabel("Manage Products")
        view_products_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        view_products_title.setStyleSheet("color: black;")
        view_products_layout.addWidget(view_products_title)

        # Search products
        self.search_product_input = QLineEdit()
        self.search_product_input.setPlaceholderText("Search product name...")
        self.search_product_input.setStyleSheet(
            "font-family: Poppins; color: black; padding: 5px; background-color: white;")
        self.search_product_input.textChanged.connect(
            lambda: self.search_products_signal.emit(self.search_product_input.text()))
        view_products_layout.addWidget(self.search_product_input)

        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Actions"])
        self.products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.products_table.setStyleSheet("""
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
        view_products_layout.addWidget(self.products_table)

        layout.addWidget(view_products_frame)
        self.setLayout(layout)

    def on_add_product(self):
        name = self.product_name.text()
        try:
            price = float(self.product_price.text())
            stock = self.product_stock.value()
            if name and price > 0:
                self.add_product_signal.emit(name, price, stock)
                self.product_name.clear()
                self.product_price.clear()
                self.product_stock.setValue(0)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid price format")

    def update_products_table(self, products):
        """Update the products table display"""
        self.products_table.setRowCount(len(products))
        for i, product in enumerate(products):
            # ID
            id_item = QTableWidgetItem(str(product.id))
            id_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 0, id_item)

            # Name
            name_item = QTableWidgetItem(product.name)
            name_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 1, name_item)

            # Price
            price_item = QTableWidgetItem(f"₱{product.price:,.2f}")
            price_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 2, price_item)

            # Stock
            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setForeground(QColor("black"))
            self.products_table.setItem(i, 3, stock_item)

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
            """)
            delete_btn.clicked.connect(lambda checked, pid=product.id: self.delete_product_signal.emit(pid))
            self.products_table.setCellWidget(i, 4, delete_btn)