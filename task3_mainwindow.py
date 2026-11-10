"""Завдання 3. Простий текстовий редактор на QMainWindow.

menuBar (Файл, Правка, Довідка), QToolBar, statusBar, shortcuts,
стандартні діалоги QFileDialog та QMessageBox.
"""
import sys

from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, QFileDialog, QLabel, QMainWindow, QMessageBox, QTextEdit,
)


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 3: Текстовий редактор")
        self.resize(720, 480)
        self.current_file = None

        # Центральний віджет
        self.text = QTextEdit()
        self.setCentralWidget(self.text)

        # Рядок стану: постійна мітка з лічильником + тимчасові повідомлення
        self.count_label = QLabel("Символів: 0")
        self.statusBar().addPermanentWidget(self.count_label)
        self.statusBar().showMessage("Готово", 3000)
        self.text.textChanged.connect(self.update_count)

        self._create_actions()
        self._create_menus()
        self._create_toolbar()

    # ---------- Дії ----------
    def _create_actions(self):
        self.new_act = QAction("Новий", self)
        self.new_act.setShortcut(QKeySequence.StandardKey.New)       # Ctrl+N
        self.new_act.setStatusTip("Створити новий документ")
        self.new_act.triggered.connect(self.new_file)

        self.open_act = QAction("Відкрити…", self)
        self.open_act.setShortcut(QKeySequence.StandardKey.Open)     # Ctrl+O
        self.open_act.setStatusTip("Відкрити текстовий файл")
        self.open_act.triggered.connect(self.open_file)

        self.save_act = QAction("Зберегти", self)
        self.save_act.setShortcut(QKeySequence.StandardKey.Save)     # Ctrl+S
        self.save_act.setStatusTip("Зберегти документ")
        self.save_act.triggered.connect(self.save_file)

        self.exit_act = QAction("Вихід", self)
        self.exit_act.setShortcut("Ctrl+Q")
        self.exit_act.triggered.connect(self.close)

        self.clear_act = QAction("Очистити", self)
        self.clear_act.setShortcut("Ctrl+L")
        self.clear_act.setStatusTip("Очистити текст")
        self.clear_act.triggered.connect(self.text.clear)

        self.about_act = QAction("Про програму", self)
        self.about_act.setShortcut("F1")
        self.about_act.triggered.connect(self.show_about)

    def _create_menus(self):
        mb = self.menuBar()
        file_menu = mb.addMenu("&Файл")
        file_menu.addActions([self.new_act, self.open_act, self.save_act])
        file_menu.addSeparator()
        file_menu.addAction(self.exit_act)

        edit_menu = mb.addMenu("&Правка")
        edit_menu.addAction(self.clear_act)

        help_menu = mb.addMenu("&Довідка")
        help_menu.addAction(self.about_act)

    def _create_toolbar(self):
        tb = self.addToolBar("Основна")
        tb.addActions([self.new_act, self.open_act, self.save_act])
        tb.addSeparator()
        tb.addAction(self.clear_act)

    # ---------- Слоти ----------
    def update_count(self):
        n = len(self.text.toPlainText())
        self.count_label.setText(f"Символів: {n}")

    def new_file(self):
        self.text.clear()
        self.current_file = None
        self.setWindowTitle("ЛБ №4 — Завдання 3: Текстовий редактор")
        self.statusBar().showMessage("Створено новий документ", 3000)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Відкрити файл", "", "Текстові файли (*.txt);;Усі файли (*)")
        if not path:
            self.statusBar().showMessage("Відкриття скасовано", 3000)
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.text.setPlainText(f.read())
        except (OSError, UnicodeDecodeError) as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити файл:\n{e}")
            return
        self.current_file = path
        self.setWindowTitle(f"Редактор — {path}")
        self.statusBar().showMessage(f"Відкрито: {path}", 5000)

    def save_file(self):
        path = self.current_file
        if not path:
            path, _ = QFileDialog.getSaveFileName(
                self, "Зберегти файл", "", "Текстові файли (*.txt)")
            if not path:
                self.statusBar().showMessage("Збереження скасовано", 3000)
                return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text.toPlainText())
        except OSError as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти:\n{e}")
            return
        self.current_file = path
        self.statusBar().showMessage(f"Збережено: {path}", 5000)

    def show_about(self):
        QMessageBox.about(self, "Про програму",
                          "Простий текстовий редактор.\nЛБ №4, PyQt6.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Editor()
    w.show()
    sys.exit(app.exec())
