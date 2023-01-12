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
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setGeometry(QRect(0, 0, 445, 597))

        self.v_layout_widget = QWidget(self.scroll_area_widget)
        self.v_layout_widget.setGeometry(QRect(0, 0, 451, 601))

        self.v_layout = QVBoxLayout(self.v_layout_widget)
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        self.scrap_yahoo = QPushButton(self.v_layout_widget)
        self.v_layout.addWidget(self.scrap_yahoo)

        self.scrap_tradingview = QPushButton(self.v_layout_widget)
        self.v_layout.addWidget(self.scrap_tradingview)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacerItem)

        self.scrap_button = QPushButton(self.v_layout_widget)
        self.v_layout.addWidget(self.scrap_button, 0, Qt.AlignRight)

        self.scroll_area.setWidget(self.scroll_area_widget)
        self.h_layout.addWidget(self.scroll_area)

        self.text_browser = QTextBrowser(self.h_layout)
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)
        self.text_browser.setFont(font)
        self.h_layout.addWidget(self.text_browser)

        # Set text
        self.setWindowTitle("Webscrapper")
        self.scrap_yahoo.setText("Yahoo Finance")
        self.scrap_yahoo.clicked.connect(self.scrap_yahoo_finance)
        self.scrap_tradingview.setText("TradingView")
        self.scrap_tradingview.clicked.connect(self.scrap_tradingview)
        self.scrap_button.setText("Start scrapping")

    def scrap_yahoo_finance(self):
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
