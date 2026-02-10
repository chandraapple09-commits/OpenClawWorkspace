from agents.market_analyst.agent import run_market_agent

ALERT_THRESHOLD = 75  # %

def check_alert(symbol):
    result = run_market_agent(symbol)

    if result["Hike Probability (%)"] >= ALERT_THRESHOLD:
        return (
            f"🚨 ALERT 🚨\n"
            f"{result['Stock']}\n"
            f"Price: ₹{result['Last Price']}\n"
            f"Hike Probability: {result['Hike Probability (%)']}%\n"
            f"Outlook: {result['Outlook']}"
        )
    return None
