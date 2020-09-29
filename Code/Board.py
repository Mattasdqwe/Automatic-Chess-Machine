from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QFrame, QPushButton, QApplication
from PyQt5.QtGui import QIcon, QPixmap, QDrag, QCursor, QPainter
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData, QPoint, QSize
from Parameters import holder_style, board_label_style, piece_label_style


class Board(QLabel):
    mouse_pressed_signal = pyqtSignal(int, int)

    def __init__(self, drag_enabled=True):
        super(Board, self).__init__()

        self.drag_enabled = drag_enabled
        self.setAcceptDrops(self.drag_enabled)
        self.setStyleSheet(board_label_style)

        self.image = QPixmap('assets/board.png')
        self.image = self.image.scaled(600, 600)
        self.setPixmap(self.image)
        self.setFixedHeight(600)
        self.setFixedWidth(600)

        self.pieces = [[None for j in range(8)] for i in range(8)]
        self.markers = []
        self.flipped = False

    def setPiece(self, piece_type, x, y):
        if self.pieces[y][x] is not None:
            try:
                self.pieces[y][x].setParent(None)
                self.pieces[y][x].deleteLater()
                self.pieces[y][x] = None
            except RuntimeError as e:
                self.pieces[y][x] = None

        if piece_type is None:
            return
        piece = Piece(piece_type, draggable=self.drag_enabled)
        piece.setParent(self)

        self.pieces[y][x] = piece
        piece.move(QPoint(x*(600/8)-3, y*(600/8)-5))
        piece.show()

    def getStringRepresentation(self):
        pieces = [[None for x in range(8)] for y in range(8)]

        for x in range(8):
            for y in range(8):
                piece = self.pieces[y][x]
                name = None
                x_actual = x
                y_actual = y
                if self.flipped:
                    x_actual = 7-x
                    y_actual = 7-y
                try:
                    if piece is not None and piece.parent() is not None:
                        name = piece.getPieceType()
                except RuntimeError:
                    self.pieces[y][x] = None

                pieces[y_actual][x_actual] = name
        return str(pieces)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().text().startswith('piece/'):
            piece_data = event.mimeData().text().split('/')

            hx = int(piece_data[2])
            hy = int(piece_data[3])
            x = int((event.pos().x()-(hx-Piece.image_size/2))/(600/8))
            y = int((event.pos().y()-(hy-Piece.image_size/2))/(600/8))

            self.setPiece(piece_data[1], x, y)

    def standardSetup(self):
        self.setPiece(Piece.black_rook, 0, 0)
        self.setPiece(Piece.black_knight, 1, 0)
        self.setPiece(Piece.black_bishop, 2, 0)
        self.setPiece(Piece.black_queen, 3, 0)
        self.setPiece(Piece.black_king, 4, 0)
        self.setPiece(Piece.black_bishop, 5, 0)
        self.setPiece(Piece.black_knight, 6, 0)
        self.setPiece(Piece.black_rook, 7, 0)
        for k in range(8):
            self.setPiece(Piece.black_pawn, k, 1)
        for x in range(8):
            for y in range(2, 6):
                self.setPiece(None, x, y)
        for k in range(8):
            self.setPiece(Piece.white_pawn, k, 6)
        self.setPiece(Piece.white_rook, 0, 7)
        self.setPiece(Piece.white_knight, 1, 7)
        self.setPiece(Piece.white_bishop, 2, 7)
        self.setPiece(Piece.white_queen, 3, 7)
        self.setPiece(Piece.white_king, 4, 7)
        self.setPiece(Piece.white_bishop, 5, 7)
        self.setPiece(Piece.white_knight, 6, 7)
        self.setPiece(Piece.white_rook, 7, 7)

    def clearBoard(self):
        for x in range(8):
            for y in range(8):
                if self.pieces[x][y] is not None:
                    try:
                        self.pieces[x][y].setParent(None)
                        self.pieces[x][y].deleteLater()
                        self.pieces[x][y] = None
                    except RuntimeError as e:
                        self.pieces[x][y] = None

    def flipBoard(self):
        self.flipped = not self.flipped
        self.setMarkers(None)
        for x in range(8):
            for y in range(4):
                xmir = 7-x
                ymir = 7-y
                piece = self.pieces[y][x]
                mir_piece = self.pieces[ymir][xmir]
                piece_type = None
                mir_piece_type = None
                if piece is not None:
                    piece_type = piece.getPieceType()
                if mir_piece is not None:
                    mir_piece_type = mir_piece.getPieceType()
                try:
                    if piece is not None:
                        piece.isHidden()
                except RuntimeError as e:
                    piece_type = None
                try:
                    if mir_piece is not None:
                        mir_piece.isHidden()
                except RuntimeError as e:
                    mir_piece_type = None

                self.setPiece(mir_piece_type, x, y)
                self.setPiece(piece_type, xmir, ymir)

    def getFlipped(self):
        return self.flipped

    def setMarkers(self, positions=None):
        for marker in self.markers:
            marker.deleteLater()
            marker.setParent(None)
        self.markers = []
        if positions is not None:
            for position in positions:
                m = SquareMarker()
                m.setParent(self)
                m.move(QPoint(position[0] * (600 / 8) - 3, position[1] * (600 / 8) - 5))
                m.show()
                self.markers.append(m)


    def mousePressEvent(self, ev):
        self.mouse_pressed_signal.emit(ev.pos().x(), ev.pos().y())


