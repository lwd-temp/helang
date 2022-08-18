from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction
from .editor import Editor
from .runner import Runner


class LTCodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LTCode')
        self.resize(800, 600)
        self._editor = Editor(self)
        self._init_layout()
        self._init_menu()

    def _init_layout(self):
        self.setCentralWidget(self._editor)

    def _init_menu(self):
        menu = self.menuBar()
        code_menu = menu.addMenu('&Code')

        run_action = QAction('&Run', self)
        run_action.triggered.connect(self._on_run_action_clicked)
        code_menu.addAction(run_action)

    def _on_run_action_clicked(self):
        self._editor.clear_output()
        runner = Runner(self._editor.code, self._editor.redirector)
        runner.start()
