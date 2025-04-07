import requests
import pandas as pd
from io import StringIO

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
