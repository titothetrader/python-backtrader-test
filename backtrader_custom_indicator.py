from datetime import datetime
import backtrader as bt

# Custom Indicator - scores price weight by distance from SMAs
class OverUnderIndicator (bt.Indicator):
    lines = ('overunder',)

    def __init__(self):
        # Define SMAs for values
        sma1 = bt.ind.SMA(period = 30)
        sma2 = bt.ind.SMA(period = 100)
        sma3 = bt.ind.SMA(period = 200)

        # Value adjusted by 1.5 to ensure positive only signals for LONG
        self.l.overunder = bt.Cmp(sma1, sma2) + bt.Cmp(sma1, sma3) - 1.5

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        # Re-define SMAs so they plot
        sma1 = bt.ind.SMA(period = 30)
        sma2 = bt.ind.SMA(period = 100)
        sma3 = bt.ind.SMA(period = 200)

        # Using just a simple SMA Cross
        # sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        # crossover = bt.ind.CrossOver(sma1, sma2)
        # self.signal_add(bt.SIGNAL_LONG, crossover)
        # OverUnderIndicator()

        # Implementing our new Custom Indicator
        ind = OverUnderIndicator()
        self.signal_add(bt.SIGNAL_LONG, ind)

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
cerebro.addsizer(bt.sizers.PercentSizer,percents = 95)

data0 = bt.feeds.YahooFinanceData(dataname='MSFT.csv', fromdate=datetime(2014, 1, 1),
                                  todate=datetime(2018, 12, 31))
cerebro.adddata(data0)

cerebro.run()
cerebro.plot()