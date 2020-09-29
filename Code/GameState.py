from Parameters import players
from Board import Piece
import chess


class GameState:

    def __init__(self):
        self.board = self.standardBoard()
        self.initial_board = self.standardBoard()
        self.moves = []
        self.white_player = players[0][0]
        self.black_player = players[0][0]
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True
        self.next_to_move = True  # True for white, False for black
        self.gameOver = False

        self.save_file = None  # TODO: implement

    @staticmethod
    def standardBoard():
        board = [[None for x in range(8)] for y in range(8)]
        board[0][0] = Piece.black_rook
        board[0][1] = Piece.black_knight
        board[0][2] = Piece.black_bishop
        board[0][3] = Piece.black_queen
        board[0][4] = Piece.black_king
        board[0][5] = Piece.black_bishop
        board[0][6] = Piece.black_knight
        board[0][7] = Piece.black_rook
        for k in range(8):
            board[1][k] = Piece.black_pawn
            board[6][k] = Piece.white_pawn
        board[7][0] = Piece.white_rook
        board[7][1] = Piece.white_knight
        board[7][2] = Piece.white_bishop
        board[7][3] = Piece.white_queen
        board[7][4] = Piece.white_king
        board[7][5] = Piece.white_bishop
        board[7][6] = Piece.white_knight
        board[7][7] = Piece.white_rook

        return board

    def getBoard(self):
        return self.board

    def setBoard(self, board_string):
        board_string = board_string.replace('[', '')
        board_string = board_string.replace(']', '')
        board_string = board_string.replace("'", '')
        board_string = board_string.replace(' ', '')

        for i, piece in enumerate(board_string.split(',')):
            if piece == 'None':
                piece = None
            self.board[int(i/8)][i % 8] = piece
            self.initial_board[int(i/8)][i % 8] = piece

    def getMoves(self):
        return self.moves

    def addMove(self, move):
        self.moves.append(move)
        self.next_to_move = not self.next_to_move
        if move.won_player is not None:
            self.gameOver = True
            return
        if move.draw:
            self.gameOver = True
            return

        piece = move.piece
        (x, y) = move.initial_square
        (x1, y1) = move.dest_square
        if move.castled:
            if piece == Piece.white_king:
                if x1 == 2:
                    self.board[7][0] = None
                    self.board[7][4] = None
                    self.board[7][3] = Piece.white_rook
                    self.board[7][2] = Piece.white_king
                if x1 == 6:
                    self.board[7][7] = None
                    self.board[7][4] = None
                    self.board[7][5] = Piece.white_rook
                    self.board[7][6] = Piece.white_king
                self.white_kingside_castle = False
                self.white_queenside_castle = False
            elif piece == Piece.black_king:
                if x1 == 2:
                    self.board[0][0] = None
                    self.board[0][4] = None
                    self.board[0][3] = Piece.black_rook
                    self.board[0][2] = Piece.black_king
                if x1 == 6:
                    self.board[0][7] = None
                    self.board[0][4] = None
                    self.board[0][5] = Piece.black_rook
                    self.board[0][6] = Piece.black_king
                self.black_kingside_castle = False
                self.black_queenside_castle = False
            return

        if self.board[y][x] == piece:
            self.board[y][x] = None
            self.board[y1][x1] = piece
        if move.en_passant:
            if y1 == 2 and self.board[3][x1] == Piece.black_pawn:
                self.board[3][x1] = None
            if y1 == 5 and self.board[4][x1] == Piece.white_pawn:
                self.board[4][x1] = None
        if piece == Piece.black_king:
            self.black_kingside_castle = False
            self.black_queenside_castle = False
        if piece == Piece.white_king:
            self.black_kingside_castle = False
            self.black_queenside_castle = False
        if piece == Piece.white_rook:
            if x == 0 and y == 7:
                self.white_queenside_castle = False
            if x == 7 and y == 7:
                self.white_kingside_castle = False
        if piece == Piece.black_rook:
            if x == 0 and y == 0:
                self.black_queenside_castle = False
            if x == 7 and y == 0:
                self.black_kingside_castle = False
        if move.promotion_piece is not None:
            self.board[y1][x1] = move.promotion_piece

    @staticmethod
    def reverseMove(board, move):
        if move.won_player is not None:
            return board
        if move.draw:
            return board
        b = [[x for x in y] for y in board]
        piece = move.piece
        (x, y) = move.initial_square
        (x1, y1) = move.dest_square
        if move.castled:
            if piece == Piece.white_king:
                if x1 == 2:
                    b[7][0] = Piece.white_rook
                    b[7][4] = Piece.white_king
                    b[7][3] = None
                    b[7][2] = None
                if x1 == 6:
                    b[7][7] = Piece.white_rook
                    b[7][4] = Piece.white_king
                    b[7][5] = None
                    b[7][6] = None
            elif piece == Piece.black_king:
                if x1 == 2:
                    b[0][0] = Piece.black_rook
                    b[0][4] = Piece.black_king
                    b[0][3] = None
                    b[0][2] = None
                if x1 == 6:
                    b[0][7] = Piece.black_rook
                    b[0][4] = Piece.black_king
                    b[0][5] = None
                    b[0][6] = None
            return b

        if move.en_passant:
            if y1 == 2:
                b[3][x1] = Piece.black_pawn
            if y1 == 5:
                b[4][x1] = Piece.white_pawn
        else:
            b[y1][x1] = move.dest_piece

        b[y][x] = piece

        return b

    def getBoardAtMove(self, move_number):
        if self.next_to_move and len(self.moves) % 2 != 0:
            move_number = move_number - 1  # compensate for black starting
        if move_number >= len(self.moves):
            return self.board

        board = self.board
        for k in range(len(self.moves)-1, max(move_number, -1), -1):
            board = self.reverseMove(board, self.moves[k])

        return board

    def getWhitePlayer(self):
        return self.white_player

    def setWhitePlayer(self, white_player):
        if white_player in [p[0] for p in players]:
            self.white_player = white_player

    def getBlackPlayer(self):
        return self.black_player

    def setBlackPlayer(self, black_player):
        if black_player in [p[0] for p in players]:
            self.black_player = black_player

    def getWhiteKingsideCastle(self):
        return self.white_kingside_castle

    def setWhiteKingsideCastle(self, castle):
        self.white_kingside_castle = castle

    def getWhiteQueensideCastle(self):
        return self.white_queenside_castle

    def setWhiteQueensideCastle(self, castle):
        self.white_queenside_castle = castle

    def getBlackKingsideCastle(self):
        return self.black_kingside_castle

    def setBlackKingsideCastle(self, castle):
        self.black_kingside_castle = castle

    def getBlackQueensideCastle(self):
        return self.black_queenside_castle

    def setBlackQueensideCastle(self, castle):
        self.black_queenside_castle = castle

    def getNextToMove(self):
        return self.next_to_move

    def setNextToMove(self, next_to_move):
        self.next_to_move = next_to_move

    def getGameOver(self):
        return self.gameOver

    def fromText(self, text):
        for line in text.split('\n'):
            contents = line.split(':')
            if contents[0] == 'board':
                self.setBoard(contents[1])
            if contents[0] == 'white_player':
                self.setWhitePlayer(contents[1])
            if contents[0] == 'black_player':
                self.setBlackPlayer(contents[1])
            if contents[0] == 'white_kingside_castle':
                self.setWhiteKingsideCastle(contents[1] == 'True')
            if contents[0] == 'white_queenside_castle':
                self.setWhiteQueensideCastle(contents[1] == 'True')
            if contents[0] == 'black_kingside_castle':
                self.setBlackKingsideCastle(contents[1] == 'True')
            if contents[0] == 'black_queenside_castle':
                self.setBlackQueensideCastle(contents[1] == 'True')
            if contents[0] == 'next_to_move':
                self.setNextToMove(contents[1] == 'True')
        self.moves = []
        self.gameOver = False

    def toText(self):
        text = ""
        text += "board:" + str(self.board) + "\n"
        text += "white_player:" + str(self.white_player) + "\n"
        text += "black_player:" + str(self.black_player) + "\n"
        text += "white_kingside_castle:" + str(self.white_kingside_castle) + "\n"
        text += "white_queenside_castle:" + str(self.white_queenside_castle) + "\n"
        text += "black_kingside_castle:" + str(self.black_kingside_castle) + "\n"
        text += "black_queenside_castle:" + str(self.black_queenside_castle) + "\n"
        text += "next_to_move:" + str(self.next_to_move) + "\n"

        return text

    def getFEN(self):
        fen = ''
        for y in range(8):
            counter = 0
            for x in range(8):
                if self.initial_board[y][x] is None:
                    counter += 1
                else:
                    if counter > 0:
                        fen += str(counter)
                    piece_str = self.initial_board[y][x][1]
                    if self.initial_board[y][x][0] == 'w':
                        piece_str = piece_str.upper()
                    fen += piece_str
                    counter = 0

            if counter > 0:
                fen += str(counter)
            if y < 7:
                fen += '/'

        # turn color
        fen += ' '
        if self.next_to_move:
            if len(self.moves) % 2 == 0:
                fen += 'w'
            else:
                fen += 'b'
        else:
            if len(self.moves) % 2 == 0:
                fen += 'b'
            else:
                fen += 'w'

        # castling
        fen += ' '
        castling = [self.white_kingside_castle, self.white_queenside_castle,
                    self.black_kingside_castle, self.black_queenside_castle]
        for move in self.moves:
            if move.piece == Piece.white_king:
                castling[0] = False
                castling[1] = False
            if move.piece == Piece.black_king:
                castling[2] = False
                castling[3] = False
            if move.piece == Piece.white_rook:
                if move.initial_square == (7, 7):
                    castling[0] = False
                if move.initial_square == (0, 7):
                    castling[1] = False
            if move.piece == Piece.black_rook:
                if move.initial_square == (7, 0):
                    castling[0] = False
                if move.initial_square == (0, 7):
                    castling[1] = False
        if castling[0]:
            fen += 'K'
        if castling[1]:
            fen += 'Q'
        if castling[2]:
            fen += 'k'
        if castling[3]:
            fen += 'q'
        if not (castling[0] or castling[1] or castling[2] or castling[3]):
            fen += '-'

        # en passant
        fen += ' -'
        # halfmove
        fen += ' 0'
        # fullmove
        fen += ' 1'

        return fen


