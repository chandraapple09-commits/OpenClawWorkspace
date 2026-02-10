from agents.market_analyst.live_data import fetch_live_data
from agents.market_analyst.indicators import compute_indicators
from agents.market_analyst.hike_probability import calculate_hike_probability

def run_market_agent(symbol):
    df = fetch_live_data(symbol)
    df = compute_indicators(df)

    if df.empty:
        raise ValueError("Insufficient data after indicator calculation")

    prob = calculate_hike_probability(df)

    latest_price = df.iloc[-1]['Close']

    if prob >= 0.70:
        outlook = "HIGH HIKE POSSIBILITY"
    elif prob >= 0.40:
        outlook = "MODERATE HIKE POSSIBILITY"
    else:
        outlook = "LOW HIKE POSSIBILITY"

    return {
        "Stock": symbol,
        "Last Price": round(latest_price, 2),
        "Hike Probability (%)": round(prob * 100, 2),
        "Outlook": outlook
    }
