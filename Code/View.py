from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QShortcut
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QKeySequence
from MainMenu import MainMenu
from PlayerSelection import PlayerSelection
from BoardSetup import BoardSetup
from GameView import GameView
from Settings import Settings


class View(QMainWindow):

    def __init__(self):
        super(View, self).__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        # self.setCursor(Qt.BlankCursor)

        # settings connecting
        game_view = GameView()
        settings = Settings()
        settings.sendSettingsSignal.connect(game_view.receiveSettings)

        self.pages = {}
        self.register(MainMenu(), 'main_menu')
        self.register(PlayerSelection(), 'player_selection')
        self.register(BoardSetup(), 'board_setup')
        self.register(game_view, 'game_view')
        self.register(settings, 'settings')



        self.shortcutFull = QShortcut(self)
        self.shortcutFull.setKey(QKeySequence('F11'))
        self.shortcutFull.setContext(Qt.ApplicationShortcut)
        self.shortcutFull.activated.connect(self.handleFullScreen)

        self.goto('main_menu')

    def handleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def register(self, widget, name):
        self.pages[name] = widget
        self.stacked_widget.addWidget(widget)
        widget.gotoSignal.connect(self.goto)
        try:
            widget.sendDataSignal.connect(self.sendData)
        except AttributeError:
            pass

    @pyqtSlot(str)
    def goto(self, name):
        if name in self.pages:
            widget = self.pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            try:
                widget.onShown()
            except AttributeError:
                pass

    @pyqtSlot(str, str)
    def sendData(self, name, data):
        if name in self.pages:
            widget = self.pages[name]
            try:
                widget.receiveData(data)
            except AttributeError:
                pass

            


