import requests
import pandas as pd
from io import StringIO
import json

def get_symbol_exchange_token_map():
    """
    Fetches Zerodha instrument list and returns a dictionary mapping:
    tradingsymbol → exchange_token
    """
    url = "https://api.kite.trade/instruments"
    response = requests.get(url)

    if response.status_code == 200:
        csv_text = response.content.decode("utf-8")
        df = pd.read_csv(StringIO(csv_text))

        # Create and return the in-memory dictionary
        return dict(zip(df["tradingsymbol"], df["instrument_token"]))
    else:
        raise Exception(f"Failed to fetch instrument list: {response.status_code}")

def fetch_and_save_symbol_token_data(
    csv_path="symbol_exchange_token.csv",
    json_path="symbol_exchange_token.json"
):
    """
    Fetch Zerodha instruments and save tradingsymbol-token map as CSV and JSON.
    
    Args:
        csv_path (str): Path to save the CSV file.
        json_path (str): Path to save the JSON file.

    Returns:
        dict: A dictionary mapping tradingsymbol to exchange_token.
    """
    url = "https://api.kite.trade/instruments"
    try:
        response = requests.get(url)
        response.raise_for_status()

        csv_text = response.content.decode("utf-8")
        df = pd.read_csv(StringIO(csv_text))

        reduced_df = df[["tradingsymbol", "exchange_token"]]
        reduced_df.to_csv(csv_path, index=False)
        print(f"✅ Saved CSV to {csv_path}")

        symbol_dict = dict(zip(reduced_df["tradingsymbol"], reduced_df["exchange_token"]))
        with open(json_path, "w") as f:
            json.dump(symbol_dict, f, indent=4)
        print(f"✅ Saved JSON to {json_path}")

        return symbol_dict

    except Exception as e:
        print(f"❌ Failed to fetch or save data: {e}")
        return {}
