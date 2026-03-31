import pandas as pd
import numpy as np

LOOKBACK = 20  # 7 gives total of 139 signals where as 20 gives 135 signals
percentile_threshold=20   # with lookback 20 -- percentile threshold=20 gives 139 signals, 15 -->96, 10-->60
df = pd.read_json("C:/Users/Dileep Sathya/OneDrive/Desktop/financial markets/compression_screener/artifacts/hist_data.json")
df = df.sort_values(['symbol', 'date']).copy()

# Calculate range %
df['range'] = round(((df['high'] - df['low']) / df['low']) * 100,2)

def rolling_percentile_rank(series):
    current_value = series.iloc[-1]
    

    past_values = series.iloc[:-1]
    return (past_values <= current_value).sum() / len(past_values) * 100

df['percentile_rank'] = (
    df.groupby('symbol')['range']
    .transform(lambda x: x.rolling(window=LOOKBACK + 1).apply(rolling_percentile_rank, raw=False))
)

df["d-1_percentile_rank"] = df.groupby('symbol')['percentile_rank'].shift(1)
df["d-2_percentile_rank"] = df.groupby('symbol')['percentile_rank'].shift(2)
df['next_day_range']      = df.groupby('symbol')['range'].shift(-1)

signals = df[
    (df['percentile_rank'].notna()) &
    (df['d-1_percentile_rank'].notna()) 
#    & (df['d-2_percentile_rank'].notna()) 
    &(df['percentile_rank'] <= percentile_threshold) &
    (df['d-1_percentile_rank'] <= percentile_threshold) 
#    &(df['d-2_percentile_rank'] <= percentile_threshold)
].copy()

print(signals[['symbol', 'date', 'range']].sort_values('date').to_string(index=False))

# --- Overall Summary ---
print("\n=== Overall Backtest Summary ===")
print("percentile_threshold",percentile_threshold)
print("lookback",LOOKBACK)
print(f"Total signals         : {len(signals)}")
print(f"Avg next day range    : {signals['next_day_range'].mean():.2f}%")
print(f"Max next day range    : {signals['next_day_range'].max():.2f}%")
print(f"Min next day range    : {signals['next_day_range'].min():.2f}%")
print(f"Avg compression range : {signals['range'].mean():.2f}%")

# --- Per Symbol Summary ---
THRESHOLD = 1.5

def symbol_stats(grp):
    return pd.Series({
        'signals'              : len(grp),
        'avg_compression_%'   : grp['range'].mean(),
        'avg_next_day_%'      : grp['next_day_range'].mean(),
        'max_next_day_%'      : grp['next_day_range'].max(),
        'min_next_day_%'      : grp['next_day_range'].min(),
        f'count_>_{THRESHOLD}%': (grp['next_day_range'] > THRESHOLD).sum(),
        f'count_<_{THRESHOLD}%': (grp['next_day_range'] <= THRESHOLD).sum(),
        f'%_above_{THRESHOLD}' : (grp['next_day_range'] > THRESHOLD).mean() * 100,
    })

symbol_summary = (
    signals.groupby('symbol')
    .apply(symbol_stats)
    .reset_index()
    .sort_values('avg_next_day_%', ascending=False)
)

# Round all numeric columns
numeric_cols = symbol_summary.select_dtypes(include='number').columns
symbol_summary[numeric_cols] = symbol_summary[numeric_cols].round(2)

print("\n=== Per Symbol Summary ===")
print(symbol_summary.to_string(index=False))