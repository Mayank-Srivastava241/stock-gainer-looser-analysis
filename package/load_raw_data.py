import requests
from datetime import date
def fetch_nse_gainer_data():
    gurl="https://www.nseindia.com/api/live-analysis-variations?index=gainers&type=allSec&csv=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.nseindia.com/",
        "Origin": "https://www.nseindia.com"
    }
    response = requests.get(gurl, headers=headers)
    gainer_data = response.text
    return (gainer_data)

def fetch_nse_looser_data():
    lurl="https://www.nseindia.com/api/live-analysis-variations?index=loosers&type=allSec&csv=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.nseindia.com/",
        "Origin": "https://www.nseindia.com"
    }
    response = requests.get(lurl, headers=headers)
    looser_data = response.text
    return (looser_data)