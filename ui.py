from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QGridLayout, QSizePolicy, QLabel,
                             QHBoxLayout, QVBoxLayout, QSpacerItem,
                             QScrollArea, QTextBrowser)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect
from scraper import Scraper
import sys


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface"""
        self.resize(800, 600)
        self.setWindowTitle("Webscrapper")

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(10, 10, 10, 10)
        self.h_layout.addLayout(self.v_layout)

        self.yahoo_button = QPushButton(self)
        self.yahoo_button.setText("Yahoo Finance")
        self.yahoo_button.clicked.connect(self.scrap_yahoo)
        self.v_layout.addWidget(self.yahoo_button)

        self.tradingview_button = QPushButton(self)
        self.tradingview_button.setText("TradingView")
        self.tradingview_button.clicked.connect(self.scrap_tradingview)
        self.v_layout.addWidget(self.tradingview_button)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacerItem)

        self.v_layout_widget = QWidget(self)
        self.v_layout_widget.setGeometry(QRect(0, 0, 451, 601))

        self.scrap_button = QPushButton(self.v_layout_widget)
        self.scrap_button.setText("Start scrapping")
        self.v_layout.addWidget(self.scrap_button, 0, Qt.AlignRight)

        self.text_browser = QTextBrowser(self)
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)
        self.text_browser.setFont(font)
        self.h_layout.addWidget(self.text_browser)

    def scrap_yahoo(self):
        """
        Scrap data from Yahoo Finance
        website using Scraper class.
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
        text = "\n".join(data)
        self.text_browser.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
