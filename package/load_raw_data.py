from playwright.sync_api import sync_playwright
from datetime import date
GAINER_URL="https://www.nseindia.com/api/live-analysis-variations?index=gainers&type=allSec&csv=true"
def fetch_nse_gainer_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120 Safari/537.36"
                ),locale ="en-IN"
            )
        page = context.new_page()
        
        response = page.request.get(GAINER_URL)
        
        gainer_data = response.text()
        browser.close()
    return str(gainer_data)

def fetch_nse_looser_data():
    LOOSER_URL="https://www.nseindia.com/api/live-analysis-variations?index=loosers&type=allSec&csv=true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120 Safari/537.36"
                ),locale ="en-IN"
            )
        page = context.new_page()
        
        response = page.request.get(LOOSER_URL)
        
        looser_data = response.text()
        browser.close()
    return (looser_data)