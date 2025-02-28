import sys
from PyQt6.QtWidgets import QApplication
from game.poker_gui import PokerTable

def main():
    app = QApplication(sys.argv)
    window = PokerTable()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 