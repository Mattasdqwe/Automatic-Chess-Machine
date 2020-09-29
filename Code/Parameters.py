stylesheet = """
    QMainWindow {
        background-color: #312e2b;
        color: #ffffff;
        max-height: 720px;
        max-width: 1280px;
    }
    
    QComboBox {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: #ffffff;
        font: bold 30px;
        min-width: 11em;
        max-width: 15em;
        padding: 20px;
    }
    QComboBox::drop-down:button {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 0px;
    }
    QComboBox QAbstractItemView {
        background-color: #312e2b;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-color: #ffffff;
        padding: 5px;
        selection-background-color: transparent;
        outline: 0px;
    } 
    QComboBox QScrollBar {
        border: 2px solid black;
        background: white;
        width: 50px;
    }
    QComboBox QScrollBar::handle {
        background: #e6912c;
    } 
    QComboBox QScrollBar::add-line, QComboBox QScrollBar::sub-line {
        background: none;
        border: none;
        height: 0px;
    } 
    QComboBox QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        height: 0px;
    }
    QComboBox QScrollBar:up-arrow, QComboBox QScrollBar::down-arrow{
        background: none;
        width: 0px;
        height: 0px;
        color: none;
        border: none;
    }
    QCheckBox {
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        font: bold 30px;
        min-width: 5em;
        max-width: 10em;
        padding: 5px;
    }
    
    QCheckBox::indicator {
        background: none;
        border: 2px solid #e6912c;
        border-style: solid;
        width: 13px;
        height: 13px;
    }
    QCheckBox::indicator:checked {
        image: url(./assets/check.png);
    }
"""
main_button_style = """
    QPushButton {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px; 
        font: bold 30px;
        min-width: 5em;
        max-width: 10em;
        padding: 40px;
    }
"""
small_button_style = """
    QPushButton {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        font: bold 30px;
        min-width: 10px;
        max-width: 10em;
        padding: 10px;
    }
"""
options_button_style = """
    QPushButton {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px; 
        font: bold 30px;
        min-width: 10px;
        max-width: 10em;
        padding: 20px;
    }
"""
board_label_style = """
    QLabel {
        min-height: 600px;
        min-width: 600px;
        max-height: 600px;
        max-width: 600px;
    }
"""
piece_label_style = """
    QLabel {
        min-height: 83px;
        min-width: 83px;
        max-height: 83px;
        max-width: 83px;
    }
"""
label_style = """
    QLabel {
        color: #ffffff;
        border: none;
        font: bold 30px;
        min-width: 11em;
        padding: 5px;
    }
"""
heading_label_style = """
    QLabel {
        color: #ffffff;
        border: none;
        font: bold 30px;
        padding: 5px;
    }
"""
back_style = """
    QPushButton {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        font: bold 30px;
        min-width: 3em;
        max-width: 3em;
        min-height: 1em;
        padding: 5px;
    }
"""
holder_style = """
    PieceHolder {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: #ffffff;
        min-width: 10px;
        min-height: 10px;
        width: 100px;
        height: 600px;
        padding: 10px;
    }
"""
check_style_white = """
    QCheckBox {
        border-color: #000000;
        background-color: #ffffff;
        color: #000000;
    }
"""
check_style_black = """
    QCheckBox {
        border-color: #ffffff;
        background-color: #000000;
        color: #ffffff;
    }
"""
check_style_move = """
    QCheckBox {
        border-color: #ffffff;
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        min-width: 10px;
        font: bold 30px;
        padding: 10px;
    }
    QCheckBox::indicator {
        background: none;
        border: none;
        width: 30;
        height: 30px;
    }
    QCheckBox::indicator:checked {
        image: url(./assets/white_check.png);
    }
    QCheckBox::indicator:unchecked {
        image: url(./assets/black_check.png);
    }
"""
move_table_style = """
    QTableWidget {
        background-color: #e6912c;
        color: #ffffff;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: #ffffff;
        min-width: 300px;
        font: bold 30px;
        padding: 10px;
    }
    QTableWidget QHeaderView {
        background-color: #e6912c;
    }
    QTableWidget QHeaderView::section {
        background-color: #e6912c;
        border-style: none;
        border: none;
        color: #ffffff;
        font: bold 30px;
    }
    QTableWidget::item:selected {
        selection-color: #ffffff;
        background-color: #312e2b;
    }
    QTableWidget QScrollBar {
        border: none;
        background: white;
        width: 50px;
    }
    QTableWidget QScrollBar::handle {
        background: #312e2b;
        border: 4px solid black;
    } 
    QTableWidget QScrollBar::add-line, QComboBox QScrollBar::sub-line {
        background: none;
        border: none;
        border-style: none;
        height: 0px;
    } 
    QTableWidget QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        height: 0px;
    }
    QTableWidget QScrollBar:up-arrow, QComboBox QScrollBar::down-arrow{
        background: none;
        width: 0px;
        height: 0px;
        color: none;
        border: none;
        border-style: none;
    }
    
"""
dialogbox_style = """
    QDialog {
        background-color: #312e2b;
        border: 2px solid black;
        min-width: 500px;
        min-height: 300px;
        font: bold 20px;
    }
    QLabel {
        font: bold 30px;
        color: #ffffff;
    }
"""
promo_white_style = """
    QDialog {
        background-color: #312e2b;
        border: 2px solid black;
        min-width: 500px;
        min-height: 150px;
        
    }
    QLabel {
        font: bold 20px;
        color: #ffffff;
    }
"""
promo_black_style = """
    QDialog {
        background-color: #ffffff;
        border: 2px solid black;
        min-width: 500px;
        min-height: 150px;
        
    }
    QLabel {
        font: bold 20px;
        color: #312e2b;
    }
"""
radio_button_style = """
    QRadioButton {
        color: #ffffff;
        font: bold 20px;
    }
"""
players = [
    ('Human', 'assets/human.png'),
    ('Stockfish Level 1', 'assets/computer.png'),
    ('Stockfish Level 2', 'assets/computer.png'),
    ('Stockfish Level 3', 'assets/computer.png'),
    ('Stockfish Level 4', 'assets/computer.png'),
    ('Stockfish Level 5', 'assets/computer.png'),
    ('Stockfish Level 6', 'assets/computer.png'),
    ('Stockfish Level 7', 'assets/computer.png'),
    ('Stockfish Level 8', 'assets/computer.png'),
    ('Stockfish Level 9', 'assets/computer.png'),
    ('Stockfish Level 10', 'assets/computer.png'),
    ('Stockfish Level 11', 'assets/computer.png'),
    ('Stockfish Level 12', 'assets/computer.png'),
    ('Stockfish Level 13', 'assets/computer.png'),
    ('Stockfish Level 14', 'assets/computer.png'),
    ('Stockfish Level 15', 'assets/computer.png'),
    ('Stockfish Level 16', 'assets/computer.png'),
    ('Stockfish Level 17', 'assets/computer.png'),
    ('Stockfish Level 18', 'assets/computer.png'),
    ('Stockfish Level 19', 'assets/computer.png'),
    ('Stockfish Level 20', 'assets/computer.png')
]
engine_strength = {
    'Stockfish Level 1': 1,
    'Stockfish Level 2': 2,
    'Stockfish Level 3': 3,
    'Stockfish Level 4': 4,
    'Stockfish Level 5': 5,
    'Stockfish Level 6': 6,
    'Stockfish Level 7': 7,
    'Stockfish Level 8': 8,
    'Stockfish Level 9': 9,
    'Stockfish Level 10': 10,
    'Stockfish Level 11': 11,
    'Stockfish Level 12': 12,
    'Stockfish Level 13': 13,
    'Stockfish Level 14': 14,
    'Stockfish Level 15': 15,
    'Stockfish Level 16': 16,
    'Stockfish Level 17': 17,
    'Stockfish Level 18': 18,
    'Stockfish Level 19': 19,
    'Stockfish Level 20': 20
}
