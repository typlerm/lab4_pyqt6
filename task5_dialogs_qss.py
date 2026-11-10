"""Завдання 5. Діалогові вікна та QSS-стилізація.

Діалоги:
  1) QMessageBox.question  — підтвердження видалення (стандартний)
  2) QInputDialog.getText  — зміна заголовка списку (діалог введення)
  3) AddPersonDialog(QDialog) — власний модальний діалог з кількома полями
QSS: глобальний stylesheet (QLabel, QPushButton, QLineEdit, QListWidget),
псевдостани :hover, :pressed, :focus, :disabled та окреме правило #dangerButton.
Кнопка «Перемкнути стиль» дозволяє зробити скріншоти ДО і ПІСЛЯ.
"""
import sys

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout,
    QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget, QMessageBox,
    QPushButton, QSpinBox, QVBoxLayout, QWidget,
)

APP_QSS = """
QWidget {
    background-color: #f4f6fb;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QLabel { color: #2c3e50; }
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #1a5fb4;
}
QLineEdit, QSpinBox, QComboBox {
    background: white;
    border: 2px solid #c5cbd9;
    border-radius: 6px;
    padding: 4px 8px;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: #1a73e8; }
QListWidget {
    background: white;
    border: 2px solid #c5cbd9;
    border-radius: 8px;
}
QListWidget::item { padding: 6px; }
QListWidget::item:selected { background: #1a73e8; color: white; }
QPushButton {
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
}
QPushButton:hover    { background-color: #1557b0; }
QPushButton:pressed  { background-color: #0d3c82; }
QPushButton:disabled { background-color: #b0b8c9; color: #eef0f5; }
QPushButton#dangerButton { background-color: #d93025; }
QPushButton#dangerButton:hover   { background-color: #b3261e; }
QPushButton#dangerButton:pressed { background-color: #8c1d18; }
"""


class AddPersonDialog(QDialog):
    """Власний модальний діалог: ім'я, вік, улюблений колір."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати людину")
        self.setModal(True)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ім'я")
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 120)
        self.age_spin.setValue(20)
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Червоний", "Зелений", "Синій", "Жовтий"])

        form = QFormLayout()
        form.addRow("Ім'я:", self.name_edit)
        form.addRow("Вік:", self.age_spin)
        form.addRow("Колір:", self.color_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(buttons)

    def _on_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Помилка", "Ім'я не може бути порожнім.")
            return
        self.accept()

    def get_data(self):
        return (self.name_edit.text().strip(), self.age_spin.value(),
                self.color_combo.currentText())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 5: діалоги та QSS")
        self.setMinimumSize(520, 420)
        self.styled = True

        self.title_label = QLabel("Список людей")
        self.title_label.setObjectName("titleLabel")
        self.info_label = QLabel("Додайте першу людину")
        self.list = QListWidget()

        self.add_btn = QPushButton("Додати (власний діалог)")
        self.rename_btn = QPushButton("Змінити заголовок (QInputDialog)")
        self.delete_btn = QPushButton("Видалити (QMessageBox)")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setEnabled(False)  # демонстрація :disabled
        self.toggle_btn = QPushButton("Перемкнути стиль")

        row = QHBoxLayout()
        row.addWidget(self.add_btn)
        row.addWidget(self.rename_btn)
        row2 = QHBoxLayout()
        row2.addWidget(self.delete_btn)
        row2.addWidget(self.toggle_btn)

        root = QVBoxLayout(self)
        root.addWidget(self.title_label)
        root.addWidget(self.list, 1)
        root.addWidget(self.info_label)
        root.addLayout(row)
        root.addLayout(row2)

        self.add_btn.clicked.connect(self.add_person)
        self.rename_btn.clicked.connect(self.rename_title)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.toggle_btn.clicked.connect(self.toggle_style)
        self.list.itemSelectionChanged.connect(
            lambda: self.delete_btn.setEnabled(bool(self.list.selectedItems())))

    def add_person(self):
        dlg = AddPersonDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, age, color = dlg.get_data()
            self.list.addItem(f"{name}, {age} р. — улюблений колір: {color}")
            self.info_label.setText(f"Останнє додавання: {name}")

    def rename_title(self):
        text, ok = QInputDialog.getText(self, "Новий заголовок",
                                        "Введіть заголовок:",
                                        text=self.title_label.text())
        if ok and text.strip():
            self.title_label.setText(text.strip())

    def delete_selected(self):
        item = self.list.currentItem()
        if item is None:
            return
        answer = QMessageBox.question(
            self, "Підтвердження", f"Видалити запис?\n\n{item.text()}")
        if answer == QMessageBox.StandardButton.Yes:
            self.list.takeItem(self.list.row(item))
            self.info_label.setText("Запис видалено")

    def toggle_style(self):
        self.styled = not self.styled
        QApplication.instance().setStyleSheet(APP_QSS if self.styled else "")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_QSS)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
