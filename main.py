from src import logger
from src.components.fyers_login import fyers_login
from src.components.data_retrieval import DataRetrieval
from src.components.compression_screener_2 import CMPScreener

def login():
    STAGE="login Stage"
    try:
        logger.info(f"-----{STAGE}-----")
        login=fyers_login.login()
        logger.info(f"{STAGE} sucessful")
    except Exception as e:
        logger.exception(e)
        raise e
    

def user_data_retiver():
    STAGE="user information- Stage"
    try:
        logger.info(f"-----{STAGE}-----")
        data=DataRetrieval()
        data.userdata()
        data.hist_data()
        logger.info(f"{STAGE} sucessful")
    except Exception as e:
        logger.exception(e)
        raise e
    



def screening():
    STAGE="COMPRESSION SCREENING PHASE"
    try:
        logger.info(f"----- {STAGE} -----")
        scr=CMPScreener()
        signals=scr.generate_signals()
        print(signals)
        logger.info(f"{STAGE} successful")

    except Exception as e:
        logger.exception(f"{STAGE} failed: {e}")
        raise


if __name__=="__main__":
    login()
    user_data_retiver()
    screening()

#    historical_data()
#    screening()
