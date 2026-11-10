"""Завдання 2. Інтерактивна форма: сигнали й слоти, валідація, скидання.

З'єднання сигнал–слот:
 1. name_edit.textChanged  -> лямбда (оновлює мітку з лічильником символів)
 2. slider.valueChanged    -> лямбда (змінює текст мітки)
 3. agree_check.toggled    -> submit_btn.setEnabled (змінює стан іншого віджета)
 4. reset_btn.clicked      -> метод reset_form
 5. submit_btn.clicked     -> метод on_submit
 6. country_combo.currentTextChanged -> звичайна функція log_country (не метод)
Валідація винесена в окрему функцію validate().
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QMessageBox, QPushButton, QSlider, QSpinBox, QVBoxLayout,
    QWidget,
)

COUNTRIES = ["— оберіть —", "Україна", "Польща", "Німеччина", "Інша"]


def validate(name: str, age: int, country_index: int):
    """Єдина функція валідації. Повертає (ok, список_помилок)."""
    errors = []
    if not name.strip():
        errors.append("Ім'я не може бути порожнім.")
    elif len(name.strip()) < 2:
        errors.append("Ім'я має містити щонайменше 2 символи.")
    if not (16 <= age <= 99):
        errors.append("Вік має бути в межах 16–99.")
    if country_index == 0:
        errors.append("Оберіть країну зі списку.")
    return (not errors, errors)


def log_country(text: str):
    """Звичайна функція як слот (не метод класу)."""
    print(f"[log] Обрано країну: {text}")


class FormWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 2: інтерактивна форма")
        self.setMinimumWidth(420)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ваше ім'я")
        self.counter_label = QLabel("Символів: 0")

        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)
        self.age_spin.setValue(18)

        self.country_combo = QComboBox()
        self.country_combo.addItems(COUNTRIES)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 10)
        self.slider.setValue(5)
        self.slider_label = QLabel("Оцінка: 5")

        self.agree_check = QCheckBox("Я погоджуюсь з умовами")

        self.submit_btn = QPushButton("Підтвердити")
        self.submit_btn.setEnabled(False)
        self.reset_btn = QPushButton("Скинути")
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)

        form = QFormLayout()
        form.addRow("Ім'я:", self.name_edit)
        form.addRow("", self.counter_label)
        form.addRow("Вік:", self.age_spin)
        form.addRow("Країна:", self.country_combo)
        form.addRow("Оцінка:", self.slider)
        form.addRow("", self.slider_label)
        form.addRow("", self.agree_check)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.reset_btn)
        buttons.addWidget(self.submit_btn)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addLayout(buttons)
        root.addWidget(self.result_label)

        # ---- З'єднання сигнал–слот ----
        self.name_edit.textChanged.connect(
            lambda t: self.counter_label.setText(f"Символів: {len(t)}"))
        self.slider.valueChanged.connect(
            lambda v: self.slider_label.setText(f"Оцінка: {v}"))
        self.agree_check.toggled.connect(self.submit_btn.setEnabled)
        self.reset_btn.clicked.connect(self.reset_form)
        self.submit_btn.clicked.connect(self.on_submit)
        self.country_combo.currentTextChanged.connect(log_country)

    def on_submit(self):
        ok, errors = validate(self.name_edit.text(), self.age_spin.value(),
                              self.country_combo.currentIndex())
        if ok:
            self.result_label.setStyleSheet("color: green;")
            self.result_label.setText(
                f"✔ Дані прийнято: {self.name_edit.text().strip()}, "
                f"{self.age_spin.value()} р., {self.country_combo.currentText()}, "
                f"оцінка {self.slider.value()}.")
        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("✖ " + " ".join(errors))
            QMessageBox.warning(self, "Помилка валідації", "\n".join(errors))

    def reset_form(self):
        self.name_edit.clear()
        self.age_spin.setValue(18)
        self.country_combo.setCurrentIndex(0)
        self.slider.setValue(5)
        self.agree_check.setChecked(False)  # вимкне кнопку через toggled
        self.result_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FormWindow()
    w.show()
    sys.exit(app.exec())
