"""Завдання 1. Вікно з базовими віджетами та компонуванням (PyQt6).

Використані віджети (10 типів): QLabel, QLineEdit, QComboBox, QCheckBox,
QRadioButton, QSlider, QSpinBox, QProgressBar, QTextEdit, QPushButton.
Layouts: QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout (вкладені).
Абсолютне позиціювання (move) не використовується.
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpinBox, QTextEdit, QVBoxLayout, QWidget,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 1: базові віджети та layouts")
        self.setMinimumSize(560, 520)

        # ---- Група 1: форма (QFormLayout) ----
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введіть ім'я та прізвище")
        self.name_edit.setToolTip("Поле для введення імені")

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Студент", "Викладач", "Гість"])
        self.role_combo.setCurrentIndex(0)
        self.role_combo.setToolTip("Оберіть роль користувача")

        self.age_spin = QSpinBox()
        self.age_spin.setRange(14, 100)
        self.age_spin.setValue(18)
        self.age_spin.setSuffix(" р.")
        self.age_spin.setToolTip("Вік від 14 до 100")

        form = QFormLayout()
        form.addRow("Ім'я:", self.name_edit)
        form.addRow("Роль:", self.role_combo)
        form.addRow("Вік:", self.age_spin)
        form_box = QGroupBox("Дані користувача")
        form_box.setLayout(form)

        # ---- Група 2: перемикачі (QHBoxLayout у QVBoxLayout) ----
        self.news_check = QCheckBox("Отримувати новини")
        self.news_check.setChecked(True)
        self.news_check.setToolTip("Підписка на розсилку")

        self.radio_light = QRadioButton("Світла тема")
        self.radio_dark = QRadioButton("Темна тема")
        self.radio_light.setChecked(True)
        self.radio_dark.setToolTip("Лише демонстраційний перемикач")

        radio_row = QHBoxLayout()
        radio_row.addWidget(self.radio_light)
        radio_row.addWidget(self.radio_dark)

        opts = QVBoxLayout()
        opts.addWidget(self.news_check)
        opts.addLayout(radio_row)  # вкладення layout у layout
        opts_box = QGroupBox("Параметри")
        opts_box.setLayout(opts)

        # ---- Група 3: повзунок + прогрес ----
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(30)
        self.slider.setToolTip("Рухайте повзунок — зміниться прогрес")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(30)
        self.slider.valueChanged.connect(self.progress.setValue)

        self.value_label = QLabel("Значення: 30")
        self.slider.valueChanged.connect(
            lambda v: self.value_label.setText(f"Значення: {v}"))

        prog_row = QHBoxLayout()
        prog_row.addWidget(self.slider, 3)
        prog_row.addWidget(self.value_label, 1)
        prog = QVBoxLayout()
        prog.addLayout(prog_row)
        prog.addWidget(self.progress)
        prog_box = QGroupBox("Прогрес")
        prog_box.setLayout(prog)

        # ---- Текстове поле ----
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Нотатки…")
        self.notes.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)

        # ---- Кнопки ----
        self.save_btn = QPushButton("Зберегти")
        self.save_btn.setToolTip("Показує підсумок у нотатках")
        self.save_btn.clicked.connect(self.show_summary)
        self.disabled_btn = QPushButton("Недоступна дія")
        self.disabled_btn.setEnabled(False)
        self.disabled_btn.setToolTip("Кнопка у стані disabled")

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.disabled_btn)
        btn_row.addWidget(self.save_btn)

        # ---- Головний layout ----
        top = QHBoxLayout()
        top.addWidget(form_box, 3)
        top.addWidget(opts_box, 2)

        root = QVBoxLayout(self)
        root.addWidget(QLabel("<h3>Демонстрація віджетів PyQt6</h3>"))
        root.addLayout(top)
        root.addWidget(prog_box)
        root.addWidget(QLabel("Нотатки:"))
        root.addWidget(self.notes, 1)
        root.addLayout(btn_row)

    def show_summary(self):
        theme = "світла" if self.radio_light.isChecked() else "темна"
        self.notes.setPlainText(
            f"Ім'я: {self.name_edit.text() or '—'}\n"
            f"Роль: {self.role_combo.currentText()}\n"
            f"Вік: {self.age_spin.value()}\n"
            f"Новини: {'так' if self.news_check.isChecked() else 'ні'}\n"
            f"Тема: {theme}\n"
            f"Прогрес: {self.progress.value()}%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
