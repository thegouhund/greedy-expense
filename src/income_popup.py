from PyQt5.QtCore import QDate, QTime
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


class InputIncomePopup(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__()
        self.data = data
        self.setWindowTitle("Input Income")
        self.setFixedWidth(350)
        self.setStyleSheet("background: white; border-radius: 12px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.dateLabel = SubtitleLabel("Tanggal", self)
        self.datePicker = CalendarPicker(self)
        layout.addWidget(self.dateLabel)
        layout.addWidget(self.datePicker)

        self.timeLabel = SubtitleLabel("Waktu", self)
        self.timePicker = TimePicker(self)
        layout.addWidget(self.timeLabel)
        layout.addWidget(self.timePicker)

        self.descLabel = SubtitleLabel("Deskripsi", self)
        self.descEdit = LineEdit(self)
        layout.addWidget(self.descLabel)
        layout.addWidget(self.descEdit)

        self.amountLabel = SubtitleLabel("Jumlah", self)
        self.amountEdit = LineEdit(self)
        self.amountEdit.setPlaceholderText("Masukkan jumlah pemasukan")
        layout.addWidget(self.amountLabel)
        layout.addWidget(self.amountEdit)

        self.saveButton = PrimaryPushButton("Simpan", self)
        self.saveButton.setIcon(FIF.SAVE)
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.clicked.connect(parent.loadIncomeData)
        layout.addWidget(self.saveButton)

        if self.data:
            self.setData(self.data)

    def setData(self, data):
        self.datePicker.setDate(QDate.fromString(data.get("date", ""), "dd-MM-yyyy"))
        self.timePicker.setTime(QTime.fromString(data.get("time", ""), "HH:mm"))
        self.descEdit.setText(data.get("desc", ""))
        self.amountEdit.setText(str(data.get("amount", "")))

    def saveData(self):
        if self.data:
            self.editData(self.data)
            self.close()
            return

        with open("income.json", "r") as f:
            existing_data = json.load(f)

        if existing_data and isinstance(existing_data, list):
            last_id = max([item.get("id", 0) for item in existing_data])
            new_id = last_id + 1
        else:
            new_id = 1

        data = {
            "id": new_id,
            "date": self.datePicker.getDate().toString("dd-MM-yyyy"),
            "time": self.timePicker.getTime().toString("HH:mm"),
            "desc": self.descEdit.text(),
            "amount": float(self.amountEdit.text()),
        }

        existing_data.append(data)

        with open("income.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        print(data)
        self.close()

    def editData(self, oldData):
        updated_data = {
            "id": oldData.get("id"),
            "date": self.datePicker.getDate().toString("dd-MM-yyyy"),
            "time": self.timePicker.getTime().toString("HH:mm"),
            "desc": self.descEdit.text(),
            "amount": float(self.amountEdit.text()),
        }

        with open("income.json", "r") as f:
            existing_data = json.load(f)

        for i, item in enumerate(existing_data):
            if item.get("id") == updated_data.get("id"):
                existing_data[i] = updated_data
                break

        with open("income.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        print(updated_data)
        self.close()
