import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (
    FluentWindow,
)
from qfluentwidgets import FluentIcon as FIF
from optimize_tab import OptimizeTab
from income_tab import IncomeTab


class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        self.expenseTab = OptimizeTab("Expense Tab", self)
        self.incomeTab = IncomeTab("Income Tab", self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.expenseTab, FIF.LIBRARY, "Expense Tab")
        self.addSubInterface(self.incomeTab, FIF.SHOPPING_CART, "Income Tab")

        # NOTE: enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowTitle("Optimasi Pengeluaran Mahasiswa")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
