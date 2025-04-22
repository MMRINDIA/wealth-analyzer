# analyzer/engine.py

import os
import json
from datetime import datetime
from analyzer.risk_detector import detect_risks

SESSION_LOG_DIR = "outputs/session_logs/"
KNOWN_FUNDS_FILE = "outputs/known_funds.json"
os.makedirs(SESSION_LOG_DIR, exist_ok=True)

# Save known fund names (for crowd learning)
def _update_known_funds(asset_names):
    known = set()
    if os.path.exists(KNOWN_FUNDS_FILE):
        with open(KNOWN_FUNDS_FILE, "r") as f:
            try:
                known = set(json.load(f))
            except json.JSONDecodeError:
                pass
    known.update(asset_names)
    with open(KNOWN_FUNDS_FILE, "w") as f:
        json.dump(list(known), f)

# Main analysis function
def analyze_portfolio(df):
    report = {"summary": []}

    # Categorize
    df["Category"] = df["Type"].map({
        "Equity": "Equity",
        "Mutual Fund": "Equity",
        "Debt Fund": "Debt",
        "Debt": "Debt",
        "Crypto": "Crypto",
        "Gold": "Gold",
        "Cash": "Cash"
    }).fillna("Other")

    # Gain/Loss
    df["Gain/Loss"] = df["Current Value"] - df["Purchase Value"]

    # Per-asset summary
    for _, row in df.iterrows():
        asset = row["Asset Name"]
        gain = row["Gain/Loss"]
        report["summary"].append(f"✅ {'Gain' if gain > 0 else 'Loss'} from {asset}: ₹{abs(gain):,.0f}")

    # Total
    total_gain = df["Gain/Loss"].sum()
    report["summary"].append(f"\n💰 Net Gain/Loss: ₹{total_gain:,.2f}")

    # Risk insights
    report["summary"].extend(detect_risks(df))

    # Save asset names
    _update_known_funds(df["Asset Name"].tolist())

    # Optional: Save session file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = os.path.join(SESSION_LOG_DIR, f"session_{timestamp}.json")
    try:
        df.to_json(session_path, orient="records", indent=2)
    except Exception as e:
        print(f"⚠️ Failed to save session: {e}")

    return report
