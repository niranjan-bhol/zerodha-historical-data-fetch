from utility import (
    print_title, get_valid_date, get_valid_timeframe, get_valid_symbol, 
    generate_filename, split_date_range_monthly, generate_historical_url, normalize_timeframe
)
from request import get_symbol_exchange_token_map
from config import KITE_USERNAME
from login import ZerodhaLogin
from data_fetch import ZerodhaDataFetcher

def main():
    print_title()

    symbol = get_valid_symbol()
    print()

    while True:
        start_date = get_valid_date("start")
        end_date = get_valid_date("end")
        print()

        if start_date > end_date:
            print("Start date cannot be after end date. Please try again.\n")
        else:
            break

    timeframe = get_valid_timeframe()

    print()
    print(f"Symbol: {symbol}")
    print(f"From: {start_date}")
    print(f"To: {end_date}")
    print(f"Timeframe: {timeframe}")
    print()
    
    timeframe_nor = normalize_timeframe(timeframe)

    ranges = split_date_range_monthly(start_date, end_date)
    """for r in ranges:
        print(r)"""

    symbol_map = get_symbol_exchange_token_map()
    instrument_tok = symbol_map.get(symbol)

    print("Instrument token:", instrument_tok)
    print()

    if instrument_tok != None:

        #url = generate_historical_url(instrument_tok, timeframe_nor, start_date, end_date, KITE_USERNAME)
        #print(url)

        # Generate all URLs
        urls = []
        for start_date, end_date in ranges:
            url = generate_historical_url(instrument_tok, timeframe_nor, start_date, end_date, KITE_USERNAME)
            urls.append(url)

        # Print all generated URLs
        """print("Generated URLs:")
        for u in urls:
            print(u)"""

        login = ZerodhaLogin()
        enctoken = login.login()
        if enctoken:
            print("✅ Login successful! Enctoken retrieved.")
            print()
        else:
            print("❌ Login failed.")
            print()
        
        fetcher = ZerodhaDataFetcher(enctoken)
        final_df = fetcher.fetch_all(urls)
        
        print("✅ Data successfully fetched.")

        #print("\n✅ Fetched Data:")
        #print(final_df)

        filename = generate_filename(symbol, start_date, end_date, timeframe)
        #print(f"\nGenerated filename: {filename}")

        # Export to CSV
        fetcher.export_to_csv(final_df, filename)

if __name__ == "__main__":
    main()
