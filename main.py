import logging
from logging.handlers import RotatingFileHandler

import sys
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import (
    QSize,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QPushButton,
    QGroupBox,
    QLineEdit,
    QWidget,
    QLabel,
    QTextEdit,
    QFileDialog,
)

logger = logging.getLogger('main')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configure_window()
        layout = QGridLayout()

        logs_groupbox = self.configure_logs_groupbox()
        layout.addWidget(logs_groupbox)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.info('Application started')


    def configure_window(self):
        self.setFixedSize(QSize(400, 500))
        self.setWindowTitle('Party Bus v1.0')

    def configure_logs_groupbox(self):
        groupbox = QGroupBox('Logs')
        grid_layout = QGridLayout()
        groupbox.setLayout(grid_layout)

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        grid_layout.addWidget(self.logs_text, 0, 0, 1, 4)

        return groupbox

    def get_file_path(
        self,
        caption: str = 'Select File',
        filter: str = 'All Files (*)',
    ) -> str:

        path, _ = QFileDialog.getOpenFileName(
            self, caption, filter=filter,
        )
        return path

    def info(self, message: str):
        logger.info(message)
        message = f'{datetime.now().strftime("%H:%M:%S")} - {message}'
        self.logs_text.append(message)


if __name__ == '__main__':
    Path('logs').mkdir(exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG,
        handlers=[
            RotatingFileHandler('logs/logs.log', maxBytes=100000, backupCount=5)
        ]
    )
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
