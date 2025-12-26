from playwright.sync_api import sync_playwright
import logging
import os
from datetime import date
logging.basicConfig(filename=f"loggs/{date.today().strftime("%d-%m-%Y")}_log.log",filemode='w',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def _get_playwright_launch_opts():
    """Return a dict of options for playwright.launch().
    Uses PLAYWRIGHT_HEADLESS env var (1/true/yes = headless) or falls back
    to enabling headless mode when running in CI (CI env var present).
    In CI we also add safe startup args to avoid sandbox issues."""
    headless_env = os.getenv('PLAYWRIGHT_HEADLESS')
    if headless_env is not None:
        headless = headless_env.lower() in ('1', 'true', 'yes')
    else:
        headless = os.getenv('CI') is not None

    opts = {'headless': headless}
    if os.getenv('CI') is not None:
        opts['args'] = ['--no-sandbox', '--disable-dev-shm-usage']

    return opts
def fetch_nse_gainer_data():
    GAINER_URL="https://www.nseindia.com/api/live-analysis-variations?index=gainers&type=allSec&csv=true"

    with sync_playwright() as p:
        opts = _get_playwright_launch_opts()
        browser = p.chromium.launch(**opts)
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
        logging.info("Fetched Gainer Data from NSE")
    return str(gainer_data)

def fetch_nse_looser_data():
    LOOSER_URL="https://www.nseindia.com/api/live-analysis-variations?index=loosers&type=allSec&csv=true"
    with sync_playwright() as p:
        opts = _get_playwright_launch_opts()
        browser = p.chromium.launch(**opts)
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
        logging.info("Fetched Looser Data from NSE")
    return (looser_data)