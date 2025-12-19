import sys
from PyQt6.QtWidgets import QApplication
from Controller.controllerFile import POSController
from Model.data_model import DataModel
from View import AdminView
from View.loginView import LoginView
from View.posView.mainPosView import mainPosView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create Model
    model = DataModel()

    # Create Views
    login_view = LoginView()
    admin_view = AdminView()
    pos_view = mainPosView()

    # Create Controller
    controller = POSController(model, login_view, admin_view, pos_view)

    # Run application
    controller.run()
    sys.exit(app.exec())