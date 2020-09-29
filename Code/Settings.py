from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QComboBox, QVBoxLayout, QLabel, QRadioButton, \
    QStyleOptionButton, QStyle, QGroupBox, QPushButton
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from Parameters import stylesheet, back_style, label_style, radio_button_style
from GameState import GameState


class Settings(QMainWindow):
    gotoSignal = pyqtSignal(str)
    sendSettingsSignal = pyqtSignal(str)

    def __init__(self):
        super(Settings, self).__init__()
        self.settings = []

        self.central_widget = QWidget()
        self.uiSetup()
        self.setCentralWidget(self.central_widget)

    def uiSetup(self):
        layout = QVBoxLayout()

        # back button
        back_button = QPushButton()
        back_button.setIcon(QIcon('assets/back_button.png'))
        back_button.setIconSize(QSize(32, 32))
        back_button.clicked.connect(lambda: self.goto('game_view'))
        back_button.setStyleSheet(back_style)

        setting1 = Setting()
        setting1.setMessage('Allow Touchscreen Moves')
        setting1.setIdentifier('allow_touchscreen_moves')
        setting1.addOption('Yes                                ', True)
        setting1.addOption('No                                 ', False)
        self.settings.append(setting1)

        setting2 = Setting()
        setting2.setMessage('Show Legal Moves')
        setting2.setIdentifier('show_legal_moves')
        setting2.addOption('Yes                                ', True)
        setting2.addOption('No                                 ', False)
        self.settings.append(setting2)

        setting3 = Setting()
        setting3.setMessage('Show Last Move')
        setting3.setIdentifier('show_last_move')
        setting3.addOption('Yes                                ', True)
        setting3.addOption('No                                 ', False)
        self.settings.append(setting3)

        layout.addWidget(back_button)
        layout.addWidget(setting1)
        layout.addWidget(setting2)
        layout.addWidget(setting3)
        layout.addStretch()

        self.central_widget.setLayout(layout)
        self.setStyleSheet(stylesheet)

    def fromFile(self):
        pass

    def saveSettings(self):
        pass

    def sendSettings(self):
        settings_string = ''
        for setting in self.settings:
            settings_string += setting.toText() + '\n'
        self.sendSettingsSignal.emit(settings_string)

    def goto(self, name):
        self.sendSettings()
        self.gotoSignal.emit(name)


class Setting(QWidget):

    def __init__(self, parent=None):
        super(Setting, self).__init__(parent=parent)
        self.value = None
        self.identifier = None

        self.setting_layout = QHBoxLayout()
        self.message = QLabel()
        self.message.setStyleSheet(label_style)
        self.options = QGroupBox()
        self.button_layout = QHBoxLayout()
        self.options.setLayout(self.button_layout)

        self.setting_layout.addWidget(self.message)
        self.setting_layout.addWidget(self.options)
        self.setLayout(self.setting_layout)

        self.setStyleSheet("Setting {max-height:100px;}")

    def setMessage(self, text):
        self.message.setText(text)

    def addOption(self, text, value):
        button = QRadioButton()
        button.toggled.connect(lambda x: self.checked(value, x))
        button.setText(text)
        button.setStyleSheet(radio_button_style)
        self.button_layout.addWidget(button)

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def checked(self, value, checked):
        if checked:
            self.value = value

    def getValue(self):
        return self.value

    def toText(self):
        return str(self.identifier) + ":" + str(self.value)


