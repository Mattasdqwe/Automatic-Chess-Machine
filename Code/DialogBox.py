from PyQt5.QtCore import pyqtSignal, Qt, QSize, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QLabel, \
    QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog

from Board import Board, Piece
from GameState import GameState, Move
from Parameters import dialogbox_style, promo_white_style, promo_black_style, small_button_style
from Control import Control


class DialogBox(QDialog):

    returnSignal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(DialogBox, self).__init__(parent=parent)
        self.setStyleSheet(dialogbox_style)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)

        self.full_layout = QVBoxLayout()
        self.button_widget = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_widget.setLayout(self.button_layout)
        self.message = QLabel()
        self.message.setAlignment(Qt.AlignCenter)
        self.full_layout.addWidget(self.message, alignment=Qt.AlignCenter)
        self.full_layout.addWidget(self.button_widget)
        self.setLayout(self.full_layout)

    def setMessage(self, text):
        self.message.setText(text)

    def addButton(self, text, emit_value):
        button = QPushButton(text=text)
        button.setStyleSheet(small_button_style)
        button.clicked.connect(lambda: self.exit(emit_value))
        self.button_layout.addWidget(button)

    def exit(self, return_value):
        self.returnSignal.emit(return_value)
        self.close()


class PromotionDialog(QDialog):
    returnSignal = pyqtSignal(str)

    def __init__(self, parent=None, white=True):
        super(PromotionDialog, self).__init__(parent=parent)
        self.white = white

        if self.white:
            self.setStyleSheet(promo_white_style)
        else:
            self.setStyleSheet(promo_black_style)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)

        self.full_layout = QVBoxLayout()
        self.piece_widget = QWidget()
        self.piece_layout = QHBoxLayout()
        if self.white:
            self.piece_layout.addWidget(Piece(Piece.white_knight, draggable=False, parent=self))
            self.piece_layout.addWidget(Piece(Piece.white_bishop, draggable=False, parent=self))
            self.piece_layout.addWidget(Piece(Piece.white_rook, draggable=False, parent=self))
            self.piece_layout.addWidget(Piece(Piece.white_queen, draggable=False, parent=self))
        else:
            self.piece_layout.addWidget(Piece(Piece.black_knight, draggable=False, parent=self))
            self.piece_layout.addWidget(Piece(Piece.black_bishop, draggable=False, parent=self))
            self.piece_layout.addWidget(Piece(Piece.black_rook, draggable=False, parent=self))
            self.piece_layout.addWidget(Piece(Piece.black_queen, draggable=False, parent=self))
        self.piece_widget.setLayout(self.piece_layout)
        self.full_layout.addWidget(QLabel('Select Promotion Piece:'), alignment=Qt.AlignCenter)
        self.full_layout.addWidget(self.piece_widget)
        self.setLayout(self.full_layout)

    def mousePressEvent(self, event):
        if self.white:
            pieces = [Piece.white_knight, Piece.white_bishop, Piece.white_rook, Piece.white_queen]
        else:
            pieces = [Piece.black_knight, Piece.black_bishop, Piece.black_rook, Piece.black_queen]
        position = int(event.pos().x()/self.width() * len(pieces))
        if position < len(pieces):
            self.returnSignal.emit(pieces[position])
            self.close()
