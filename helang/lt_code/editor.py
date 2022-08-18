from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from .redirector import Redirector

FONT = QFont('Consolas')
FONT.setPointSize(18)


class _TextArea(QTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)


class _OutputArea(QTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)


class Editor(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.resize(800, 600)
        self.setFont(FONT)
        self._init_areas()

    def _init_areas(self):
        self._layout = QVBoxLayout()
        self._text_area = _TextArea(self)
        self._output_area = _OutputArea(self)
        self._layout.addWidget(self._text_area)
        self._layout.addWidget(self._output_area)
        self.setLayout(self._layout)

    @property
    def stdout(self):
        return Redirector(self._write_stdout_output)

    @property
    def stderr(self):
        return Redirector(self._write_stderr_output)

    @property
    def code(self):
        return self._text_area.toPlainText()

    def _write_stdout_output(self, s: str):
        self._output_area.insertPlainText(s)

    def _write_stderr_output(self, s: str):
        self._output_area.insertHtml(f'<div style="color: red">{s}</div>')

    def clear_output(self):
        self._output_area.clear()
