import ta

def compute_indicators(df):
    """
    Compute indicators safely
    """
    df = df.copy()

    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['EMA_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['EMA_50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()

    # Drop rows ONLY if Close is missing
    df = df[df['Close'].notna()]

    return df
