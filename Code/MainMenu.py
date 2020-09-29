from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from Parameters import stylesheet, main_button_style


class MainMenu(QMainWindow):
    gotoSignal = pyqtSignal(str)

    def __init__(self):
        super(MainMenu, self).__init__()

        self.central_widget = QWidget()
        self.uiSetup()
        self.setCentralWidget(self.central_widget)

    def uiSetup(self):
        layout = QVBoxLayout()

        layout.addStretch()
        new_game_button = QPushButton()
        new_game_button.setText('New Game')
        new_game_button.clicked.connect(lambda: self.goto('player_selection'))
        new_game_button.setStyleSheet(main_button_style)
        layout.addWidget(new_game_button)
        layout.addStretch()

        resume_button = QPushButton()
        resume_button.setText('Resume Saved Game')
        # resume_button.clicked.connect(lambda: self.goto('resume_selection'))
        resume_button.setStyleSheet(main_button_style)
        layout.addWidget(resume_button)
        layout.addStretch()

        layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(layout)
        self.setStyleSheet(stylesheet)

    def goto(self, name):
        self.gotoSignal.emit(name)
