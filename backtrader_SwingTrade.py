from datetime import datetime
import backtrader as bt

class SwingTrade(bt.SignalStrategy):
    params = (("closeThreshold",3),)

    def __init__(self):
        self.sma1 = bt.ind.SMA(period = 1400)

    def next(self):
        weekday = self.data.datetime.date().isoweekday()
        print(weekday)

        if self.data.close[0] < (self.sma1[0]*1.1) and weekday == 1:     # Buy only on Monday
            self.buy()
            self.params.closeThreshold = 3
            print(f"Bought 1 BTC for {self.data.close[0]}")

        if self.data.close[0] > (self.sma1[0]* self.params.closeThreshold) and self.position.size > 0:
            self.close(size = 1)
            self.params.closeThreshold += 1
            print(f"Sold 1 BTC for {self.data.close[0]}")
        



cerebro = bt.Cerebro()
cerebro.addstrategy(SwingTrade)

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
cerebro.addsizer(bt.sizers.SizerFix, stake=1)

cerebro.run()
cerebro.plot()