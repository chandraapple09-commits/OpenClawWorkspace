def calculate_hike_probability(df):
    """
    Rule-based hike probability (0 to 1)
    """
    latest = df.iloc[-1]
    probability = 0.0

    # RSI logic
    if latest['RSI'] < 30:
        probability += 0.30
    elif latest['RSI'] < 45:
        probability += 0.15

    # Trend logic
    if latest['EMA_20'] > latest['EMA_50']:
        probability += 0.30

    # Momentum
    if latest['MACD'] > 0:
        probability += 0.20

    # Price strength
    if latest['Close'] > df['Close'].rolling(20).mean().iloc[-1]:
        probability += 0.20

    return min(probability, 1.0)
