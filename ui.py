from matplotlib import ticker, pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QVBoxLayout, QSpacerItem, QPushButton,
                             QSizePolicy, QScrollArea, QLabel,
                             QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5.QtGui import QFont
from analysis import Analysis
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
        self.plot_candles(analysis.data)

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
        self.output.resizeColumnsToContents()

    @staticmethod
    def plot_candles(data):
        """
        Plot candlestick chart
        """
        o, h, c, l, v = data['open'], data['high'], data['close'], data['low'], data['volume']
        scale = 'linear'  # scale = 'log'
        points = None
        plt.style.use('dark_background')
        plt.rcParams['axes.linewidth'] = 0.5
        plt.rcParams['figure.facecolor'] = '#131722'
        plt.gca().set_facecolor('#131722')
        highest, lowest, max_volume = h[0], l[0], v[0]
        for k in range(len(o)):
            if h[k] > highest:
                highest = h[k]
            if l[k] < lowest:
                lowest = l[k]
            if v is not None:
                if v[k] > max_volume:
                    max_volume = v[k]
        for k in range(len(o)):
            if c[k] >= o[k]:
                plt.gca().add_patch(plt.Rectangle(
                    (k + 1, o[k]), 0.618, (c[k] - o[k]),
                    color='#2BA59A'))
                plt.gca().add_line(plt.Line2D(
                    [k + 1.309, k + 1.309], [l[k], h[k]],
                    color='#2BA59A', linewidth=1))
                if v is not None:
                    plt.axvspan(k + 0.809, k + 1.809,
                                ymax=(v[k] / max_volume / 6.18),
                                facecolor='#2BA59A', alpha=0.5)
            else:
                plt.gca().add_patch(plt.Rectangle(
                    (k + 1, o[k]), 0.618, (c[k] - o[k]),
                    color='#EF5350'))
                plt.gca().add_line(plt.Line2D(
                    [k + 1.309, k + 1.309], [l[k], h[k]],
                    color='#EF5350', linewidth=1))
                if v is not None:
                    plt.axvspan(k + 0.809, k + 1.809,
                                ymax=(v[k] / max_volume / 6.18),
                                facecolor='#EF5350', alpha=0.5)
        if points is not None:
            plt.scatter(*points, color='orange', alpha=1)
        plt.yscale(scale)
        if lowest - 0.05 * (highest - lowest) < 0:
            plt.gca().set_ylim([0, highest + 0.05 * (highest - lowest)])
        else:
            plt.gca().set_ylim([lowest - 0.05 * (highest - lowest),
                                highest + 0.05 * (highest - lowest)])
        plt.gca().set_xlim([0, len(o) + 2])
        plt.gca().grid(True, color='#38414E', linewidth=0.5)
        plt.gca().set_axisbelow(True)
        plt.subplots_adjust(left=0.1, right=1, top=1, bottom=0.05)
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=15))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=30))
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
