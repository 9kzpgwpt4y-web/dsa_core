import pandas as pd
import akshare as ak
from datetime import datetime, timedelta
from src.data.provider import DataProvider
from src.utils.logger import logger

def filter_a_share_pool():
    logger.info("开始获取 A 股全市场实时行情数据...")
    try:
        # 修改为更稳定的接口
        df_spot = ak.stock_zh_a_spot()
        
        # 注意：不同接口返回的列名可能略有不同
        # 打印一下列名，看看是否匹配（如果列名不对，我们再调整）
        # print(df_spot.columns) 
        
        # 如果 stock_zh_a_spot 的列名是 '总市值', '市盈率' 等，保持逻辑不变
        # ... 后续筛选代码 ...
        return df_spot
    except Exception as e:
        logger.error(f"全市场数据过滤失败: {e}")
        return pd.DataFrame()

def main():
    # 1. 获取符合资产池条件的标的
    pool_df = filter_a_share_pool()
    if pool_df.empty:
        return
        
    print("\n" + "="*50)
    print("入选标的池 (Top 5):")
    print(pool_df.head())
    print("="*50 + "\n")

    # 2. 获取近一年的日期范围
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    # 3. 选取前两只股票拉取历史数据验证管道
    test_symbols = pool_df['代码'].head(2).tolist()
    test_names = pool_df['名称'].head(2).tolist()

    for symbol, name in zip(test_symbols, test_names):
        logger.info(f"正在验证数据连通性 -> {name} ({symbol})")
        hist_df = DataProvider.get_a_share_hist(symbol, start_date, end_date)
        
        if not hist_df.empty:
            logger.success(f"{name} 历史数据获取成功! 数据量: {len(hist_df)} 条")
            print(hist_df.tail(3))  # 打印最后3天的量价数据检查字段结构
            print("-" * 30)

if __name__ == "__main__":
    main()