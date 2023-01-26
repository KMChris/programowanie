from matplotlib import ticker, pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QCheckBox,
                             QVBoxLayout, QSpacerItem, QPushButton, QComboBox,
                             QSizePolicy, QLabel, QSpinBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from threading import Thread
from analysis import Analysis
from api import API
import sys
import csv


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.api = API()
        self.analysis = None
        self.bins = 50
        self.symbols = {
            'stocks': [],
            'forex': [],
            'crypto': [],
            'commodities': []
        }
        self.names = {
            'stocks': [],
            'forex': [],
            'crypto': [],
            'commodities': []
        }
        self.indicators = {
            'sma': QCheckBox('SMA'),
            'ema': QCheckBox('EMA'),
            'bollinger': QCheckBox('Bollinger Bands'),
            'rsi': QCheckBox('RSI'),
            'macd': QCheckBox('MACD'),
            'stochastic': QCheckBox('Stochastic'),
            'williams': QCheckBox('Williams %R')
        }
        self._get_symbols()
        self._init_ui()
        self.update_symbols()

    def _get_symbols(self):
        """
        Get symbols and names from CSV files
        """
        for category in self.symbols:
            with open(f'symbols/{category}.csv', 'r') as f:
                file = csv.reader(f)
                for row in file:
                    self.symbols[category].append(row[0])
                    self.names[category].append(row[1])

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
        self.category = QComboBox()
        self.category.addItems(['Stocks', 'Forex', 'Crypto', 'Commodities'])
        self.category.currentTextChanged.connect(self.update_symbols)
        self.menu.addWidget(self.category)

        self.symbol = QComboBox()
        self.symbol.setEnabled(False)
        self.menu.addWidget(self.symbol)

        # Buttons for each website to scrap
        self.button = QPushButton()
        self.button.setText("Analyze")
        self.button.clicked.connect(self.analyze)
        self.menu.addWidget(self.button)

        spacerItem = QSpacerItem(20, 40,
                                 QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self.menu.addItem(spacerItem)

        # Output table widget
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.output = QTableWidget(self)
        self.output.setColumnCount(0)
        self.output.setRowCount(0)
        self.scrollArea.setWidget(self.output)
        self.menu.addWidget(self.scrollArea)

        plt.style.use('dark_background')
        plt.rcParams['axes.linewidth'] = 0.5
        plt.rcParams['figure.facecolor'] = '#131722'
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def update_symbols(self):
        """
        Update the symbols list
        when the category is changed.
        """
        self.symbol.setEnabled(False)
        self.symbol.clear()
        category = self.category.currentText().lower()
        self.symbol.addItems(self.symbols[category])
        self.symbol.setEnabled(True)

    def analyze(self):
        """
        Analyze the data for the selected
        symbol. Display the results in
        the output table widget and plot
        the candlestick chart.
        """
        thread = Thread(target=self._analyze)
        thread.start()

    def _analyze(self):
        """
        Start the analysis in a separate
        thread. This is done to prevent
        the GUI from freezing.
        """
        index = self.symbol.currentIndex()
        category = self.category.currentText().lower()
        symbol = self.symbols[category][index]
        self.analysis = Analysis(symbol)
        self.draw_plot(self.analysis.data.iloc[-self.bins:])
        self.update_signal(self.analysis.signal)

    def draw_plot(self, data):
        """
        Draw the candlestick chart
        on the canvas.

        Parameters
        ----------
        data : pandas.DataFrame
            The data to plot.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#131722')
        ax.tick_params(axis='x', colors='#F0F0F0')
        ax.tick_params(axis='y', colors='#F0F0F0')
        ax.grid(color='#F0F0F0', linestyle='--', linewidth=0.5)
        ax.set_xticks(range(0, len(data)))
        ax.set_xticklabels(data['date'])
        ax.set_xlim([1, len(data.index) + 1])
        ax.grid(True, color='#38414E', linewidth=0.5)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=20))
        self.plot_candles(ax, data)
        self.plot_indicators(ax)
        self.figure.tight_layout()
        self.canvas.draw()

    @staticmethod
    def plot_candles(ax, data):
        """
        Plot the candlesticks on the given
        axes using provided data.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        data : pandas.DataFrame
            The data to plot.
        """
        highest = data['high'].max()
        lowest = data['low'].min()
        max_volume = data['volume'].max()
        values = data[['open', 'high', 'close', 'low', 'volume']].values
        for i, (o, h, c, l, v) in enumerate(values):
            color = '#2BA59A' if c >= o else '#EF5350'

            # Plot candle body
            ax.add_patch(plt.Rectangle((i + 1, o), 0.618,
                                       (c - o), color=color))

            # Plot high and low
            ax.add_line(plt.Line2D([i + 1.309, i + 1.309],
                                   [l, h], color=color, linewidth=1))

            # Plot volume
            ax.axvspan(i + 0.809, i + 1.809,
                       ymax=(v / max_volume / 6.18),
                       facecolor=color, alpha=0.5)
        if lowest - 0.05 * (highest - lowest) < 0:
            ax.set_ylim(0.0, highest + 0.05 * (highest - lowest))
        else:
            ax.set_ylim(lowest - 0.05 * (highest - lowest),
                        highest + 0.05 * (highest - lowest))

    def plot_indicators(self, ax):
        """
        Plot indicators on the
        candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        sma = self.indicators['sma'].isChecked()
        ema = self.indicators['ema'].isChecked()
        bollinger = self.indicators['bollinger'].isChecked()
        rsi = self.indicators['rsi'].isChecked()
        macd = self.indicators['macd'].isChecked()
        stochastic = self.indicators['stochastic'].isChecked()
        williams = self.indicators['williams'].isChecked()

        if sma and not bollinger:
            self.plot_sma(ax)
        if ema:
            self.plot_ema(ax)
        if bollinger:
            self.plot_bollinger(ax)

        # Plot indicators with a second y-axis
        if rsi or stochastic or williams:
            ax2 = ax.twinx()
            ax2.set_ylim([0, 100])
            ax2.set_yticks([0, 20, 40, 60, 80, 100])
            ax2.set_yticklabels(['0', '20', '40', '60', '80', '100'])
            ax2.tick_params(axis='y', colors='#F0F0F0')
            ax2.set_axisbelow(True)
            if rsi:
                self.plot_rsi(ax2)
            if stochastic:
                self.plot_stochastic(ax2)
            if williams:
                self.plot_williams(ax2)
            ax2.legend(loc='lower left')
        elif macd:
            ax2 = ax.twinx()
            ax2.tick_params(axis='y', colors='#F0F0F0')
            ax2.set_axisbelow(True)
            self.plot_macd(ax2)
            ax2.legend(loc='lower left')

        # Add legend on the first y-axis
        if sma or ema or bollinger:
            ax.legend(loc='upper left')

    def plot_sma(self, ax):
        pass

    def plot_ema(self, ax):
        pass

    def plot_bollinger(self, ax):
        pass

    def plot_rsi(self, ax):
        pass

    def plot_macd(self, ax):
        pass

    def plot_stochastic(self, ax):
        pass

    def plot_williams(self, ax):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
