from datetime import datetime, date, timedelta
import calendar

ALLOWED_TIMEFRAMES = {
    "minute": ["1", "2", "3", "4", "5", "10", "15", "30"],
    "hour": ["1", "2", "3"],
    "day": ["1"],
    "week": ["1"],
    "month": ["1"]
}

def print_title():
    print("\nZerodha Historical Data Tool\n")

def get_valid_symbol():
    while True:
        symbol = input("Enter stock symbol (e.g., RELIANCE, INFY): ").strip().upper()
        if symbol:
            return symbol
        print("Stock symbol cannot be empty. Please try again.")

def get_valid_date(prompt):
    while True:
        date_input = input(f"Enter {prompt} date (YYYY-MM-DD): ").strip()
        try:
            user_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            if user_date >= date.today():
                print("Date cannot be today or in the future. Please enter a past date.")
            else:
                return user_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def print_valid_timeframes():
    print("Valid Timeframes:")
    for unit, values in ALLOWED_TIMEFRAMES.items():
        formatted = ", ".join([f"{v}{unit}" for v in values])
        print(f"  {unit.title()}s: {formatted}")
    print()

def get_valid_timeframe():
    print_valid_timeframes()
    while True:
        timeframe = input("Enter timeframe (e.g., 15minute, 1hour, 1day): ").strip().lower()
        for unit in ALLOWED_TIMEFRAMES:
            if timeframe.endswith(unit):
                number = timeframe.replace(unit, "")
                if number in ALLOWED_TIMEFRAMES[unit]:
                    return timeframe
        print("Invalid timeframe. Please enter a valid one from the list above.")

def split_date_range_monthly(start_date_str, end_date_str):
    """
    Splits the duration from start_date to end_date into monthly intervals.
    Returns a list of (start_date, end_date) tuples in YYYY-MM-DD format.
    """
    result = []

    #start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    #end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    current = start_date_str

    while current <= end_date_str:
        # Get last day of the current month
        last_day = calendar.monthrange(current.year, current.month)[1]
        end_of_month = datetime(current.year, current.month, last_day).date()

        interval_end = min(end_of_month, end_date_str)

        result.append((current.strftime("%Y-%m-%d"), interval_end.strftime("%Y-%m-%d")))

        # Move to next day after current interval
        current = interval_end + timedelta(days=1)

    return result

def normalize_timeframe(timeframe):
    """
    Converts verbose timeframes like '1minute', '1hour' to shortened format like 'minute', 'hour'.
    """
    mapping = {
        "1minute": "minute",
        "1hour": "hour",
        "1day": "day",
        "1week": "week",
        "1month": "month"
    }
    return mapping.get(timeframe.lower(), timeframe)

def generate_historical_url(instrument_token, timeframe, start_date, end_date, kite_username):
    """
    Constructs Zerodha historical data URL with given parameters.
    """
    base_url = "https://kite.zerodha.com/oms/instruments/historical/"
    return (
        f"{base_url}{instrument_token}/{timeframe}"
        f"?user_id={kite_username}&oi=1&from={start_date}&to={end_date}"
    )

def generate_filename(symbol, start_date, end_date, timeframe):
    """
    Generates a filename in the format:
    SYMBOL-STARTDATE-ENDDATE-TIMEFRAME.csv
    Example: RELIANCE-2024-01-01-2024-03-01-5minute.csv
    """
    return f"{symbol}_{start_date}_{end_date}_{timeframe}.csv"

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
