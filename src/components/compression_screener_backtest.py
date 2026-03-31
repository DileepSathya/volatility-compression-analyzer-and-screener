import pandas as pd
import numpy as np

LOOKBACK = 20
df=pd.read_json("C:/Users/Dileep Sathya/OneDrive/Desktop/financial markets/compression_screener/artifacts/hist_data.json")
df = df.sort_values('date').copy()

# Calculate range %
df['range'] = ((df['high'] - df['low']) / df['low']) * 100

def rolling_percentile_rank(series):
    current_value = series.iloc[-1]
    past_values = series.iloc[:-1]
    return (past_values <= current_value).sum() / len(past_values) * 100

df['percentile_rank'] = (
    df['range']
    .rolling(window=LOOKBACK + 1)
    .apply(rolling_percentile_rank, raw=False)
)

df["d-1_percentile_rank"]=df['percentile_rank'].shift(1)
df["d-2_percentile_rank"]=df['percentile_rank'].shift(2)


df = df[
    (df['percentile_rank'].notna()) &
    (df['d-1_percentile_rank'].notna()) &
    (df['percentile_rank'] <= 20) &
    (df['d-1_percentile_rank'] <= 20 ) 
]
print(df[['symbol','date']])