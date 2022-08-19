from datetime import datetime
import backtrader as bt

# Class to log price data only
class LogDataStrategy(bt.Strategy):
    def next(self):
        close = self.datas[0].close[0]
        date = self.datas[0].datetime.date(0)
        # print(f'Date: {date} | Closing Price: {close}')

# Buy and Hold Strategy
class BuyAndHold(bt.Strategy):
    def __init__(self):
        self.val_start = self.broker.get_cash()
        self.order_exist = False

# Lifecycle method for next bar
    def next(self):
        if not self.order_exist:
            # Make a buy order
            size = int(self.broker.get_cash() / self.data) # gives units of stock we can buy
            self.buy(size=size)
            self.order_exist = True

# Lifecycle method for when we reach the last bar or the program stops
    def stop(self):
        roi = self.broker.get_value() / self.val_start
        print(f'ROI: {roi}')

# Basic Brokerage Cash Set & Data Fetch
def run():
    cerebro = bt.Cerebro()
    # cerebro.addstrategy(LogDataStrategy)
    cerebro.addstrategy(BuyAndHold)
    cerebro.broker.setcash(100000)
    print(f'Starting value: {cerebro.broker.getvalue()}')

    data = bt.feeds.YahooFinanceCSVData(
        dataname='SPY.csv', 
        fromdate=datetime(2000,1,1), 
        todate=datetime(2022,1,1))

    cerebro.adddata(data)
    cerebro.run()

    cerebro.plot()

    print(f'Final value: {cerebro.broker.getvalue()}')


run()