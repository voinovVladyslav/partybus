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
        self.input_file_path = None
        layout = QGridLayout()

        input_groupbox = self.configure_input_groupbox()
        layout.addWidget(input_groupbox)

        logs_groupbox = self.configure_logs_groupbox()
        layout.addWidget(logs_groupbox)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.info('Application started')

    def configure_window(self):
        self.setFixedSize(QSize(400, 500))
        self.setWindowTitle('Party Bus v1.0')

    def configure_input_groupbox(self):
        groupbox = QGroupBox('Input')
        grid_layout = QGridLayout()
        groupbox.setLayout(grid_layout)

        self.input_file_text = QLineEdit()
        self.input_file_text.setReadOnly(True)
        grid_layout.addWidget(QLabel('Input:'), 0, 0, 1, 1)
        grid_layout.addWidget(self.input_file_text, 0, 1, 1, 2)

        self.input_button = QPushButton('Select File')
        self.input_button.clicked.connect(self.handle_input_button)
        grid_layout.addWidget(self.input_button, 0, 3, 1, 1)

        return groupbox

    def handle_input_button(self):
        file_path = self.get_file_path(
            caption='Select Data File',
            filter='Excel Files (*.xlsx *.xls *.xlsm *.xlsb)',
        )
        if not file_path:
            self.info('No input file selected')
            return
        self.input_file_path = file_path
        self.input_file_text.setText(file_path)
        self.info(f'Selected input file: {file_path}')

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
