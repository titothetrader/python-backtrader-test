from datetime import datetime
import pandas as pd
import backtrader as bt

# Define Strategy for Fear and Greed Indicator
class FearAndGreed(bt.Strategy):
    def __init__(self):
        self.val_start = self.broker.get_cash()
        self.order_exist = False

    def next(self):
        df = pd.read_csv('fear_and_greed/BTC-USD-fear-greed.csv')
        date = self.datas[0].datetime.date(0)
        row = df.query(f'Date == "{date}"')
        fear_values = row['Fng_value'].values
        if len(fear_values) > 0:
            fear_value = fear_values[0]

            # Extreme fear make a buy order
            if fear_value < 10 and self.order_exist == False:
                size = int(self.broker.get_cash() / self.data) # gives units of stock we can buy
                self.buy(size=size)
                print(f'BUY ORDER: {fear_value, date}')
                self.order_exist = True

            # Extreme greed make a sell order
            if fear_value > 90 and self.order_exist == True:
                self.close()
                print(f'SELL ORDER: {fear_value, date}')
                self.order_exist = False


# Lifecycle method for when we reach the last bar or the program stops
    def stop(self):
        roi = self.broker.get_value() / self.val_start
        print(f'ROI: {roi}')

# Basic Brokerage Cash Set & Data Fetch
def run():
    cerebro = bt.Cerebro()
    # cerebro.addstrategy(LogDataStrategy)
    cerebro.addstrategy(FearAndGreed)
    cerebro.broker.setcash(100000)
    print(f'Starting value: {cerebro.broker.getvalue()}')

    data = bt.feeds.YahooFinanceCSVData(
        dataname='fear_and_greed/BTC-USD.csv', 
        fromdate=datetime(2000,1,1), 
        todate=datetime(2022,1,1))

    cerebro.adddata(data)
    cerebro.run()

    cerebro.plot()

    print(f'Final value: {cerebro.broker.getvalue()}')


run()