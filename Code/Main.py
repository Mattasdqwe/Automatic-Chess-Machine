from PyQt5.QtWidgets import QApplication
from View import View


def main():
    app = QApplication([])
    view = View()
    view.show()
    
    app.exec_()


if __name__ == '__main__':
    main()
