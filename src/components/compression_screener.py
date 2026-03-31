import pandas as pd
from src.configurations.config import config_manager
class cmp_screener:
    def __init__(self):
        file_path=config_manager.json_file_path()
        df=pd.read_json(file_path)
  

# Ensure sorted by date ascending
        df = df.sort_values('date')

        # Take last 21 days (20 lookback + today)
        df = df.tail(22).copy()

        # Calculate daily range %
        df['range'] = (round((df['high'] - df['low']) / df['low']) * 100,2)

        # Separate today and lookback
        today_range = df.iloc[-1]['range']
 
        lookback_ranges = df.iloc[:-1]['range']  # previous 20 days

        # Percentile rank calculation
        percentile_rank = (lookback_ranges <= today_range).sum() / len(lookback_ranges) * 100

        print("Today's Range:", today_range)
        print("Percentile Rank:", percentile_rank)

if __name__=="__main__":
    cmp_screener()
