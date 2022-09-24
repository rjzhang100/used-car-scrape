from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import time 
import pandas as pd
import pwinput
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option( "prefs", {'protocol_handler.excluded_schemes.tel': False})
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.facebook.com/marketplace/category/vehicles')

#Sign in to Facebook
email_field = driver.find_element_by_id("email")
pass_field = driver.find_element_by_id("pass")
login_button = driver.find_element_by_id("loginbutton")
email_in = input(print(("Enter email: ")))
pass_in = pwinput.pwinput(mask = '*')
email_field.send_keys(email_in)
pass_field.send_keys(pass_in)
login_button.click()

#Function that scrolls to the bottom of the page
def auto_scroll(wait_load_time: int):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(wait_load_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


#Scroll to bottom of page
for _ in range(10):
    auto_scroll(1)

soup = BeautifulSoup(driver.page_source, features = 'html.parser')
name_class = "b6ax4al1 lq84ybu9 hf30pyar om3e55n1"
price_class = "gvxzyvdx aeinzg81 t7p7dqev gh25dzvf tb6i94ri gupuyl1y i2onq4tn b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas f5mw3jnl hxfwr5lz hpj0pwwo sggt6rq5 innypi6y pbevjfx6"
location_class_umbrella = "gvxzyvdx aeinzg81 t7p7dqev gh25dzvf tb6i94ri gupuyl1y i2onq4tn b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas f5mw3jnl szxhu1pg nfkogyam kkmhubc1 tes86rjd rtxb060y"
location_class = "b6ax4al1 lq84ybu9 hf30pyar om3e55n1 oshhggmv qm54mken"
mileage_class = "b6ax4al1 lq84ybu9 hf30pyar om3e55n1 oshhggmv qm54mken"
listing_class = "bdao358l alzwoclg cqf1kptm sl27f92c mmwt03ec s1m0hq7j rj2hsocd mfclru0v qulk4ar7 r0sq1yji"

#Function that checks if string contains numbers
def has_numbers(string: str) -> bool:
    return any(char.isdigit() for char in string)

#Lists to store data 
names = []
prices = []
locations = []
mileages = []

#Iterate through soup, pull and append appropriate data per listing
for result in soup.find_all(class_ = listing_class):
    for name in result.find_all(class_ = name_class):
        names.append(name.get_text())
    for price in result.find_all(class_ = price_class):
        prices.append(price.get_text())
    for location in result.find_all(class_ = location_class):
        if (not has_numbers(location.get_text())):
            locations.append(location.get_text())
    for mileage in result.find_all(class_ = mileage_class):
        if (has_numbers(mileage.get_text())):
            mileages.append(mileage.get_text())
        elif (mileage.get_text() == ""):
            mileages.append("")
    

#Store as dataframe and send to CSV
car_data = list(zip(names, prices, locations, mileages))
df = pd.DataFrame(car_data, columns = ["Name", "Price", "Location", "Mileage"])
df.to_csv("output/car_data.csv")