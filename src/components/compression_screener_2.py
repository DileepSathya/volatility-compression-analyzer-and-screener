import pandas as pd
import numpy as np
from src.configurations.config import config_manager
from datetime import datetime, timedelta,date


class CMPScreener:

    def __init__(self, lookback=20, percentile_threshold=20):
        self.lookback = lookback
        self.percentile_threshold = percentile_threshold

        self.df = self._load_data()
        self._prepare_data()

    def _load_data(self):
        file_path = config_manager.json_file_path()
        df = pd.read_json(file_path)
        df = df.sort_values(['symbol', 'date']).copy()
        df['range'] = round(((df['high'] - df['low']) / df['low']) * 100,2)
        return df

    def _rolling_percentile_rank(self, series):
        current_value = series.iloc[-1]
        past_values = series.iloc[:-1]
        return (past_values <= current_value).sum() / len(past_values) * 100

    def _prepare_data(self):
        self.df['percentile_rank'] = (
            self.df.groupby('symbol')['range']
            .transform(lambda x: x.rolling(self.lookback + 1)
                       .apply(self._rolling_percentile_rank, raw=False))
        )

        self.df["d-1_percentile_rank"] = (
            self.df.groupby('symbol')['percentile_rank'].shift(1)
        )

        self.df['next_day_range'] = (
            self.df.groupby('symbol')['range'].shift(-1)
        )


    def generate_signals(self):

        signals = self.df[
            (self.df['percentile_rank'].notna()) &
            (self.df['d-1_percentile_rank'].notna()) &
            (self.df['percentile_rank'] <= self.percentile_threshold) &
            (self.df['d-1_percentile_rank'] <= self.percentile_threshold)
        ].copy()

        signals['date']=pd.to_datetime(signals['date'])
        latest = signals.loc[signals['date'].idxmax()]

        return latest[['symbol','date','range','percentile_rank','d-1_percentile_rank']]