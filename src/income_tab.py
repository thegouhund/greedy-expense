import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTableWidgetItem
from qfluentwidgets import (
    SubtitleLabel,
    TableWidget,
    PrimaryPushButton,
    TransparentPushButton,
)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from income_popup import InputIncomePopup


class IncomeTab(QFrame):
    def showInputIncomePopup(self, data=None):
        self.popup = InputIncomePopup(parent=self, data=data)
        self.popup.show()

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QVBoxLayout(self)
        self.hBoxLayout.setContentsMargins(24, 24, 24, 24)

        self.setObjectName(text.replace(" ", "-"))

        title = SubtitleLabel("Pemasukan", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.subtitle = SubtitleLabel("Total Uang: Rp 2.000.000", self)
        self.subtitle.setStyleSheet("font-size: 16px; color: black;")

        topRowWidget = QWidget(self)
        topRowLayout = QHBoxLayout(topRowWidget)
        topRowLayout.setContentsMargins(0, 0, 0, 0)
        topRowLayout.addWidget(self.subtitle)
        topRowLayout.addStretch()
        button = PrimaryPushButton(
            "Tambah Pemasukan",
            self,
            icon=FIF.ADD,
        )
        topRowLayout.addWidget(button)

        self.hBoxLayout.addWidget(title, 0, Qt.AlignTop)
        self.hBoxLayout.addWidget(topRowWidget, 0, Qt.AlignTop)

        self.table = TableWidget(self)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(TableWidget.SelectRows)
        self.table.setSelectionMode(TableWidget.SingleSelection)
        self.table.setEditTriggers(TableWidget.NoEditTriggers)

        self.hBoxLayout.addWidget(self.table, 1)

        buttonRowWidget = QWidget(self)
        buttonRowLayout = QHBoxLayout(buttonRowWidget)
        buttonRowLayout.setContentsMargins(0, 12, 0, 0)
        buttonRowLayout.addStretch()
        editButton = TransparentPushButton("Edit", self, icon=FIF.EDIT)
        deleteButton = TransparentPushButton("Delete", self, icon=FIF.DELETE)
        buttonRowLayout.addWidget(editButton)
        buttonRowLayout.addWidget(deleteButton)
        self.hBoxLayout.addWidget(buttonRowWidget, 0, Qt.AlignRight)

        # BUTTON CONNECTIONs
        button.clicked.connect(lambda: self.showInputIncomePopup())
        editButton.clicked.connect(self.editIncomeData)
        deleteButton.clicked.connect(self.deleteIncomeData)

        self.loadIncomeData()

    def loadIncomeData(self):
        with open("income.json", "r") as f:
            incomeInfos = json.load(f)

        self.incomeInfos = incomeInfos
        self.table.setRowCount(len(incomeInfos))
        self.table.setColumnCount(3)
        for i, expenseInfo in enumerate(incomeInfos):
            date_str = f"{expenseInfo.get('date', '')} {expenseInfo.get('time', '')}"
            desc = expenseInfo.get("desc", "")
            amount = str(expenseInfo.get("amount", ""))
            row = [date_str, desc, amount]
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(row[j]))
                self.table.setBorderVisible(True)

        self.table.setHorizontalHeaderLabels(["Time", "Description", "Amount"])
        self.table.resizeColumnsToContents()
        self.subtitle.setText(
            f"Total Uang: Rp {sum(float(item['amount']) for item in incomeInfos):,.2f}"
        )

    def editIncomeData(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            data = self.incomeInfos[selected_row]
            self.showInputIncomePopup(data)

    def deleteIncomeData(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            with open("income.json", "r") as f:
                existing_data = json.load(f)

            if existing_data and isinstance(existing_data, list):
                del existing_data[selected_row]

            with open("income.json", "w") as f:
                json.dump(existing_data, f, indent=4)

            self.loadIncomeData()
