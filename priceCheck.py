import pyautogui
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
import time

inp_website_count = int(input("Website Count: "))

options = Options()

options.set_preference("network.http.pipelining", True)
options.set_preference("browser.cache.memory.capacity", 65536)
options.set_preference("browser.display.show_image_placeholders", False)
options.set_preference("network.http.pipelining.maxrequests", 8)
options.set_preference("permissions.default.image", 2)
options.set_preference("geo.prompt.testing", True)
options.set_preference("geo.prompt.testing.allow", False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))





###########################################
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize the Google Sheets API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('api_data.json', scope)
client = gspread.authorize(credentials)

# Open a specific Google Sheet by its title
spreadsheet = client.open('JawadPrice')

#################################################

site = spreadsheet.get_worksheet(0)
price = spreadsheet.get_worksheet(1)


price_list = price.col_values(ord('A') - ord('A') + 1)
header = price_list[0]
price_list = price_list[1:]

print(price_list)












def open_website(website_name):
    pyautogui.FAILSAFE = False
    pyautogui.click(0,0)
    driver.get(website_name)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.d-block.ratio.ratio-1x1.overflow-hidden.bg-white')))

def open_product(product_number):

    product_xpath = "/html/body/main/div/div/div/div[2]/div["+str(product_number)+"]"

    elements = driver.find_elements(By.XPATH, product_xpath)

    if elements:
        print("xpath available")
        driver.find_element(By.XPATH, product_xpath).click()
        print("clicked on the xpath")


        chenge_pack()

    else:
        print("xpath not available")


def match_price(product_url, selected_pack):
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'price')))

    price_data = driver.find_element(By.CLASS_NAME, 'price').find_element(By.TAG_NAME, 'span').text

    print(price_data)

    if price_data in price_list:
        print(price_data, "Found on the price list")
        matched_row = price.find(price_data).row
        matched_col = price.find(sirialNo).col
        product_url_with_formula = f'=HYPERLINK("{product_url}", "Data Found")'
        price.update_cell(matched_row, matched_col, product_url_with_formula)

    else:
        print(price_data, "Not found in price list")

def chenge_pack():
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'price')))
    # Locate the <select> element by ID


    select_element = driver.find_element(By.CLASS_NAME, "form-select")

    # Use the Select class to interact with the dropdown
    dropdown = Select(select_element)

    # Get all options from the dropdown
    options1 = dropdown.options

    try:
        for option in options1:
            # Change the selected option every 3 seconds
            dropdown.select_by_value(option.get_attribute("value"))

            # Print the selected option
            print("Selected Option:", option.text)
            current_product_url = driver.current_url
            current_pack = option.text

            match_price(current_product_url, current_pack)


            # Wait for 3 seconds
            time.sleep(0.3)

    except Exception as e:
        print(f"An error occurred: {e}")


def total_website():
    # Specify the column letter (e.g., 'A', 'B', 'C', etc.)
    column_letter = 'A'

    # Get all values in the specified column
    column_data = site.col_values(ord(column_letter) - ord('A') + 1)

    # Remove the header if needed
    header = column_data[0]
    column_data = column_data[1:]

    # Count how many data points are in the column
    count_of_data = len(column_data)
    return count_of_data

website_count = inp_website_count
while website_count <= (total_website()+1):
    sirialNo = site.cell(website_count, 1).value
    website = site.cell(website_count, 2).value

    print(sirialNo)
    print(website)

    open_website(website)
    product_count = 1


    def open_product_link():
        # Find all anchor elements with a specific class that contains product information
        product_links = driver.find_elements(By.CSS_SELECTOR, 'a.d-block.ratio.ratio-1x1.overflow-hidden.bg-white')
        print(product_links)

        all_product_links = []

        # Extract and print the href attribute of each product link
        for link in product_links:
            product_url = link.get_attribute("href")
            all_product_links.append(product_url)

        for np_product_url in all_product_links:
            driver.get(np_product_url)
            chenge_pack()

    open_product_link()

    website_count += 1



