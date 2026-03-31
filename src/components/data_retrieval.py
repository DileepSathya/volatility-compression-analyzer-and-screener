from src import logger
from fyers_apiv3 import fyersModel
from src.configurations.config import config_manager
#from src.pipeline.hist_data_retrival_pipeline import hist_data_retrival_pipeline
from datetime import datetime, timedelta,date
from src.utils.common import extract_candles_with_symbol,save_to_raw_hist_data_json,clear_hist_data_json
from src.utils.common import format_symbol

class DataRetrieval:

    def __init__(self):
        logger.info("Accessing client_id and acesstoken")
        client_id, access_token = config_manager.authentication()
        logger.info("Accessing client_id and acesstoken successful")
        self.fyers = fyersModel.FyersModel(
            client_id=client_id,
            is_async=False,
            token=access_token,
            log_path=""
        )

    def userdata(self):
        response = self.fyers.get_profile()
        print(response)
        return response

    def hist_data(self):
        data_retrivel_period=366
        file_path=config_manager.json_file_path()
        clear_hist_data_json(file_path)  
        choice = input("Do you want to retrieve custom data? (y/n): ").strip().lower()

        if choice =='y':
            trade_date = input("Enter date that you want to backtest(YYYY-MM-DD): ")
            trade_date = date.fromisoformat(trade_date)# - timedelta(days=1)

            trade_date_20=trade_date - timedelta(days=data_retrivel_period)
        else:
            trade_date = date.today()# - timedelta(days=1)
            trade_date_20 = trade_date - timedelta(days=data_retrivel_period)

        in_symbol_list = config_manager.data_loading_config()

        symbols_list = [format_symbol(symbol) for symbol in in_symbol_list]

        for symbol in symbols_list:
            range_from=trade_date_20
            range_to=trade_date

            data = {
                    "symbol": symbol,
                    "resolution": "D",
                    "date_format": "1",
                    "range_from": range_from,
                    "range_to": range_to,
                    "cont_flag": "1"
                }
            print(data)
            response = self.fyers.history(data=data)


            data_with_symbols=extract_candles_with_symbol(response_json=response,symbol=symbol)
                
            
                
            
            save_to_raw_hist_data_json(data_with_symbols,file_path)

            print(f"{symbol} data load Successful")