class Piece(QLabel):

    white_pawn = 'wp'
    white_rook = 'wr'
    white_knight = 'wn'
    white_bishop = 'wb'
    white_queen = 'wq'
    white_king = 'wk'
    black_pawn = 'bp'
    black_rook = 'br'
    black_knight = 'bn'
    black_bishop = 'bb'
    black_queen = 'bq'
    black_king = 'bk'
    image_size = 83

    def __init__(self, piece_type, draggable=True, copy_drag=False, parent=None):
        super(Piece, self).__init__(parent=parent)
        self.draggable = draggable
        self.copy_drag = copy_drag
        self.piece_type = piece_type

        self.image = QPixmap('assets/'+piece_type+'.png')
        self.setPixmap(self.image)
        self.drag_start_position = self.pos()

        self.setStyleSheet(piece_label_style)

    def getPieceType(self):
        return self.piece_type

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.parent().mouseMoveEvent(event)

    def mouseMoveEvent(self, event):
        if not self.draggable:
            return
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.drag_start_position.x() < 0 or self.drag_start_position.x() > self.image_size:
            return
        if self.drag_start_position.y() < 0 or self.drag_start_position.y() > self.image_size:
            return

        if not self.copy_drag:
            self.hide()
        drag = QDrag(self)
        hotspot = event.pos() - QPoint(6, 6)
        mimedata = QMimeData()
        mimedata.setText('piece/' + self.piece_type + '/' + str(hotspot.x()) + '/' + str(hotspot.y()))
        drag.setMimeData(mimedata)
        pixmap = self.image
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotspot)
        if not self.copy_drag:
            self.setParent(None)
            self.deleteLater()
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class PieceHolder(QLabel):

    def __init__(self, is_white=True):
        super(PieceHolder, self).__init__()

        self.is_white = is_white
        self.setAcceptDrops(True)
        self.setStyleSheet(holder_style)

        self.resize(120, 625)
        self.setupPieces()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pass  # pieces dropped are deleted

    def setPiece(self, name, position):
        piece = Piece(name, copy_drag=True)
        xpos = int((self.width()-Piece.image_size)/2)
        ypos = int(self.height()*position/6)
        piece.move(xpos, ypos)
        piece.setParent(self)
        piece.show()

    def setupPieces(self):
        if self.is_white:
            self.setPiece(Piece.white_pawn, 0)
            self.setPiece(Piece.white_rook, 1)
            self.setPiece(Piece.white_knight, 2)
            self.setPiece(Piece.white_bishop, 3)
            self.setPiece(Piece.white_queen, 4)
            self.setPiece(Piece.white_king, 5)
        else:
            self.setPiece(Piece.black_pawn, 0)
            self.setPiece(Piece.black_rook, 1)
            self.setPiece(Piece.black_knight, 2)
            self.setPiece(Piece.black_bishop, 3)
            self.setPiece(Piece.black_queen, 4)
            self.setPiece(Piece.black_king, 5)


class SquareMarker(QLabel):

    def __init__(self):
        super(SquareMarker, self).__init__()

        self.image = QPixmap('assets/marker.png')
        self.setPixmap(self.image)

        self.setStyleSheet(piece_label_style)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().mouseMoveEvent(event)

