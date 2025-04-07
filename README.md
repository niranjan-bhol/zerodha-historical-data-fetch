# Zerodha Historical Data Jugaad

Get historical stock data from Zerodha **without paying ₹2000/month** 💸 — because why pay when you can *jugaad*?

## ⚡ What is this?

Zerodha officially charges ₹2000/month for access to their historical data API. If you're like us — broke, curious, or just love a good hack — this project is your backdoor to fetching historical stock market data using your regular **Kite login** credentials and **TOTP**.

## 🧠 How It Works

1. Logs in to your Kite account using **TOTP-based 2FA**.
2. Bypasses official API limits by scraping data from Kite's internal historical URL endpoints.
3. Automatically splits long date ranges into monthly chunks (Zerodha's hidden limit).
4. Fetches and compiles historical data — and exports to CSV for your analysis.

## 🛠️ Features

- Login with user ID, password, and TOTP key
- Generate all valid Zerodha historical data URLs based on stock, timeframe, and date range
- Fetch and stitch data across months
- Export final dataset to CSV
- Completely modular structure (`login.py`, `utility.py`, `data_fetch.py`, `request.py`, `main.py`)

## 📥 Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/niranjan-bhol/zerodha-historical-data-fetch.git
cd zerodha-historical-data-fetch
```

### 2️⃣ Install Dependencies
Make sure you have Python installed, then run:

```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a .env file and add your Zerodha credentials:

```sh
KITE_USERNAME=your_username
KITE_PASSWORD=your_password
KITE_TOTP_KEY=your_totp_secret"  # Get this from your TOTP setup (Google Authenticator, etc.) | refer YouTube video in resources
```

### 4️⃣ Run the Application
To fetch and export data:

```sh
python main.py
```

Follow the on-screen options to continue.

## 📚 Resources

- Zerodha Kite API Docs: [link](https://kite.trade/docs/connect/v3/)
- YouTube Tutorial: [link](https://youtu.be/HIpT1in7pCM?si=cnPrd9LJGfE-ln44)

<br>
Made with ❤️ and jugaad by a curious coder.

enjoy!
