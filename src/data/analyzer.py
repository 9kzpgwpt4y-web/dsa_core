import pandas as pd

class TechAnalyzer:
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        # 计算 5, 10, 20 日均线
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        # 计算乖离率
        df['bias_5'] = (df['close'] - df['ma5']) / df['ma5'] * 100
        return df.dropna()