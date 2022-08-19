from datetime import datetime
import backtrader as bt

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma = bt.ind.SMA(period = 50)
        price = self.data
        crossover = bt.ind.CrossOver(price, sma)
        self.signal_add(bt.SIGNAL_LONG, crossover)

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data = bt.feeds.YahooFinanceCSVData(dataname='BTC-USD.csv', fromdate=datetime(2015,1,1), todate=datetime(2022,1,24))

cerebro.adddata(data)

cerebro.addsizer(bt.sizer.AllInSizer, percents=95)

cerebro.run()
cerebro.plot()