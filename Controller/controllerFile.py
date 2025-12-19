from PyQt6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget
from PyQt6.QtGui import QPalette, QColor
from View.colors import *
from View.transactionView import TransactionView
from View.adminMenuView import AdminMenuView
from View.overviewView import OverviewView


class POSController:
    def __init__(self, model, login_view, admin_view, pos_view):
        self.model = model
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("POS System")
        self.main_window.setGeometry(100, 100, 1200, 700)

        # Set color scheme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(BACKGROUND))
        self.main_window.setPalette(palette)

        # Views
        self.login_view = login_view
        self.admin_view = admin_view
        self.pos_view = pos_view

        # Create Admin Menu View
        self.admin_menu_view = AdminMenuView()

        # Create Transaction View
        self.transaction_view = TransactionView()

        self.overview_view = OverviewView()

        # Stack widget - add all views
        self.stack = QStackedWidget()
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.admin_menu_view)  # Add admin menu
        self.stack.addWidget(self.admin_view)
        self.stack.addWidget(self.pos_view)
        self.stack.addWidget(self.transaction_view)
        self.stack.addWidget(self.overview_view)

        self.main_window.setCentralWidget(self.stack)

        # Connect login signals
        self.login_view.login_signal.connect(self.handle_login)

        # Connect Admin Menu signals
        self.admin_menu_view.open_overview_signal.connect(self.handle_open_overview)
        self.admin_menu_view.open_transactions_signal.connect(self.handle_view_transactions)
        self.admin_menu_view.open_pos_signal.connect(self.handle_open_pos_from_menu)
        self.admin_menu_view.open_user_product_mgmt_signal.connect(self.handle_open_user_product_mgmt)
        self.admin_menu_view.logout_signal.connect(self.handle_logout)

        # Connect Admin View signals
        self.admin_view.add_user_signal.connect(self.handle_add_user)
        self.admin_view.add_product_signal.connect(self.handle_add_product)
        self.admin_view.delete_user_signal.connect(self.handle_delete_user)
        self.admin_view.delete_product_signal.connect(self.handle_delete_product)
        self.admin_view.search_users_signal.connect(self.handle_search_users)
        self.admin_view.search_products_signal.connect(self.handle_search_products)
        self.admin_view.logout_signal.connect(self.handle_logout)
        self.admin_view.open_pos_signal.connect(self.handle_open_pos)
        self.admin_view.view_transactions_signal.connect(self.handle_view_transactions)
        self.admin_view.view_overview_signal.connect(self.handle_open_overview)
        self.admin_view.back_to_admin_signal.connect(self.handle_back_to_admin_menu)

        self.overview_view.logout_signal.connect(self.handle_logout)
        self.overview_view.back_to_admin_signal.connect(self.handle_back_to_admin_menu)

        # Connect POS signals
        self.pos_view.add_to_cart_signal.connect(self.handle_add_to_cart)
        self.pos_view.remove_from_cart_signal.connect(self.handle_remove_from_cart)
        self.pos_view.complete_sale_signal.connect(self.handle_complete_sale)
        self.pos_view.logout_signal.connect(self.handle_logout)
        self.pos_view.back_to_admin_signal.connect(self.handle_back_to_admin_menu)

        # Connect Transaction View signals
        self.transaction_view.search_transactions_signal.connect(self.handle_search_transactions)
        self.transaction_view.delete_transaction_signal.connect(self.handle_delete_transaction)  # NEW
        self.transaction_view.back_to_admin_signal.connect(self.handle_back_to_admin_menu)

    def handle_login(self, username, password, role):
        """Handle user login - route admin to menu, staff to POS"""
        if self.model.authenticate(username, password):
            if self.model.current_user.role != role:
                QMessageBox.warning(self.main_window, "Error",
                                    f"User is not {role}")
                return

            if role == "admin":
                # Admin goes to Admin Menu
                self.stack.setCurrentWidget(self.admin_menu_view)
            else:
                # Staff goes directly to POS
                self.pos_view.set_admin_mode(False)
                self.pos_view.update_products(self.model.products)
                self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
                self.stack.setCurrentWidget(self.pos_view)
        else:
            QMessageBox.warning(self.main_window, "Error", "Invalid credentials")

    def handle_delete_transaction(self, order_id):
        """Handle transaction deletion with confirmation"""
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete transaction '{order_id}'?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.model.delete_transaction(order_id)
            if success:
                QMessageBox.information(self.main_window, "Success", message)
                # Refresh the transactions table
                self.transaction_view.update_transactions_table(self.model.transactions)
                # Also update overview if needed
                if hasattr(self, 'overview_view'):
                    users_count = len(self.model.users)
                    sold_items = sum(t.get_total_items() for t in self.model.transactions)
                    total_profit = sum(t.total_amount for t in self.model.transactions)
                    available_stock = sum(p.stock for p in self.model.products)
                    self.overview_view.update_overview(users_count, sold_items, total_profit, available_stock)
            else:
                QMessageBox.warning(self.main_window, "Error", message)

    def handle_open_overview(self):
        """FIXED: Open Overview with actual data"""
        # Calculate metrics
        users_count = len(self.model.users)

        # Calculate total sold items from all transactions
        sold_items = sum(t.get_total_items() for t in self.model.transactions)

        # Calculate total profit from all transactions
        total_profit = sum(t.total_amount for t in self.model.transactions)

        # Calculate available stock
        available_stock = sum(p.stock for p in self.model.products)

        # Update overview display
        self.overview_view.update_overview(users_count, sold_items, total_profit, available_stock)
        self.stack.setCurrentWidget(self.overview_view)

    def handle_open_user_product_mgmt(self):
        """Open User & Product Management view"""
        self.admin_view.update_users_table(self.model.users)
        self.admin_view.update_products_table(self.model.products)
        self.stack.setCurrentWidget(self.admin_view)

    def handle_open_pos_from_menu(self):
        """Open POS from admin menu"""
        self.pos_view.set_admin_mode(True)  # Admin mode
        self.pos_view.update_products(self.model.products)
        self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
        self.stack.setCurrentWidget(self.pos_view)

    def handle_open_pos(self):
        """Admin opens POS system from admin panel"""
        self.pos_view.set_admin_mode(True)
        self.pos_view.update_products(self.model.products)
        self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
        self.stack.setCurrentWidget(self.pos_view)

    def handle_back_to_admin_menu(self):
        """Return to admin menu"""
        self.stack.setCurrentWidget(self.admin_menu_view)

    def handle_back_to_admin(self):
        """Return to admin menu from anywhere"""
        self.stack.setCurrentWidget(self.admin_menu_view)

    def handle_add_user(self, username, password, role):
        if self.model.add_user(username, password, role):
            QMessageBox.information(self.main_window, "Success", "User added successfully")
            self.admin_view.update_users_table(self.model.users)
        else:
            QMessageBox.warning(self.main_window, "Error", "Username already exists")

    def handle_delete_user(self, username):
        reply = QMessageBox.question(self.main_window, "Confirm Delete",
                                     f"Are you sure you want to delete user '{username}'?",
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.model.delete_user(username)
            if success:
                QMessageBox.information(self.main_window, "Success", message)
                self.admin_view.update_users_table(self.model.users)
            else:
                QMessageBox.warning(self.main_window, "Error", message)

    def handle_search_users(self, search_term):
        filtered_users = self.model.search_users(search_term)
        self.admin_view.update_users_table(filtered_users)

    def handle_add_product(self, name, price, stock):
        self.model.add_product(name, price, stock)
        QMessageBox.information(self.main_window, "Success", "Product added successfully")
        self.admin_view.update_products_table(self.model.products)
        self.pos_view.update_products(self.model.products)

    def handle_delete_product(self, product_id):
        reply = QMessageBox.question(self.main_window, "Confirm Delete",
                                     f"Are you sure you want to delete this product?",
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.model.delete_product(product_id)
            QMessageBox.information(self.main_window, "Success", "Product deleted successfully")
            self.admin_view.update_products_table(self.model.products)
            self.pos_view.update_products(self.model.products)

    def handle_search_products(self, search_term):
        filtered_products = self.model.search_products(search_term)
        self.admin_view.update_products_table(filtered_products)

    def handle_add_to_cart(self, product_id, quantity):
        product = next((p for p in self.model.products if p.id == product_id), None)
        if product:
            if self.model.add_to_cart(product, quantity):
                self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
            else:
                QMessageBox.warning(self.main_window, "Error", "Insufficient stock")

    def handle_remove_from_cart(self, index):
        self.model.remove_from_cart(index)
        self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())

    def handle_delete_transaction(self, order_id):
        """Handle transaction deletion with confirmation"""
        print(f"Controller received delete request for: {order_id}")  # Debug print

        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete transaction '{order_id}'?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Default to No for safety
        )

        if reply == QMessageBox.StandardButton.Yes:
            print(f"User confirmed deletion of {order_id}")  # Debug print
            success, message = self.model.delete_transaction(order_id)
            if success:
                QMessageBox.information(self.main_window, "Success", message)
                # Refresh the transactions table
                self.transaction_view.update_transactions_table(self.model.transactions)
                # Also update overview if needed
                if hasattr(self, 'overview_view'):
                    users_count = len(self.model.users)
                    sold_items = sum(t.get_total_items() for t in self.model.transactions)
                    total_profit = sum(t.total_amount for t in self.model.transactions)
                    available_stock = sum(p.stock for p in self.model.products)
                    self.overview_view.update_overview(users_count, sold_items, total_profit, available_stock)
            else:
                QMessageBox.warning(self.main_window, "Error", message)
        else:
            print("User cancelled deletion")  # Debug print

    def handle_complete_sale(self):
        """Handle sale completion - validation already done in cart view"""
        try:
            # Check if cart is empty
            if not self.model.cart:
                QMessageBox.warning(self.main_window, "Error", "Cart is empty")
                return

            # Get cash amount (already validated in cartView)
            try:
                cash_text = self.pos_view.cart_view.cash_input.text().strip()
                cash_amount = float(cash_text)
            except (ValueError, AttributeError) as e:
                print(f"Error getting cash amount: {e}")
                QMessageBox.warning(self.main_window, "Error", "Invalid cash amount")
                return

            total = float(self.model.get_cart_total())  # Convert to float
            change = cash_amount - total

            print(f"About to show confirmation dialog - Total: {total}, Cash: {cash_amount}, Change: {change}")

            # Final confirmation with details
            reply = QMessageBox.question(
                self.main_window,
                "Confirm Sale",
                f"Total: ₱{total:,.2f}\n"
                f"Cash: ₱{cash_amount:,.2f}\n"
                f"Change: ₱{change:,.2f}\n\n"
                f"Complete this sale?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                print("User confirmed sale, attempting to complete...")

                # Complete the sale
                try:
                    self.model.complete_sale()
                    print("Sale completed in model successfully")
                except Exception as e:
                    print(f"Error in model.complete_sale(): {e}")
                    import traceback
                    traceback.print_exc()
                    QMessageBox.critical(self.main_window, "Error", f"Failed to complete sale: {str(e)}")
                    return

                # Update views
                try:
                    print("Updating views...")
                    self.pos_view.update_products(self.model.products)
                    self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
                    print("Views updated successfully")
                except Exception as e:
                    print(f"Error updating views: {e}")
                    import traceback
                    traceback.print_exc()

                # Clear cash input after successful sale
                try:
                    print("Clearing cash input...")
                    self.pos_view.cart_view.clear_cash_input()
                    print("Cash input cleared")
                except Exception as e:
                    print(f"Error clearing cash input: {e}")

                # Show success message with change
                try:
                    print("Showing success message...")
                    QMessageBox.information(
                        self.main_window,
                        "Sale Completed",
                        f"Sale completed successfully!\n\n"
                        f"Total: ₱{total:,.2f}\n"
                        f"Cash: ₱{cash_amount:,.2f}\n"
                        f"Change: ₱{change:,.2f}"
                    )
                    print("Success message shown")
                except Exception as e:
                    print(f"Error showing success message: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("User cancelled sale")

        except Exception as e:
            print(f"FATAL ERROR in handle_complete_sale: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_window, "Critical Error",
                                 f"An unexpected error occurred: {str(e)}")

    def handle_view_transactions(self):
        """Show transaction history"""
        self.transaction_view.update_transactions_table(self.model.transactions)
        self.stack.setCurrentWidget(self.transaction_view)

    def handle_search_transactions(self, search_term):
        """Search transactions"""
        filtered_transactions = self.model.search_transactions(search_term)
        self.transaction_view.update_transactions_table(filtered_transactions)

    def handle_back_to_admin_from_transactions(self):
        """Return to admin panel from transactions"""
        self.admin_view.update_users_table(self.model.users)
        self.admin_view.update_products_table(self.model.products)
        self.stack.setCurrentWidget(self.admin_view)

    def handle_logout(self):
        self.model.current_user = None
        self.model.clear_cart()
        self.login_view.clear_fields()
        self.stack.setCurrentWidget(self.login_view)

    def handle_view_overview(self):
        """Show overview with system statistics"""
        # Calculate metrics
        users_count = len(self.model.users)

        # Calculate total sold items from all transactions
        sold_items = sum(t.get_total_items() for t in self.model.transactions)

        # Calculate total profit from all transactions
        total_profit = sum(t.total_amount for t in self.model.transactions)

        # Calculate available stock
        available_stock = sum(p.stock for p in self.model.products)

        # Update overview display
        self.overview_view.update_overview(users_count, sold_items, total_profit, available_stock)
        self.stack.setCurrentWidget(self.overview_view)

    def handle_back_to_admin_from_overview(self):
        """Return to admin panel from overview"""
        self.admin_view.update_users_table(self.model.users)
        self.admin_view.update_products_table(self.model.products)
        self.stack.setCurrentWidget(self.admin_view)



    def run(self):
        self.main_window.show()