import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

from docx import Document
from PyQt6.QtCore import (
    QSize,
    QSettings,
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
from service.banwords import load_banwords
from service.excel import read_excel, aggregate_data
from service.writers.factory import get_writer

COMPANY_NAME = 'Party Bus'
APPLICATION_NAME = 'Party Bus v2.0'

logger = logging.getLogger('main')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configure_window()
        self.settings = QSettings(COMPANY_NAME, APPLICATION_NAME)

        self.input_file_path = None
        self.banwords_file_path = None
        self.banwords = []

        layout = QGridLayout()

        input_groupbox = self.configure_input_groupbox()
        layout.addWidget(input_groupbox)

        filter_groupbox = self.configure_filter_groupbox()
        layout.addWidget(filter_groupbox)

        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.handle_generate)
        self.enable_generate_button()
        layout.addWidget(self.generate_button)

        logs_groupbox = self.configure_logs_groupbox()
        layout.addWidget(logs_groupbox)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.info('Application started')
        self.preload_banwords()

    def configure_window(self):
        self.setFixedSize(QSize(400, 400))
        self.setWindowTitle(APPLICATION_NAME)

    def handle_generate(self):
        try:
            data = read_excel(Path(str(self.input_file_path)))
            data = aggregate_data(data)

            document = Document()
            for i, page_data in enumerate(data['pages'][1:18], 1):
                page_data['name'] = f'{i}. {page_data["name"]}'
                kwargs = {
                    'document': document,
                    'data': page_data,
                    'banwords': self.banwords,
                    'phone': data['phone'],
                }
                writer = get_writer(i, **kwargs)
                self.info(
                    f'Writing page {i} using {writer.__class__.__name__}...'
                )
                writer.write()

            filename, _ = QFileDialog.getSaveFileName(
                self, 'Save File', filter='Document Files (*.docx)',
            )
            if not filename:
                self.info('No save file selected')
                return

            self.info(f'Saving document to {filename}...')
            document.save(filename)
            self.info('Done!')

        except Exception as e:
            msg = f'An error occurred while generating the file: {e}'
            self.info(msg)
            logger.exception(msg)

    def enable_generate_button(self):
        self.generate_button.setEnabled(bool(self.input_file_path))

    def configure_input_groupbox(self):
        groupbox = QGroupBox('Input')
        grid_layout = QGridLayout()
        groupbox.setLayout(grid_layout)

        self.input_file_text = QLineEdit()
        self.input_file_text.setReadOnly(True)
        grid_layout.addWidget(QLabel('Input:'), 0, 0, 1, 1)
        grid_layout.addWidget(self.input_file_text, 0, 1, 1, 2)

        self.input_button = QPushButton('Browse')
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
        self.enable_generate_button()

    def configure_filter_groupbox(self):
        groupbox = QGroupBox('Filter')
        grid_layout = QGridLayout()
        groupbox.setLayout(grid_layout)

        self.banwords_input_text = QLineEdit()

        self.banwords_input_text.setReadOnly(True)
        grid_layout.addWidget(QLabel('Banwords:'), 0, 0, 1, 1)
        grid_layout.addWidget(self.banwords_input_text, 0, 1, 1, 2)

        self.select_bandwords_button = QPushButton('Browse')
        self.select_bandwords_button.clicked.connect(
            self.handle_select_bandwords_button
        )
        grid_layout.addWidget(self.select_bandwords_button, 0, 3, 1, 1)

        return groupbox

    def preload_banwords(self):
        try:
            prev_banwords_file_path = self.settings.value('banwords_file_path')
            if not prev_banwords_file_path:
                self.info('No previous banwords file found')
                return
            self.info(
                f'Loading previous banwords file {prev_banwords_file_path}'
            )
            self.banwords_input_text.setText(prev_banwords_file_path)
            self.banwords_file_path = prev_banwords_file_path
            self.banwords = load_banwords(prev_banwords_file_path)
            self.info(f'Loaded {len(self.banwords)} banwords')
        except Exception:
            self.info('Faled to load previous banwords file')

    def handle_select_bandwords_button(self):
        file_path = self.get_file_path(
            caption='Select Banwords File',
            filter='Text Files (*.txt)',
        )
        if not file_path:
            self.info('No banwords file selected')
            return
        self.banwords_file_path = file_path
        self.banwords_input_text.setText(file_path)
        self.info(f'Selected banwords file: {file_path}')

        self.settings.setValue('banwords_file_path', file_path)
        self.banwords = load_banwords(Path(file_path))
        self.info(f'Loaded {len(self.banwords)} banwords')

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
            RotatingFileHandler(
                'logs/logs.log', maxBytes=100000, backupCount=5
            )
        ]
    )
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
