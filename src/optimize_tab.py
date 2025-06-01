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
import json
from expense_popup import InputExpensePopup
from utils import format_rupiah


class OptimizeTab(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QVBoxLayout(self)
        self.hBoxLayout.setContentsMargins(24, 24, 24, 24)

        self.setObjectName(text.replace(" ", "-"))

        title = SubtitleLabel("Optimasi", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.subtitle = SubtitleLabel("Total Uang: ", self)
        self.subtitle.setStyleSheet("font-size: 16px; color: black;")
        self.remaining_budget_label = SubtitleLabel("Sisa Uang: ", self)
        self.remaining_budget_label.setStyleSheet("font-size: 16px; color: black;")

        topRowWidget = QWidget(self)
        topRowLayout = QHBoxLayout(topRowWidget)
        topRowLayout.setContentsMargins(0, 0, 0, 0)
        topRowLayout.addWidget(self.subtitle)
        topRowLayout.addStretch()
        button = PrimaryPushButton(
            "Tambah Pengeluaran",
            self,
            icon=FIF.ADD,
        )
        topRowLayout.addWidget(button)

        self.hBoxLayout.addWidget(title, 0, Qt.AlignTop)
        self.hBoxLayout.addWidget(topRowWidget, 0, Qt.AlignTop)
        self.hBoxLayout.addWidget(self.remaining_budget_label, 0, Qt.AlignTop)

        self.table = TableWidget(self)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.setHorizontalHeaderLabels(
            [
                "Date",
                "Description",
                "Estimated Amount",
                "Priority",
                "Benefit-Cost Ratio",
            ]
        )
        self.table.verticalHeader().hide()
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(TableWidget.SelectRows)
        self.table.setSelectionMode(TableWidget.SingleSelection)
        self.table.setEditTriggers(TableWidget.NoEditTriggers)
        self.table.currentItemChanged.connect(self.loadExpenseData)

        buttonRowWidget = QWidget(self)
        buttonRowLayout = QHBoxLayout(buttonRowWidget)
        buttonRowLayout.setContentsMargins(0, 12, 0, 0)
        buttonRowLayout.addStretch()
        editButton = TransparentPushButton("Edit", self, icon=FIF.EDIT)
        deleteButton = TransparentPushButton("Delete", self, icon=FIF.DELETE)
        buttonRowLayout.addWidget(editButton)
        buttonRowLayout.addWidget(deleteButton)

        self.hBoxLayout.addWidget(self.table, 1)
        self.hBoxLayout.addWidget(buttonRowWidget, 0, Qt.AlignRight)

        # BUTTON CONNECTIONs
        button.clicked.connect(self.showInputExpensePopup)
        editButton.clicked.connect(self.editIncomeData)
        deleteButton.clicked.connect(self.deleteExpenseData)
        self.loadExpenseData()

    def loadExpenseData(self):
        with open("expense.json", "r") as f:
            self.expenseInfos = json.load(f)

        with open("income.json", "r") as f:
            incomeInfos = json.load(f)

        total_income = sum(float(item["amount"]) for item in incomeInfos)
        self.expenseInfos.sort(key=lambda x: float(x.get("bcr", 0)), reverse=True)

        self.table.setRowCount(len(self.expenseInfos))
        self.table.setColumnCount(4)

        temp_budget = total_income
        for i, expenseInfo in enumerate(self.expenseInfos):
            desc = expenseInfo.get("desc", "")
            amount_val = expenseInfo.get("amount", "")
            amount = format_rupiah(amount_val)
            priority = str(expenseInfo.get("priority", ""))
            bcr = str(expenseInfo.get("bcr", ""))
            row = [desc, amount, priority, bcr]

            can_be_paid = temp_budget >= float(amount_val)
            if can_be_paid:
                temp_budget -= float(amount_val)

            for j in range(4):
                item = QTableWidgetItem(row[j])
                if can_be_paid:
                    item.setBackground(Qt.green)
                self.table.setItem(i, j, item)

        self.table.setHorizontalHeaderLabels(
            ["Description", "Estimated Amount", "Priority", "Benefit-Cost Ratio"]
        )
        self.table.resizeColumnsToContents()

        self.subtitle.setText(f"Total Uang: Rp {total_income:,.2f}")
        self.remaining_budget_label.setText(f"Sisa Budget: Rp {temp_budget:,.2f}")

    def deleteExpenseData(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            selected_id = self.expenseInfos[selected_row].get("id")
            if selected_id is None:
                return

            with open("expense.json", "r") as f:
                existing_data = json.load(f)

            for i in range(len(existing_data)):
                if existing_data[i].get("id") == selected_id:
                    del existing_data[i]

        with open("expense.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        self.loadExpenseData()

    def editIncomeData(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            data = self.expenseInfos[selected_row]
            self.showInputExpensePopup(data)

    def showInputExpensePopup(self, data=None):
        self.popup = InputExpensePopup(parent=self, data=data)
        self.popup.show()
