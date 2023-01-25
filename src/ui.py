from matplotlib import ticker, pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QVBoxLayout, QSpacerItem, QPushButton,
                             QSizePolicy, QScrollArea, QLabel,
                             QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5.QtGui import QFont
from threading import Thread
from analysis import Analysis
from api import API
import sys


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.api = API()
        self.symbols = {
            'stocks': None,
            'forex': None,
            'crypto': None,
            'commodities': None
        }
        self._init_ui()
        self.update_symbols()

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
        thread = Thread(target=self._update_symbols)
        thread.start()

    def _update_symbols(self):
        """
        Start the update in a separate
        thread. This is done to prevent
        the GUI from freezing.
        List all available symbols
        for the selected category and
        add them to the symbols list.
        """
        self.symbol.setEnabled(False)
        self.symbol.clear()
        category = self.category.currentText().lower()
        if self.symbols[category] is not None:
            self.symbol.addItems(self.symbols[category])
        else:
            symbols = self.api.list_category(category)['symbol']
            symbols = symbols.sort_values()
            self.symbols[category] = symbols
            self.symbol.addItems(symbols)
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
        symbol = self.symbol.currentText()
        analysis = Analysis(symbol)
        self.display_data([
            ['SMA', analysis.sma()[0]],
            ['EMA', analysis.ema()[0]],
            ['RSI', analysis.rsi()[0]]
        ])
        self.plot_candles(analysis.data.iloc[-30:])

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

    def plot_candles(self, data):
        """
        Plot candlestick chart
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#131722')
        ax.tick_params(axis='x', colors='#F0F0F0')
        ax.tick_params(axis='y', colors='#F0F0F0')
        ax.grid(color='#F0F0F0', linestyle='--', linewidth=0.5)
        ax.set_xticks(range(1, len(data) + 1))
        ax.set_xticklabels(data['date'])

        highest = data['high'].max()
        lowest = data['low'].min()
        if 'volume' in data.columns:
            max_volume = data['volume'].max()
        else:
            data.loc['volume'] = None
        for i, (o, h, c, l, v) in enumerate(
                data[['open', 'high', 'close', 'low', 'volume']].values):
            if c >= o:
                color = '#2BA59A'
            else:
                color = '#EF5350'
            ax.add_patch(plt.Rectangle(
                (i + 1, o), 0.618, (c - o),
                color=color))
            ax.add_line(plt.Line2D(
                [i + 1.309, i + 1.309], [l, h],
                color=color, linewidth=1))
            if v is not None:
                plt.axvspan(i + 0.809, i + 1.809,
                            ymax=(v / max_volume / 6.18),
                            facecolor=color, alpha=0.5)
        if lowest - 0.05 * (highest - lowest) < 0:
            ax.set_ylim([0, highest + 0.05 * (highest - lowest)])
        else:
            ax.set_ylim([lowest - 0.05 * (highest - lowest),
                         highest + 0.05 * (highest - lowest)])
        ax.set_xlim([0, len(data.index) + 2])
        ax.grid(True, color='#38414E', linewidth=0.5)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=20))
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
