from PyQt5.QtCore import pyqtSignal, Qt, QSize, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QLabel, \
    QTableWidgetItem, QHeaderView, QAbstractItemView

from Board import Board, Piece
from GameState import GameState, Move
from Parameters import stylesheet, options_button_style, small_button_style, move_table_style, heading_label_style, \
    players
from Control import Control
from DialogBox import DialogBox, PromotionDialog
from Settings import Settings


class GameView(QMainWindow):
    gotoSignal = pyqtSignal(str)
    sendGameStateSignal = pyqtSignal(GameState)
    sendMoveSignal = pyqtSignal(Move)
    requestLegalMovesSignal = pyqtSignal(int, int)
    sendPromotionSignal = pyqtSignal(str)
    requestDrawSignal = pyqtSignal(bool)
    sendDrawSignal = pyqtSignal()
    sendResignSignal = pyqtSignal()

    def __init__(self):
        super(GameView, self).__init__()
        self.board = Board(drag_enabled=False)
        self.game_state = GameState()

        self.control_thread = QThread(parent=self)
        self.control = Control()
        self.controlSetup()

        self.central_widget = QWidget()
        self.uiSetup()
        self.setCentralWidget(self.central_widget)

        self.selectedSquare = None
        self.movesAvailable = []

        # settings
        self.allow_touchscreen_moves = True
        self.show_legal_moves = True
        self.show_last_move = True

    def uiSetup(self):
        layout = QHBoxLayout()

        # options display
        options_widget = QWidget()
        options_layout = QVBoxLayout()

        draw_button = QPushButton('Offer Draw')
        draw_button.setStyleSheet(options_button_style)
        draw_button.clicked.connect(self.requestDraw)
        resign_button = QPushButton('Resign')
        resign_button.clicked.connect(self.sendResigns)
        resign_button.setStyleSheet(options_button_style)
        settings_button = QPushButton()
        settings_button.clicked.connect(lambda: self.goto('settings'))
        settings_button.setIcon(QIcon('assets/settings.png'))
        settings_button.setIconSize(QSize(70, 70))
        settings_button.setStyleSheet(options_button_style)

        suboptions_widget = QWidget()
        suboptions_layout = QHBoxLayout()
        save_button = QPushButton('Save\nGame')
        save_button.setStyleSheet(small_button_style)
        new_game_button = QPushButton('New\nGame')
        new_game_button.clicked.connect(self.newGame)
        new_game_button.setStyleSheet(small_button_style)
        suboptions_layout.addWidget(save_button)
        suboptions_layout.addWidget(new_game_button)
        suboptions_widget.setLayout(suboptions_layout)

        options_layout.addStretch()
        options_layout.addWidget(draw_button)
        options_layout.addWidget(resign_button)
        options_layout.addWidget(settings_button)
        options_layout.addWidget(suboptions_widget)
        options_layout.addStretch()
        options_widget.setLayout(options_layout)

        # board display
        game_view_widget = QWidget()
        game_view_layout = QHBoxLayout()
        game_view_layout.addWidget(self.board)
        self.board.mouse_pressed_signal.connect(self.boardPressed)
        game_view_widget.setLayout(game_view_layout)

        # move display
        move_display_widget = QWidget()
        move_display_layout = QVBoxLayout()

        move_header = QLabel('Game Moves')
        move_header.setStyleSheet(heading_label_style)
        self.move_table = QTableWidget()
        self.move_table.setRowCount(0)
        self.move_table.setColumnCount(2)
        self.move_table.setShowGrid(False)
        self.move_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.move_table.horizontalHeader().hide()
        self.move_table.verticalHeader().setDefaultSectionSize(100)
        self.move_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.move_table.verticalHeader().setSectionsClickable(False)
        self.move_table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.move_table.setFocusPolicy(Qt.NoFocus)
        self.move_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.move_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.move_table.currentCellChanged.connect(self.cellSelected)
        self.move_table.setStyleSheet(move_table_style)

        move_display_layout.addWidget(move_header)
        move_display_layout.addWidget(self.move_table)
        move_display_widget.setLayout(move_display_layout)

        layout.addWidget(options_widget)
        layout.addStretch()
        layout.addWidget(game_view_widget, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(move_display_widget)
        self.central_widget.setLayout(layout)
        self.setStyleSheet(stylesheet)

    def displayBoard(self, board):
        for x in range(8):
            for y in range(8):
                if not self.board.flipped:
                    self.board.setPiece(board[y][x], x, y)
                else:
                    self.board.setPiece(board[y][x], 7-x, 7-y)

    def gameViewSetup(self):
        self.displayBoard(self.game_state.getBoard())

    def addMove(self, move):
        next_move = self.game_state.getNextToMove()
        if next_move or self.move_table.rowCount() == 0:
            self.move_table.insertRow(self.move_table.rowCount())
        self.game_state.addMove(move)

        item = QTableWidgetItem(move.stringRepresentation())
        item.setTextAlignment(Qt.AlignCenter)
        if next_move:
            self.move_table.setItem(self.move_table.rowCount()-1, 0, item)
            self.move_table.setCurrentCell(self.move_table.rowCount()-1, 0)
        else:
            self.move_table.setItem(self.move_table.rowCount()-1, 1, item)
            self.move_table.setCurrentCell(self.move_table.rowCount()-1, 1)

    def cellSelected(self, row, col, org_row, org_col):
        board = self.game_state.getBoardAtMove(2*row + col)
        self.displayBoard(board)

    def boardPressed(self, x, y):
        # return to current game view
        if self.game_state.next_to_move:
            self.move_table.setCurrentCell(self.move_table.rowCount()-1, 1)
            self.displayBoard(self.game_state.getBoard())
        else:
            self.move_table.setCurrentCell(self.move_table.rowCount()-1, 0)
            self.displayBoard(self.game_state.getBoard())

        x = int(x/600*8)
        y = int(y/600*8)
        if self.board.flipped:
            x = 7-x
            y = 7-y

        if (x, y) == self.selectedSquare:
            self.selectedSquare = None
            self.movesAvailable = []
            self.board.setMarkers(None)
            return
        for m in self.movesAvailable:
            if (x, y) == m.dest_square and self.allow_touchscreen_moves:
                self.selectedSquare = None
                self.movesAvailable = []
                self.board.setMarkers(None)
                if m.promotion_piece is not None:
                    m.setPromotionPending()
                self.sendMove(m)
                return
        if self.show_legal_moves:
            self.requestLegalMoves(x, y)
        self.selectedSquare = (x, y)

    def controlSetup(self):
        self.control_thread.start()
        self.control.moveToThread(self.control_thread)
        # send signals
        self.sendGameStateSignal.connect(self.control.receiveGameState)
        self.sendMoveSignal.connect(self.control.receiveMove)
        self.requestLegalMovesSignal.connect(self.control.sendLegalMoves)
        self.sendPromotionSignal.connect(self.control.receivePromotion)
        self.sendResignSignal.connect(self.control.receiveResign)
        self.requestDrawSignal.connect(self.control.receiveDrawOffer)
        self.sendDrawSignal.connect(self.control.receiveDrawAccepted)

        # receive signals

        self.control.illegalBoardSignal.connect(self.receiveIllegalBoardEncountered)
        self.control.sendMoveSignal.connect(self.receiveMove)
        self.control.sendLegalMovesSignal.connect(self.receiveLegalMoves)
        self.control.requestPromotionSignal.connect(self.requestPromotion)
        self.control.sendDrawOfferSignal.connect(self.receiveDrawOffer)
        self.control.sendDrawSignal.connect(self.receiveDraw)
        self.control.start.emit()

    # ui communication functions
    def receiveSettings(self, settings):
        settings = settings.split('\n')
        for setting in settings:
            setting = setting.split(':')
            if setting[0] == 'allow_touchscreen_moves':
                self.allow_touchscreen_moves = (setting[1] == 'True')
            if setting[0] == 'show_legal_moves':
                self.show_legal_moves = (setting[1] == 'True')
            if setting[0] == 'show_last_move':
                self.show_last_move = (setting[1] == 'True')

    def newGame(self):
        new_confirm = DialogBox(self)
        new_confirm.setMessage('Are you sure you want to start a new game?\nCurrent game progress will be erased!')
        new_confirm.addButton('Start', True)
        new_confirm.addButton('Cancel', False)

        def new_connect(confirm):
            if confirm:
                self.move_table.clear()
                self.move_table.setRowCount(0)
                self.goto('player_selection')

        new_confirm.returnSignal.connect(new_connect)
        new_confirm.exec()

    def receiveData(self, data):
        self.game_state.fromText(data)
        self.gameViewSetup()
        self.sendGameStateSignal.emit(self.game_state)

    def goto(self, name):
        self.gotoSignal.emit(name)

    def onShown(self):
        pass

    # control communication functions
    def receiveMove(self, move):
        self.addMove(move)

    def sendMove(self, move):
        self.sendMoveSignal.emit(move)

    def receiveLegalMoves(self, moves):
        marker_positions = []
        self.movesAvailable = []
        for move in moves:
            (x, y) = move.dest_square
            self.movesAvailable.append(move)
            if self.board.flipped:
                x = 7-x
                y = 7-y
            marker_positions.append((x, y))
        self.board.setMarkers(marker_positions)

    def requestLegalMoves(self, x, y):
        if self.game_state.getGameOver():
            return
        self.requestLegalMovesSignal.emit(x, y)

    def requestPromotion(self):
        promotion_dialog = PromotionDialog(parent=self, white=self.game_state.getNextToMove())
        promotion_dialog.returnSignal.connect(self.sendPromotion)
        promotion_dialog.exec()

    def sendPromotion(self, piece):
        self.sendPromotionSignal.emit(piece)

    def requestDraw(self):
        if self.game_state.getGameOver():
            return
        if self.game_state.next_to_move and self.game_state.white_player != players[0][0]:
            return
        if (not self.game_state.next_to_move) and self.game_state.black_player != players[0][0]:
            return
        draw_confirm = DialogBox(self)
        draw_confirm.setMessage('Are you sure you want to request a draw?')
        draw_confirm.addButton('Request Draw', True)
        draw_confirm.addButton('Cancel', False)

        def draw_connect(confirm):
            if not confirm:
                return
            self.requestDrawSignal.emit(self.game_state.next_to_move)

        draw_confirm.returnSignal.connect(draw_connect)
        draw_confirm.exec()

    def sendDraw(self):
        self.sendDrawSignal.emit()
        self.addMove(Move(None, None, None, None, None, None, draw=True))

    def receiveDrawOffer(self, color):
        if self.game_state.getGameOver():
            return
        if color:
            sender = 'White'
        else:
            sender = 'Black'
        offer_confirm = DialogBox(self)
        offer_confirm.setMessage('A draw offer from '+sender+' has been received')
        offer_confirm.addButton('Accept Draw', True)
        offer_confirm.addButton('Decline Draw', False)

        def offer_connect(confirm):
            if confirm:
                self.sendDraw()

        offer_confirm.returnSignal.connect(offer_connect)
        offer_confirm.exec()

    def receiveDraw(self, accepted):
        draw_status = DialogBox(self)
        draw_status.addButton('OK', None)

        if accepted:
            draw_status.setMessage('The draw has been accepted')
            self.addMove(Move(None, None, None, None, None, None, draw=True))
        else:
            draw_status.setMessage('The draw has been rejected')
        draw_status.exec()

    def sendResigns(self):
        if self.game_state.getGameOver():
            return
        if self.game_state.next_to_move and self.game_state.white_player != players[0][0]:
            return
        if (not self.game_state.next_to_move) and self.game_state.black_player != players[0][0]:
            return
        resign_confirm = DialogBox(self)
        resign_confirm.setMessage('Are you sure you want to resign?')
        resign_confirm.addButton('Resign', True)
        resign_confirm.addButton('Cancel', False)

        def resign_connect(confirm):
            if not confirm:
                return
            if self.game_state.next_to_move:
                self.addMove(Move(None, None, None, None, None, None, won_player=Move.won_player_black))
            else:
                self.addMove(Move(None, None, None, None, None, None, won_player=Move.won_player_white))
            self.sendResignSignal.emit()

        resign_confirm.returnSignal.connect(resign_connect)
        resign_confirm.exec()

    def receiveIllegalBoardEncountered(self):
        print('illegal board encountered')

    def receivePhysicalBoardMismatch(self):
        pass

    def sendMismatchResolved(self):
        pass

    def sendAutomaticSetup(self):
        pass