class Move:

    won_player_white = '1-0'
    won_player_black = '0-1'

    def __init__(self, piece, dest_piece, x, y, x1, y1, promotion_piece=None, castled=False, en_passant=False,
                 check=False, checkmate=False, draw=False, won_player=None):
        self.piece = piece
        self.dest_piece = dest_piece
        self.initial_square = (x, y)
        self.dest_square = (x1, y1)
        self.promotion_piece = promotion_piece
        self.promotion_choice_pending = False
        self.castled = castled
        self.en_passant = en_passant
        self.check = check
        self.checkmate = checkmate
        self.draw = draw
        self.won_player = won_player

    def setPromotionPending(self, pending=True):
        self.promotion_choice_pending = pending

    def getPromotionPending(self):
        return self.promotion_choice_pending

    @staticmethod
    def toFile(n):
        return chr(ord('a') + n)

    @staticmethod
    def toRank(n):
        return str(8-n)

    def getInitialSquareString(self):
        return self.toFile(self.initial_square[1]) + self.toRank(self.initial_square[0])

    def getDestinationSquareString(self):
        return self.toFile(self.dest_square[1]) + self.toRank(self.dest_square[0])

    @staticmethod
    def getSquareNumber(x, y):
        return 8 * (7 - y) + x

    @staticmethod
    def getXY(square_number):
        x = square_number % 8
        y = 7 - int(square_number / 8)
        return x, y

    @staticmethod
    def numberToPiece(piece):
        if piece is None:
            return None
        piece_type = {
            chess.ROOK: Piece.white_rook[1],
            chess.KNIGHT: Piece.white_knight[1],
            chess.BISHOP: Piece.white_bishop[1],
            chess.QUEEN: Piece.white_queen[1],
            chess.KING: Piece.white_king[1],
            chess.PAWN: Piece.white_pawn[1]
        }
        if piece.color:
            color = 'w'
        else:
            color = 'b'
        return color + piece_type[piece.piece_type]

    @staticmethod
    def pieceToNumber(piece):
        if piece is None:
            return None
        piece_type = {
            Piece.white_rook[1]: chess.ROOK,
            Piece.white_knight[1]: chess.KNIGHT,
            Piece.white_bishop[1]: chess.BISHOP,
            Piece.white_queen[1]: chess.QUEEN,
            Piece.white_king[1]: chess.KING,
            Piece.white_pawn[1]: chess.PAWN
        }
        return piece_type[piece[1]]

    @staticmethod
    def moveFromChessMove(move, board):
        try:
            x, y = Move.getXY(move.from_square)
            x1, y1 = Move.getXY(move.to_square)
            piece = Move.numberToPiece(board.piece_at(move.from_square))
            dest_piece = Move.numberToPiece(board.piece_at(move.to_square))
            promotion_piece = None
            if move.promotion is not None:
                promotion_piece = Move.numberToPiece(chess.Piece(move.promotion, board.color_at(move.from_square)))
            en_passant = board.is_en_passant(move)
            castled = board.is_castling(move)
            check = board.gives_check(move)
            board.push(move)
            checkmate = board.is_checkmate()
            board.pop()
            return Move(piece, dest_piece, x, y, x1, y1, promotion_piece, castled, en_passant, check, checkmate)
        except Exception as e:
            print(e)

    @staticmethod
    def whiteWonMove():
        return Move(None, None, None, None, None, None, won_player=Move.won_player_white)

    @staticmethod
    def blackWonMove():
        return Move(None, None, None, None, None, None, won_player=Move.won_player_black)

    @staticmethod
    def drawMove():
        return Move(None, None, None, None, None, True, None)

    def stringRepresentation(self):
        if self.castled:
            if self.dest_square == (6, 7) or self.dest_square == (6, 0):
                return 'O-O'
            if self.dest_square == (2, 7) or self.dest_square == (2, 0):
                return 'O-O-O'
            return ''
        if self.draw:
            return '½–½'
        if self.won_player is not None:
            if self.won_player == self.won_player_white or self.won_player == self.won_player_black:
                return self.won_player
            return ''

        # piece moving
        move_text = ''
        if self.piece != Piece.white_pawn and self.piece != Piece.black_pawn:
            move_text += self.piece[1].upper()
        else:
            if self.dest_piece is not None:
                move_text += self.toFile(self.initial_square[0])

        # capture?
        if self.dest_piece is not None:
            move_text += 'x'

        # destination square
        move_text += self.toFile(self.dest_square[0])
        move_text += self.toRank(self.dest_square[1])

        # pawn promotion
        if self.promotion_piece is not None:
            move_text += '=' + self.promotion_piece[1].upper()

        # check and mate
        if self.checkmate:
            move_text += '#'
        elif self.check:
            move_text += '+'

        return move_text



