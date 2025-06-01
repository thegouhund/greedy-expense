from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import (
    SubtitleLabel,
    PrimaryPushButton,
    CalendarPicker,
    LineEdit,
    TimePicker,
)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QWidget
import json


class InputExpensePopup(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__()
        self.data = data
        self.setWindowTitle("Input Expense")
        self.setFixedWidth(350)
        self.setStyleSheet("background: white; border-radius: 12px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.descLabel = SubtitleLabel("Deskripsi", self)
        self.descEdit = LineEdit(self)
        layout.addWidget(self.descLabel)
        layout.addWidget(self.descEdit)

        self.amountLabel = SubtitleLabel("Jumlah", self)
        self.amountEdit = LineEdit(self)
        self.amountEdit.setPlaceholderText("Masukkan jumlah pemasukan")
        layout.addWidget(self.amountLabel)
        layout.addWidget(self.amountEdit)

        self.priorityLabel = SubtitleLabel("Prioritas", self)
        self.priorityEdit = LineEdit(self)
        self.priorityEdit.setPlaceholderText("Masukkan prioritas pengeluaran")
        layout.addWidget(self.priorityLabel)
        layout.addWidget(self.priorityEdit)

        self.saveButton = PrimaryPushButton("Simpan", self)
        self.saveButton.setIcon(FIF.SAVE)
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.clicked.connect(parent.loadExpenseData)
        self.onlyInt = QIntValidator()
        self.priorityEdit.setValidator(self.onlyInt)
        layout.addWidget(self.saveButton)

        if self.data:
            self.setData(self.data)

    def setData(self, data):
        self.descEdit.setText(data.get("desc", ""))
        self.amountEdit.setText(str(data.get("amount", "")))
        self.priorityEdit.setText(str(data.get("priority", "")))

    def saveData(self):
        if self.data:
            self.editData(self.data)
            self.close()
            return

        with open("expense.json", "r") as f:
            existing_data = json.load(f)

        if existing_data and isinstance(existing_data, list):
            last_id = max([item.get("id", 0) for item in existing_data])
            new_id = last_id + 1
        else:
            new_id = 1

        amount = float(self.amountEdit.text())
        priority = float(self.priorityEdit.text())
        bcr = priority / amount if amount != 0 else 0

        data = {
            "id": new_id,
            "desc": self.descEdit.text(),
            "amount": amount,
            "priority": priority,
            "bcr": bcr,
        }

        existing_data.append(data)

        with open("expense.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        print(data)
        self.close()

    def editData(self, oldData):
        amount = float(self.amountEdit.text())
        priority = float(self.priorityEdit.text())
        bcr = priority / amount if amount != 0 else 0

        updated_data = {
            "id": oldData.get("id"),
            "desc": self.descEdit.text(),
            "amount": amount,
            "priority": priority,
            "bcr": bcr,
        }

        with open("expense.json", "r") as f:
            existing_data = json.load(f)

        for i, item in enumerate(existing_data):
            if item.get("id") == updated_data.get("id"):
                existing_data[i] = updated_data
                break

        with open("expense.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        print(updated_data)
        self.close()
