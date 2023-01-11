from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Download stock market data on commodities from the Yahoo Finance website
driver = webdriver.Chrome()
driver.get('https://finance.yahoo.com/commodities')

# Cookies consent
driver.find_element(By.ID, 'consent-page').find_elements(By.CLASS_NAME, 'btn')[0].click()

# Get data from the table
data = []
for i in range(1, 38):  # 37 rows
    row = []
    for j in range(1, 8):  # 7 columns
        xpath = f'//*[@id="list-res-table"]/div[1]/table/tbody/tr[{i}]/td[{j}]'
        row.append(driver.find_element('xpath', xpath).text)
    data.append(row)

# Display data
print(*data, sep='\n')

# Close the browser
driver.quit()
