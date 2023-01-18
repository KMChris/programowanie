from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QVBoxLayout, QSpacerItem, QPushButton,
                             QSizePolicy, QScrollArea, QLabel,
                             QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5.QtGui import QFont
from analysis import Analysis
from threading import Thread
import sys


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface"""
        self.resize(800, 600)
        self.setWindowTitle("Financial Data Analysis")

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

        self.label = QLabel("Choose symbol for analysis:")
        self.label.setFont(font)
        self.menu.addWidget(self.label)

        # Select
        self.combobox = QComboBox()
        self.combobox.addItems(['AAPL', 'MSFT', 'AMZN', 'GOOG', 'FB'])
        self.menu.addWidget(self.combobox)

        # Buttons for each website to scrap
        self.button = QPushButton()
        self.button.setText("Analyze")
        self.button.clicked.connect(self.analyze)
        self.menu.addWidget(self.button)

        spacerItem = QSpacerItem(20, 40,
                                 QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self.menu.addItem(spacerItem)

        # Text browser for displaying data
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)

        # Output table widget
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.output = QTableWidget(self)
        self.output.setColumnCount(0)
        self.output.setRowCount(0)
        self.scrollArea.setWidget(self.output)
        self.layout.addWidget(self.scrollArea)

    def analyze(self):
        """
        Scrap data from TradingView
        website using Scraper class.
        """
        symbol = self.combobox.currentText()
        analysis = Analysis(symbol)
        self.display_data([
            ['SMA', analysis.sma()[0]],
            ['EMA', analysis.ema()[0]],
            ['RSI', analysis.rsi()[0]]
        ])

    def display_data(self, data):
        """
        Display data in the
        output table widget.
        """
        self.output.setColumnCount(len(data[0]))
        self.output.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.output.setItem(i, j, QTableWidgetItem(str(item)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
