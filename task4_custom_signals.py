"""Завдання 4. Кастомні сигнали та міжкомпонентна взаємодія.

Компоненти (кожен має власну відповідальність і НЕ знає про інші):
  InputPanel   — введення нового запису.
      itemSubmitted = pyqtSignal(int, str)  (пріоритет, текст)
        Значення: користувач підтвердив новий запис.
        Випромінюється: при натисканні «Додати» (або Enter) з непорожнім текстом.
        Джерело: InputPanel. Приймач: ResultsPanel.add_item (з'єднання у MainWindow).
  FilterPanel  — фільтр за підрядком і мінімальним пріоритетом.
      filterChanged = pyqtSignal(str, int)  (підрядок, мін. пріоритет)
        Значення: змінився критерій фільтрації.
        Випромінюється: при зміні тексту/пріоритету користувачем, а також один
        раз після програмного скидання (reset).
        Джерело: FilterPanel. Приймач: ResultsPanel.apply_filter.
  ResultsPanel — список записів.
      itemsChanged = pyqtSignal(list)  (список видимих рядків)
        Значення: змінився набір відображуваних записів.
        Випромінюється: після додавання запису або застосування фільтра.
        Джерело: ResultsPanel. Приймач: слот MainWindow.on_items_changed (статус).

Демонстрація:
  * disconnect — чекбокс «З'єднання Input→Results активне» підключає/відключає
    сигнал itemSubmitted від слота add_item: при вимкненні записи не додаються.
  * blockSignals — FilterPanel.reset() змінює віджети програмно під
    blockSignals(True), а потім випромінює filterChanged один раз.
    Лічильник «filterChanged отримано» у вікні показує ефект: без блокування
    було б 2 каскадні виклики, з блокуванням — 1.
"""
import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QPushButton, QSpinBox, QVBoxLayout, QWidget,
)


class InputPanel(QWidget):
    itemSubmitted = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Текст запису")
        self.priority = QSpinBox()
        self.priority.setRange(1, 5)
        self.priority.setPrefix("Пріоритет: ")
        self.add_btn = QPushButton("Додати")

        lay = QHBoxLayout(self)
        lay.addWidget(self.edit, 1)
        lay.addWidget(self.priority)
        lay.addWidget(self.add_btn)

        self.add_btn.clicked.connect(self._submit)
        self.edit.returnPressed.connect(self._submit)

    def _submit(self):
        text = self.edit.text().strip()
        if text:
            self.itemSubmitted.emit(self.priority.value(), text)
            self.edit.clear()


class FilterPanel(QWidget):
    filterChanged = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Фільтр за текстом")
        self.min_priority = QSpinBox()
        self.min_priority.setRange(1, 5)
        self.min_priority.setPrefix("Мін. пріоритет: ")
        self.reset_btn = QPushButton("Скинути фільтр")

        lay = QHBoxLayout(self)
        lay.addWidget(self.text_edit, 1)
        lay.addWidget(self.min_priority)
        lay.addWidget(self.reset_btn)

        self.text_edit.textChanged.connect(self._emit)
        self.min_priority.valueChanged.connect(self._emit)
        self.reset_btn.clicked.connect(self.reset)

    def _emit(self, *_):
        self.filterChanged.emit(self.text_edit.text(), self.min_priority.value())

    def reset(self):
        # Блокуємо сигнали віджетів, щоб не було двох каскадних emit
        self.text_edit.blockSignals(True)
        self.min_priority.blockSignals(True)
        self.text_edit.clear()
        self.min_priority.setValue(1)
        self.text_edit.blockSignals(False)
        self.min_priority.blockSignals(False)
        self._emit()  # один контрольований emit


class ResultsPanel(QWidget):
    itemsChanged = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._items = []  # список (priority, text)
        self._filter = ("", 1)
        self.list = QListWidget()
        lay = QVBoxLayout(self)
        lay.addWidget(self.list)

    def add_item(self, priority: int, text: str):
        self._items.append((priority, text))
        self._refresh()

    def apply_filter(self, text: str, min_priority: int):
        self._filter = (text.lower(), min_priority)
        self._refresh()

    def _refresh(self):
        sub, min_p = self._filter
        visible = [f"[{p}] {t}" for p, t in self._items
                   if p >= min_p and sub in t.lower()]
        self.list.clear()
        self.list.addItems(visible)
        self.itemsChanged.emit(visible)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 4: кастомні сигнали")
        self.setMinimumSize(560, 420)

        self.input_panel = InputPanel()
        self.filter_panel = FilterPanel()
        self.results = ResultsPanel()

        self.link_check = QCheckBox("З'єднання Input → Results активне (disconnect demo)")
        self.link_check.setChecked(True)
        self.status = QLabel("Видимих записів: 0")
        self.filter_counter = QLabel("filterChanged отримано: 0")
        self._filter_calls = 0

        root = QVBoxLayout(self)
        root.addWidget(self.input_panel)
        root.addWidget(self.filter_panel)
        root.addWidget(self.link_check)
        root.addWidget(self.results, 1)
        root.addWidget(self.status)
        root.addWidget(self.filter_counter)

        # Усі з'єднання — ЗОВНІ, у батьківському вікні
        self.input_panel.itemSubmitted.connect(self.results.add_item)
        self.filter_panel.filterChanged.connect(self.results.apply_filter)
        self.filter_panel.filterChanged.connect(self.count_filter_calls)
        self.results.itemsChanged.connect(self.on_items_changed)
        self.link_check.toggled.connect(self.toggle_link)

    def toggle_link(self, active: bool):
        if active:
            self.input_panel.itemSubmitted.connect(self.results.add_item)
        else:
            self.input_panel.itemSubmitted.disconnect(self.results.add_item)

    def count_filter_calls(self, *_):
        self._filter_calls += 1
        self.filter_counter.setText(f"filterChanged отримано: {self._filter_calls}")

    def on_items_changed(self, items: list):
        self.status.setText(f"Видимих записів: {len(items)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
