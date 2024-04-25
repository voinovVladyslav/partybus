import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

from docx import Document
from PyQt6.QtCore import (
    QSize,
    QSettings,
    QObject,
    QThread,
    pyqtSignal,
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
from service.excel import (
    read_excel,
    aggregate_data,
    aggregate_links,
)
from service.writers.factory import get_writer
from service.links.factory import get_linker

COMPANY_NAME = 'Party Bus'
APPLICATION_NAME = 'Party Bus v1.0'

logger = logging.getLogger('main')


class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, main_window, document):
        super().__init__()
        self.mw: 'MainWindow' = main_window
        self.document = document
        self.is_finished = False

    def run(self):
        try:
            excel_data = read_excel(
                Path(str(self.mw.input_file_path))
            )
            data = aggregate_data(excel_data)
            self.mw.info(f'Loaded {len(data["cities"])} city names')
            self.mw.info(f'Company name: {data["company_name"]}')
            raw_links = read_excel(
                Path(str(self.mw.links_file_path)),
                sheet_name=1,
            )
            links = aggregate_links(
                raw_links, data['cities'], company_name=data['company_name']
            )

            for i, page_data in enumerate(data['pages'], 1):
                page_data['name'] = f'{i}. {page_data["name"]}'
                linker = get_linker(
                    page_number=i,
                    patterns=links,
                    cities=data['cities'],
                    company_name=data['company_name'],
                    regex_replace_count=1,
                    break_after_first_match=True,
                )
                kwargs = {
                    'document': self.document,
                    'data': page_data,
                    'banwords': self.mw.banwords,
                    'phone': data['phone'],
                    'linker': linker,
                }
                writer = get_writer(i, **kwargs)
                self.mw.info(
                    f'Writing page {i} using '
                    f'{writer.__class__.__name__} and '
                    f'{linker.__class__.__name__}...'
                )
                writer.write()

            self.is_finished = True
            self.finished.emit()

        except Exception as e:
            msg = f'An error occurred while generating the file: {e}'
            self.mw.info(msg)
            logger.exception(msg)

        finally:
            if not self.is_finished:
                self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configure_window()
        self.settings = QSettings(COMPANY_NAME, APPLICATION_NAME)

        self.input_file_path = None
        self.banwords_file_path = None
        self.banwords = []
        self.links_file_path = None

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
        self.preload_links()

    def configure_window(self):
        self.setFixedSize(QSize(600, 400))
        self.setWindowTitle('Party Bus v1.0')

    def handle_generate(self):
        self.thread_ = QThread()
        self.worker = Worker(self, Document())
        self.worker.moveToThread(self.thread_)

        self.enable_generate_button(False)
        self.thread_.started.connect(self.worker.run)
        self.worker.finished.connect(self.finished_generate)
        self.worker.finished.connect(self.thread_.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread_.finished.connect(self.thread_.deleteLater)
        self.thread_.start()

    def enable_generate_button(self, value: bool | None = None):
        if value is not None:
            self.generate_button.setEnabled(value)
            return
        self.generate_button.setEnabled(bool(self.input_file_path))

    def finished_generate(self):
        self.enable_generate_button(True)
        document = self.worker.document
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save File', filter='Document Files (*.docx)',
        )
        if not filename:
            self.info('No save file selected')
            return

        self.info(f'Saving document to {filename}...')
        document.save(filename)
        self.info('Done!')

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

        self.links_input_text = QLineEdit()
        self.links_input_text.setReadOnly(True)
        grid_layout.addWidget(QLabel('Links:'), 1, 0, 1, 1)
        grid_layout.addWidget(self.links_input_text, 1, 1, 1, 2)

        self.select_links_button = QPushButton('Browse')
        self.select_links_button.clicked.connect(
            self.handle_select_links_button
        )
        grid_layout.addWidget(self.select_links_button, 1, 3, 1, 1)

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

    def preload_links(self):
        try:
            prev_links_file_path = self.settings.value('links_file_path')
            if not prev_links_file_path:
                self.info('No previous links file found')
                return
            self.info(f'Loading previous links file {prev_links_file_path}')
            self.links_input_text.setText(prev_links_file_path)
            self.links_file_path = prev_links_file_path
        except Exception:
            self.info('Faled to load previous links file')

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

    def handle_select_links_button(self):
        file_path = self.get_file_path(
            caption='Select Links File',
            filter='Excel Files (*.xlsx *.xls *.xlsm *.xlsb)',
        )
        if not file_path:
            self.info('No links file selected')
            return
        self.settings.setValue('links_file_path', file_path)
        self.links_file_path = file_path
        self.links_input_text.setText(file_path)
        self.info(f'Selected links file: {file_path}')

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
