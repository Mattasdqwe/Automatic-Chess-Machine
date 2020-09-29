from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QComboBox, QVBoxLayout, QLabel, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from Parameters import stylesheet, main_button_style, players, back_style, label_style
from GameState import GameState


class PlayerSelection(QMainWindow):
    gotoSignal = pyqtSignal(str)
    sendDataSignal = pyqtSignal(str, str)

    def __init__(self):
        super(PlayerSelection, self).__init__()

        self.game_state = GameState()

        self.central_widget = QWidget()
        self.uiSetup()
        self.setCentralWidget(self.central_widget)

    def uiSetup(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)

        # back button
        back_button = QPushButton()
        back_button.setIcon(QIcon('assets/back_button.png'))
        back_button.setIconSize(QSize(32, 32))
        back_button.clicked.connect(lambda: self.goto('main_menu'))
        back_button.setStyleSheet(back_style)

        # selection labels
        label_widget = QWidget()
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        white_label = QLabel('White Player')
        white_label.setAlignment(Qt.AlignCenter)
        white_label.setStyleSheet(label_style)
        label_layout.addWidget(white_label, alignment=Qt.AlignLeft)
        label_layout.addStretch()
        black_label = QLabel('Black Player')
        black_label.setAlignment(Qt.AlignCenter)
        black_label.setStyleSheet(label_style)
        label_layout.addWidget(black_label, alignment=Qt.AlignRight)
        label_layout.addStretch()
        label_layout.setAlignment(Qt.AlignTop)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_widget.setLayout(label_layout)

        # black and white selection combo-boxes
        selection_widget = QWidget()
        selection_layout = QHBoxLayout()
        selection_layout.addStretch()
        self.white_select = QComboBox()
        for p in players:
            self.white_select.addItem(QIcon(p[1]), p[0])
        self.white_select.setIconSize(QSize(64, 64))
        self.white_select.setMaxVisibleItems(4)
        # white_select.view().setCursor(Qt.BlankCursor)
        selection_layout.addWidget(self.white_select, alignment=Qt.AlignLeft)
        selection_layout.addStretch()

        self.black_select = QComboBox()
        for p in players:
            self.black_select.addItem(QIcon(p[1]), p[0])
        self.black_select.setIconSize(QSize(64, 64))
        self.black_select.setMaxVisibleItems(4)
        # black_select.view().setCursor(Qt.BlankCursor)
        selection_layout.addWidget(self.black_select, alignment=Qt.AlignRight)
        selection_layout.addStretch()
        selection_layout.setAlignment(Qt.AlignTop)
        selection_layout.setContentsMargins(0, 0, 0, 0)
        selection_widget.setLayout(selection_layout)

        # Board setup button
        board_setup_button = QPushButton()
        board_setup_button.setText('Board Setup')
        board_setup_button.clicked.connect(lambda: self.goto('board_setup'))
        board_setup_button.setStyleSheet(main_button_style)

        # Play button
        play_button = QPushButton()
        play_button.setText('Play')
        play_button.clicked.connect(lambda: self.goto('game_view'))
        play_button.clicked.connect(self.sendGameState)
        play_button.setStyleSheet(main_button_style)

        layout.addWidget(back_button, alignment=Qt.AlignLeft)
        layout.addWidget(label_widget)
        layout.addWidget(selection_widget)
        layout.addStretch()
        layout.addWidget(board_setup_button, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(play_button, alignment=Qt.AlignCenter)
        self.central_widget.setLayout(layout)
        self.setStyleSheet(stylesheet)

    def sendGameState(self):
        self.game_state.setWhitePlayer(self.white_select.currentText())
        self.game_state.setBlackPlayer(self.black_select.currentText())
        self.sendData('game_view', self.game_state.toText())

    # Used to get game state from board setup view
    def receiveData(self, data):
        self.game_state.fromText(data)

    def sendData(self, name, data):
        self.sendDataSignal.emit(name, data)

    def goto(self, name):
        self.gotoSignal.emit(name)
