from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Click", self)
        self.button.clicked.connect(self.on_button_clicked)

        self.setCentralWidget(self.button)

    def on_button_clicked(self):
        pass

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
