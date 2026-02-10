from agents.market_analyst.agent import run_market_agent

if __name__ == "__main__":
    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS"
    ]

    print("\n📊 LIVE STOCK MARKET ANALYSIS\n")

    for stock in stocks:
        try:
            result = run_market_agent(stock)
            print("-" * 50)
            for k, v in result.items():
                print(f"{k}: {v}")
        except Exception as e:
            print(f"{stock} → Error: {e}")
