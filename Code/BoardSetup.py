from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox

from Board import Board, PieceHolder
from GameState import GameState
from Parameters import stylesheet, back_style, check_style_white, check_style_black, small_button_style, \
    check_style_move


class BoardSetup(QMainWindow):
    gotoSignal = pyqtSignal(str)
    sendDataSignal = pyqtSignal(str, str)

    def __init__(self):
        super(BoardSetup, self).__init__()

        self.central_widget = QWidget()
        self.uiSetup()
        self.setCentralWidget(self.central_widget)

    def uiSetup(self):
        layout = QVBoxLayout()

        # back button
        back_button = QPushButton()
        back_button.setIcon(QIcon('assets/back_button.png'))
        back_button.setIconSize(QSize(32, 32))
        back_button.clicked.connect(lambda: self.goto('player_selection'))
        back_button.clicked.connect(self.sendGameState)
        back_button.setStyleSheet(back_style)

        # board display
        board_contents_widget = QWidget()
        board_contents_layout = QHBoxLayout()
        white_pieces = PieceHolder(is_white=True)
        black_pieces = PieceHolder(is_white=False)
        self.board = Board()
        self.board.standardSetup()

        # castling availabilities
        castling_widget = QWidget()
        castling_layout = QVBoxLayout()
        self.white_castle_kingside = QCheckBox('Kingside \nCastle')
        self.white_castle_kingside.setStyleSheet(check_style_white)
        self.white_castle_kingside.setChecked(True)
        self.white_castle_queenside = QCheckBox('Queenside \nCastle')
        self.white_castle_queenside.setStyleSheet(check_style_white)
        self.white_castle_queenside.setChecked(True)
        self.black_castle_kingside = QCheckBox('Kingside \nCastle')
        self.black_castle_kingside.setStyleSheet(check_style_black)
        self.black_castle_kingside.setChecked(True)
        self.black_castle_queenside = QCheckBox('Queenside \nCastle')
        self.black_castle_queenside.setStyleSheet(check_style_black)
        self.black_castle_queenside.setChecked(True)
        castling_layout.addWidget(self.white_castle_kingside)
        castling_layout.addStretch()
        castling_layout.addWidget(self.white_castle_queenside)
        castling_layout.addStretch()
        castling_layout.addWidget(self.black_castle_kingside)
        castling_layout.addStretch()
        castling_layout.addWidget(self.black_castle_queenside)
        castling_widget.setLayout(castling_layout)

        # editing options
        editing_options_widget = QWidget()
        editing_options_layout = QVBoxLayout()
        clear_board = QPushButton('Clear\nBoard')
        clear_board.clicked.connect(self.board.clearBoard)
        clear_board.setStyleSheet(small_button_style)
        reset_board = QPushButton('Reset\nBoard')
        reset_board.clicked.connect(self.board.standardSetup)
        reset_board.setStyleSheet(small_button_style)
        flip_board = QPushButton('Flip\nBoard')
        flip_board.clicked.connect(self.board.flipBoard)
        flip_board.setStyleSheet(small_button_style)
        self.white_to_move = QCheckBox('Next\nMove             ')
        self.white_to_move.setStyleSheet(check_style_move)
        self.white_to_move.setChecked(True)
        editing_options_layout.addWidget(clear_board)
        editing_options_layout.addWidget(reset_board)
        editing_options_layout.addWidget(flip_board)
        editing_options_layout.addWidget(self.white_to_move)
        editing_options_widget.setLayout(editing_options_layout)

        # adding to contents layout
        board_contents_layout.addWidget(castling_widget)
        board_contents_layout.addStretch()
        board_contents_layout.addWidget(white_pieces)
        board_contents_layout.addStretch()
        board_contents_layout.addWidget(self.board)
        board_contents_layout.addStretch()
        board_contents_layout.addWidget(black_pieces)
        board_contents_layout.addStretch()
        board_contents_layout.addWidget(editing_options_widget)
        board_contents_widget.setLayout(board_contents_layout)

        layout.addWidget(back_button)
        layout.addWidget(board_contents_widget, alignment=Qt.AlignCenter)
        self.central_widget.setLayout(layout)
        self.setStyleSheet(stylesheet)

    def sendGameState(self):
        game_state = GameState()

        game_state.setBoard(self.board.getStringRepresentation())
        game_state.setWhiteKingsideCastle(self.white_castle_kingside.isChecked())
        game_state.setWhiteQueensideCastle(self.white_castle_queenside.isChecked())
        game_state.setBlackKingsideCastle(self.black_castle_kingside.isChecked())
        game_state.setBlackQueensideCastle(self.black_castle_queenside.isChecked())
        game_state.setNextToMove(self.white_to_move.isChecked())

        self.sendData('player_selection', game_state.toText())

    def sendData(self, name, data):
        self.sendDataSignal.emit(name, data)

    def goto(self, name):
        self.gotoSignal.emit(name)
