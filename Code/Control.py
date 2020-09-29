from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot, QCoreApplication

from Parameters import players, engine_strength
from GameState import GameState, Move
from Pathing import Pathing
from PieceDetection import PieceDetection
import chess
import chess.engine
import platform
import threading



class Control(QObject):
    # emitter signals
    sendMoveSignal = pyqtSignal(Move)
    illegalBoardSignal = pyqtSignal()
    sendLegalMovesSignal = pyqtSignal(list)
    requestPromotionSignal = pyqtSignal()
    sendDrawOfferSignal = pyqtSignal(bool)
    sendDrawSignal = pyqtSignal(bool)

    test_signal = pyqtSignal(str)
    start = pyqtSignal()

    def __init__(self):
        super(Control, self).__init__()

        self.board = chess.Board()
        self.gameRunning = True
        self.start.connect(self.run)

        if platform.system() == 'Windows':
            self.engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish_win/Windows/stockfish_20011801_x64")
        elif platform.system() == 'Linux':
            self.engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish_linux/Linux/stockfish")
        else:
            raise SystemError

        self.white_player = players[0][0]
        self.black_player = players[0][0]
        self.held_move = None

        self.pathing = Pathing()
        self.moving = False
        self.move_thread = None
        self.detection = PieceDetection()
        self.detect_thread = None

    def makeMove(self, move):
        self.moving = True
        self.pathing.updateBoardRep(self.board)
        self.pathing.makeMove(move)
        self.board.push(move)
        self.moving = False

    def detectMove(self):
        self.detection.break_monitoring = False
        events = self.detection.monitor()
        if events is not None:
            move = self.detection.constructMove(events)
            if move != self.detection.ILLEGAL_MOVE:
                print('illegal move')
            else:
                print('move detected ' + str(move))
        else:
            print('skipped')

    @pyqtSlot(GameState)
    def receiveGameState(self, game_state):
        self.gameRunning = True
        self.board.set_fen(game_state.getFEN())
        # for move in game_state.getMoves():
        #     # self.receiveMove(move)
        self.white_player = game_state.getWhitePlayer()
        self.black_player = game_state.getBlackPlayer()

    @pyqtSlot(Move)
    def receiveMove(self, move):
        if not self.gameRunning or self.moving:
            return
        if move.getPromotionPending():
            self.held_move = move
            self.requestPromotionSignal.emit()
            return
        (x, y) = move.initial_square
        (x1, y1) = move.dest_square
        initial_int = Move.getSquareNumber(x, y)
        dest_int = Move.getSquareNumber(x1, y1)

        promotion_piece = None
        if move.promotion_piece is not None:
            promotion_piece = Move.pieceToNumber(move.promotion_piece)
        chess_move = chess.Move(initial_int, dest_int, promotion=promotion_piece)
        if self.board.is_legal(chess_move):
            self.sendMoveSignal.emit(move)
            self.detection.break_monitoring = True
            self.move_thread = threading.Thread(target=self.makeMove, args=[chess_move])
            self.move_thread.start()

    @pyqtSlot(str)
    def receivePromotion(self, promotion_piece):
        if not self.gameRunning:
            return
        if self.held_move is None:
            return

        self.held_move.promotion_piece = promotion_piece
        self.held_move.setPromotionPending(False)
        self.receiveMove(self.held_move)
        self.held_move = None

    @pyqtSlot(bool)
    def receiveDrawOffer(self, color):
        if color:  # white offers draw
            if self.black_player == players[0][0]:  # human player
                self.sendDrawOfferSignal.emit(True)
            else:  # no way of offering computer a draw
                self.sendDrawSignal.emit(False)
        else:  # black offers draw
            if self.white_player == players[0][0]:  # human player
                self.sendDrawOfferSignal.emit(False)
            else:  # no way of offering computer a draw
                self.sendDrawSignal.emit(False)

    @pyqtSlot()
    def receiveDrawAccepted(self):
        self.gameRunning = False

    @pyqtSlot()
    def receiveResign(self):
        self.gameRunning = False

    @pyqtSlot(int, int)
    def sendLegalMoves(self, x, y):
        if not self.gameRunning or self.moving:
            return
        moves = []
        square = 8 * (7 - y) + x
        for move in self.board.legal_moves:
            if move.from_square == square:
                moves.append(Move.moveFromChessMove(move, self.board))
        self.sendLegalMovesSignal.emit(moves)

    @pyqtSlot()
    def run(self):
        self.gameRunning = True
        if not self.board.is_valid():
            self.illegalBoardSignal.emit()
            return

        while True:
            QCoreApplication.processEvents()
            if self.board.turn and self.gameRunning and not self.moving:
                if self.board.is_checkmate():
                    self.gameRunning = False
                    self.sendMoveSignal.emit(Move.blackWonMove())
                elif self.board.is_game_over():
                    self.gameRunning = False
                    self.sendMoveSignal.emit(Move.drawMove())
                elif self.white_player != players[0][0]:
                    result = self.engine.play(self.board,
                                              limit=chess.engine.Limit(time=1),
                                              options={'Skill Level': engine_strength[self.white_player]})

                    if result.move is not None:
                        self.sendMoveSignal.emit(Move.moveFromChessMove(result.move, self.board))
                        self.move_thread = threading.Thread(target=self.makeMove, args=[result.move])
                        self.move_thread.start()
                elif self.detect_thread is None or not self.detect_thread.is_alive():  # human player
                    self.detect_thread = threading.Thread(target=self.detectMove)
                    self.detect_thread.start()

            elif self.gameRunning and not self.moving:
                if self.board.is_checkmate():
                    self.gameRunning = False
                    self.sendMoveSignal.emit(Move.whiteWonMove())
                elif self.board.is_game_over():
                    self.gameRunning = False
                    self.sendMoveSignal.emit(Move.drawMove())
                elif self.black_player != players[0][0]:  # computer player
                    result = self.engine.play(self.board,
                                              limit=chess.engine.Limit(time=1),
                                              options={'Skill Level': str(engine_strength[self.black_player])})

                    if result.move is not None:
                        self.sendMoveSignal.emit(Move.moveFromChessMove(result.move, self.board))
                        self.move_thread = threading.Thread(target=self.makeMove, args=[result.move])
                        self.move_thread.start()
                elif self.detect_thread is None or not self.detect_thread.is_alive():  # human player
                    self.detect_thread = threading.Thread(target=self.detectMove)
                    self.detect_thread.start()
