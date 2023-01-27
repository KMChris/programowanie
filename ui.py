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
        self.resize(1200, 600)
        self.setWindowTitle("Financial Data Analysis")

        # Create layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Menu bar
        self.menu_widget = QWidget()
        self.menu = QVBoxLayout()
        self.menu.setContentsMargins(10, 10, 10, 10)
        self.menu_widget.setLayout(self.menu)
        self.menu_widget.setFixedWidth(250)
        self.layout.addWidget(self.menu_widget)

        # Label for the menu
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.label = QLabel("Choose symbol for analysis:")
        self.label.setFont(font)
        self.menu.addWidget(self.label)

        # Select category
        self.category = QComboBox()
        self.category.addItems(['Stocks', 'Forex', 'Crypto', 'Commodities'])
        self.category.currentTextChanged.connect(self.update_symbols)
        self.menu.addWidget(self.category)

        # Symbol selection
        self.symbol = QComboBox()
        self.symbol.setEnabled(False)
        self.menu.addWidget(self.symbol)

        # Checkboxes for indicators
        self.label_indicators = QLabel("Choose indicators:")
        font.setPointSize(10)
        self.label_indicators.setFont(font)
        self.menu.addWidget(self.label_indicators)
        for indicator in self.indicators:
            self.indicators[indicator].stateChanged.connect(self.update_indicators)
            self.menu.addWidget(self.indicators[indicator])

        # Bins for histogram
        self.label_bins = QLabel("Bins for histogram:")
        self.label_bins.setFont(font)
        self.menu.addWidget(self.label_bins)
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(10, 500)
        self.bins_spinbox.setValue(self.bins)
        self.bins_spinbox.valueChanged.connect(self.update_bins)
        self.menu.addWidget(self.bins_spinbox)

        # Button for analysis
        self.button = QPushButton()
        self.button.setText("Analyze")
        self.button.clicked.connect(self.analyze)
        self.menu.addWidget(self.button)

        spacerItem = QSpacerItem(20, 40,
                                 QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self.menu.addItem(spacerItem)

        # Prediction
        self.label_prediction = QLabel("Prediction:")
        self.label_prediction.setFont(font)
        self.label_prediction.hide()
        self.menu.addWidget(self.label_prediction)

        font.setPointSize(20)
        self.signal = QWidget()
        self.signal.setStyleSheet("background-color: #66ff66")
        self.signal.setFixedHeight(50)
        self.signal_label = QLabel("BUY")
        self.signal_label.setAlignment(Qt.AlignCenter)
        self.signal_label.setFont(font)
        self.signal_label.setStyleSheet("color: #000000")
        self.signal_layout = QVBoxLayout()
        self.signal_layout.addWidget(self.signal_label)
        self.signal.setLayout(self.signal_layout)
        self.signal.hide()
        self.menu.addWidget(self.signal)

        # Plot
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
        self.symbol.addItems(self.names[category])
        self.symbol.setEnabled(True)

    def update_signal(self, signal):
        """
        Update the signal label and box
        color when the signal is changed.
        """
        self.signal_label.setText(signal.upper())
        if signal == 'buy':
            self.signal.setStyleSheet("background-color: #66ff66")
        elif signal == 'sell':
            self.signal.setStyleSheet("background-color: #ff6666")
        else:
            self.signal.setStyleSheet("background-color: #6666ff")
        self.label_prediction.show()
        self.signal.show()

    def update_indicators(self):
        """
        Update the indicators list
        when the checkboxes are changed.
        """
        if self.indicators['rsi'].isChecked() \
                or self.indicators['stochastic'].isChecked() \
                or self.indicators['williams'].isChecked():
            self.indicators['macd'].setChecked(False)
            self.indicators['macd'].setEnabled(False)
        else:
            self.indicators['macd'].setEnabled(True)

        if self.indicators['macd'].isChecked():
            self.indicators['rsi'].setChecked(False)
            self.indicators['rsi'].setEnabled(False)
            self.indicators['stochastic'].setChecked(False)
            self.indicators['stochastic'].setEnabled(False)
            self.indicators['williams'].setChecked(False)
            self.indicators['williams'].setEnabled(False)
        else:
            self.indicators['rsi'].setEnabled(True)
            self.indicators['stochastic'].setEnabled(True)
            self.indicators['williams'].setEnabled(True)

    def update_bins(self):
        """
        Update the number of bins
        for the histogram.
        """
        self.bins = self.bins_spinbox.value()

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
        """
        Plot simple moving average
        on the candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """

        sma = self.analysis.sma().iloc[-self.bins - 1:]
        ax.plot(self.bins - sma.index + 0.309,
                sma, color='#F9A825', label='SMA')

    def plot_ema(self, ax):
        """
        Plot exponential moving average
        on the candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        ema = self.analysis.ema().iloc[-self.bins - 1:]
        ax.plot(self.bins - ema.index + 0.309,
                ema, color='#42A5F5', label='EMA')

    def plot_bollinger(self, ax):
        """
        Plot Bollinger Bands on the
        candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        bb = self.analysis.bollinger().iloc[-self.bins - 1:]
        ax.plot(self.bins - bb.index + 0.309,
                bb['upper'], color='#66BB6A', label='Bollinger Bands')
        ax.fill_between(self.bins - bb.index + 0.309,
                        bb['lower'], bb['upper'],
                        color='#66BB6A', alpha=0.2)
        ax.plot(self.bins - bb.index + 0.309,
                bb['lower'], color='#66BB6A')
        self.plot_sma(ax)

    def plot_rsi(self, ax):
        """
        Plot relative strength index
        on the candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        rsi = self.analysis.rsi().iloc[-self.bins - 1:]
        ax.plot(self.bins - rsi.index + 0.309,
                rsi, color='#9C27B0', label='RSI')

    def plot_macd(self, ax):
        """
        Plot moving average convergence
        divergence on the candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        macd = self.analysis.macd().iloc[-self.bins - 1:]
        ax.plot(self.bins - macd.index + 0.309,
                macd['MACD'], color='#F44336', label='MACD')
        ax.plot(self.bins - macd.index + 0.309,
                macd['Signal'], color='#4CAF50', label='Signal')
        ax.bar(self.bins - macd.index + 0.309,
               macd['Histogram'], color='#F44336',
               alpha=0.2, width=0.618,
               align='center', label='Histogram')

    def plot_stochastic(self, ax):
        """
        Plot stochastic oscillator
        on the candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        stochastic = self.analysis.stochastic().iloc[-self.bins - 1:]
        ax.plot(self.bins - stochastic.index + 0.309,
                stochastic['%K'], color='#0094FF', label='Stochastic %K')
        ax.plot(self.bins - stochastic.index + 0.309,
                stochastic['%D'], color='#FF6A00', label='Stochastic %D')

    def plot_williams(self, ax):
        """
        Plot Williams %R
        on the candlestick chart.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        williams = self.analysis.williams().iloc[-self.bins - 1:]
        ax.plot(self.bins - williams.index + 0.309,
                williams, color='#F44336', label='Williams %R')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
