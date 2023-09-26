from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import sys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.common import NoSuchElementException


# https://finance.yahoo.com/quote/AMZN
def scrape(ticker_symbol: str):
   yahoo_url = f'https://finance.yahoo.com/quote/{ticker_symbol}'
   yahoo_scraping(yahoo_url)


def clic_button(driver, button):
    try:
        button = driver.find_element(By.CSS_SELECTOR, button)
        button.click()
    except NoSuchElementException:
        print(f'cant find button:{button}')


def clic_cookies(driver, element, button, wait):
   try:
       # wait up to 3 seconds for the consent modal to show up
       consent_overlay = WebDriverWait(driver, wait).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, element)))

       # click the "Accept all" button
       accept_all_button = consent_overlay.find_element(By.CSS_SELECTOR, button)
       accept_all_button.click()
   except TimeoutException:
      print(f'cant find:{element}')


def yahoo_scraping(url):
   options = Options()
   options.add_argument('--headless=new')
   driver = webdriver.Chrome(
      service=ChromeService(ChromeDriverManager().install()),
      #options=options
                             )
   driver.set_window_size(1920, 1080)
   driver.get(url)
   clic_cookies(driver, '.consent-overlay', '.accept-all', wait=10)
   driver.find_element(By.XPATH, "//*[@id=\"interactive-2col-qsp-m\"]/ul/li[7]/button").click()  # clic 5y button to get mor data

   time.sleep(3)
   driver.quit()


if __name__ == '__main__':
   sys.argv.append('AMZN')
   if len(sys.argv) <= 1:
      print('Ticker symbol CLI argument missing!!')
   else:
      scrape(sys.argv[1])
