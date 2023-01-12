from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QVBoxLayout, QSpacerItem, QPushButton,
                             QSizePolicy, QScrollArea, QLabel, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from scraper import Scraper
from threading import Thread
import sys


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface"""
        self.resize(800, 600)
        self.setWindowTitle("Webscrapper")

        # Create layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Menu bar
        self.menu = QVBoxLayout()
        self.menu.setContentsMargins(10, 10, 10, 10)
        self.layout.addLayout(self.menu)

        # Label for the menu
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.label = QLabel("Choose website to scrap:")
        self.label.setFont(font)
        self.menu.addWidget(self.label)

        # Buttons for each website to scrap
        self.button1 = QPushButton()
        self.button1.setText("Yahoo Finance")
        self.button1.clicked.connect(self.scrap_yahoo)
        self.menu.addWidget(self.button1)

        self.button2 = QPushButton()
        self.button2.setText("TradingView")
        self.button2.clicked.connect(self.scrap_tradingview)
        self.menu.addWidget(self.button2)

        spacerItem = QSpacerItem(20, 40,
                                 QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self.menu.addItem(spacerItem)

        self.scrap_button = QPushButton()
        self.scrap_button.setText("Start scrapping")
        self.menu.addWidget(self.scrap_button, 0, Qt.AlignRight)

        # Text browser for displaying data
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)

        # Output text area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.output = QTableWidget(self)
        self.output.setColumnCount(0)
        self.output.setRowCount(0)
        self.scrollArea.setWidget(self.output)
        self.layout.addWidget(self.scrollArea)

    def scrap_yahoo(self):
        """
        Scrap data from Yahoo Finance
        website using Scraper class.
        """
        thread = Thread(target=self._scrap_yahoo)
        thread.start()

    def _scrap_yahoo(self):
        """
        Helper function for yahoo scrapping
        to avoid blocking the UI.
        """
        scraper = Scraper()
        data = scraper.scrap_yahoo_finance()
        self.display_data(data)
        scraper.quit()

    def scrap_tradingview(self):
        """
        Scrap data from TradingView
        website using Scraper class.
        """
        pass

    def display_data(self, data):
        """
        Convert data to string and
        display it in the text browser.
        """
        self.output.setColumnCount(len(data[0]))
        self.output.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.output.setItem(i, j, QTableWidgetItem(item))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
