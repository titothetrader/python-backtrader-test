from datetime import datetime
import backtrader as bt

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data0 = bt.feeds.GenericCSVData(
    dataname = "BTC-USD.csv",
    fromdate = datetime(2011,1,1),
    todate = datetime(2022,1,24),
    datetime = 0,                   # Column Order
    open = 1,
    high = 2,
    low = 3,
    close = 4,
    volume = 6,
    openinterest = -1,
    dtformat = "%Y-%m-%d"
)

cerebro.adddata(data0)
cerebro.broker.setcash(10000)

cerebro.run()
cerebro.plot()