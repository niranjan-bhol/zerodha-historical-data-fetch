import requests
import pandas as pd

class ZerodhaDataFetcher:
    def __init__(self, enctoken):
        self.enctoken = enctoken
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "https://kite.zerodha.com/dashboard",
            "Accept-Language": "en-US,en;q=0.6",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"enctoken {self.enctoken}"
        }

    def fetch_data_from_url(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            candles = data.get("data", {}).get("candles", [])
            if candles:
                df = pd.DataFrame(candles, columns=["datetime", "open", "high", "low", "close", "volume", "oi"])
                return df
            else:
                print(f"No candle data found for URL: {url}")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return pd.DataFrame()

    def fetch_all(self, urls):
        all_data = pd.DataFrame()
        for url in urls:
            #print(f"Fetching data from: {url}")
            df = self.fetch_data_from_url(url)
            if not df.empty:
                all_data = pd.concat([all_data, df], ignore_index=True)
        return all_data

    def export_to_csv(self, df, filename="historical_data.csv"):
        """
        Exports the given DataFrame to a CSV file.
        
        Parameters:
            df (pd.DataFrame): Data to export.
        filename (str): File name to save the CSV as.
        """
        try:
            df.to_csv(filename, index=False)
            print(f"✅ Data successfully exported to {filename}")
        except Exception as e:
            print(f"❌ Failed to export data: {e}")
