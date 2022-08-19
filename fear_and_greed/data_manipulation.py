import pandas as pd

# Add Fear & Greed Index: https://alternative.me/crypto/fear-and-greed-index/
fear_and_greed_df = pd.read_csv('fear_and_greed/fear_and_greed.csv')
# print(fear_and_greed_df)

fear_and_greed_df['Date'] = pd.to_datetime(fear_and_greed_df['Date']).dt.strftime('%Y-%m-%d')
# print(fear_and_greed_df['date'])

# Add BTC-USD price history
btc_df = pd.read_csv('fear_and_greed/BTC-USD.csv')

# Join 2 Data Sets
results = pd.merge(btc_df, fear_and_greed_df, on=['Date'])
results.to_csv('fear_and_greed/BTC-USD-fear-greed.csv', index=False)