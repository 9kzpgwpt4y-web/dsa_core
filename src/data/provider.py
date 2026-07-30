import pandas as pd
import akshare as ak
import yfinance as yf
from datetime import datetime, timedelta
from src.utils.logger import logger

class DataProvider:
    @staticmethod
    def get_a_share_hist(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取 A 股前复权日线数据
        """
        try:
            # --- 新增过滤逻辑 ---
            # 北交所数据接口有时不稳定或格式不同，先跳过
            if symbol.lower().startswith('bj'):
                logger.warning(f"跳过北交所标的: {symbol}，目前仅支持沪深主板/创业板")
                return pd.DataFrame()
            # ------------------

            logger.info(f"正在获取 A 股数据: {symbol}")
            start = start_date.replace("-", "")
            end = end_date.replace("-", "")
            
            # 核心接口调用
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start, end_date=end, adjust="qfq")
            
            if df.empty:
                logger.warning(f"股票 {symbol} 返回数据为空")
                return pd.DataFrame()

            # 统一字段重命名
            rename_map = {
                "日期": "date", "开盘": "open", "最高": "high", 
                "最低": "low", "收盘": "close", "成交量": "volume"
            }
            df = df.rename(columns=rename_map)
            df['date'] = pd.to_datetime(df['date'])
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            df.set_index('date', inplace=True)
            return df

        except Exception as e:
            logger.error(f"获取 {symbol} 数据失败: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def get_us_share_hist(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取美股日线数据
        """
        try:
            logger.info(f"正在获取美股数据: {ticker}")
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(start=start_date, end=end_date)
            
            if df.empty: return pd.DataFrame()

            df.reset_index(inplace=True)
            df.columns = [col.lower() for col in df.columns]
            df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            df.set_index('date', inplace=True)
            return df
        except Exception as e:
            logger.error(f"获取 {ticker} 数据失败: {str(e)}")
            return pd.DataFrame()