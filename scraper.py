from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Scraper:
    """
    This class use Selenium library to scrap data from
    various websites, such as Yahoo Finance, TradingView,
    Investing.com, etc. It uses a browser to download
    data from the website and then parse it to get the
    desired output format.
    """

    def __init__(self):
        self._init_driver()

    def _init_driver(self):
        """Initialize the browser"""
        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def scrap_yahoo_finance(self):
        """
        Download stock market data on commodities
        from the Yahoo Finance website
        """
        self.driver.get('https://finance.yahoo.com/commodities')

        # Cookies consent
        self.driver.find_element(
            By.ID, 'consent-page'
        ).find_elements(
            By.CLASS_NAME, 'btn'
        )[0].click()

        # Get data from the table
        data = []
        for i in range(1, 38):  # 37 rows
            row = []
            for j in range(1, 8):  # 7 columns
                xpath = f'//*[@id="list-res-table"]/div[1]/table/tbody/tr[{i}]/td[{j}]'
                row.append(self.driver.find_element('xpath', xpath).text)
            data.append(row)

        return data

    def quit(self):
        """Close the browser"""
        self.driver.quit()

if __name__ == '__main__':
    scraper = Scraper()
    print(*scraper.scrap_yahoo_finance(), sep='\n')
    scraper.quit()
