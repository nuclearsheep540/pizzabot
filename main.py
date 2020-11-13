#!/usr/bin/env python3 # NOTE: DO WE NEED THIS?
import time
import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# NOTE: To run headless
# TODO: Add arg parser to manage this
# #chrome_options.add_argument("--disable-extensions")
# #chrome_options.add_argument("--disable-gpu")
# #chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.add_argument("--headless")
# # chrome_options.headless = True # also works


def print_logo():
    """Prints inital load ASCII"""
    print("#### PIZZABOT ####")

def user_details():
    """Get user details required to enter the website"""
    email = input('Enter your email address: ')
    password = getpass.getpass('Enter your password: ')
    postcode = input('Enter your postcode: ')
    print("\nFetching your pizza menu...\n")

    return dict(email=email, password=password, postcode=postcode)

def initialize_chrome_webdriver():
    """Initializes the chrome webdriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.dominos.co.uk/user/login")
    return driver

def wait_for_page_load(id_string, page_name):
    """Waits for the id string to load, or raises error message"""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id_string)))
    except:
        print(f"Unable to load {page_name} page")
        driver.quit()

def login_and_navigate_to_menu(driver, user_details):
    """Log in with email and password, then navigate to menu"""
    wait_for_page_load(id_string="loginPanel", page_name="login")

    email_input = driver.find_element_by_xpath("//input[@name='email']")
    email_input.send_keys(user_details["email"])

    email_input = driver.find_element_by_xpath("//input[@name='password']")
    email_input.send_keys(user_details["password"], Keys.RETURN)

    # NOTE: Might need an IF condition to see if are navigated to welcome or not.
    #       If we are navigated to the welcome pacge, then run this code
    wait_for_page_load(id_string="welcome-page", page_name="welcome")
    driver.find_element_by_id("menu-selector").click()

def get_pizza_menu(driver):
    """Constructs a list containing dicts of the pizza information"""

    ## CURRENT BUG: sometimes page loads with buy buttons for cookies, 
    ## and 'featured article', and offsets our buy button array
    wait_for_page_load(id_string="Pizza", page_name="menu")
    time.sleep(1)

    normal_menu = driver.find_element(By.ID, 'Speciality Pizzas')
    vegan_menu = driver.find_element(By.ID, 'Vegan Friendly Pizzas')

    normal_pizzas = normal_menu.find_elements(By.TAG_NAME, 'article')
    vegan_pizzas = vegan_menu.find_elements(By.TAG_NAME, 'article')

    all_pizzas = normal_pizzas + vegan_pizzas

    pizza_menu = []
    for index, pizza in enumerate(all_pizzas):
        item = pizza.find_element(By.CLASS_NAME, "h6")
        item_name = item.get_attribute("innerHTML").replace("&amp;","&")
        pizza_menu.append({"index": index, "item": item, "name": item_name})

    return pizza_menu

def select_pizza(driver):
    """Handles user choosing a pizza, and adding it to basket"""
    time.sleep(1)
    pizza_menu = get_pizza_menu(driver)

    print("Choose a pizza number")
    for pizza in pizza_menu:
        print(f"Pizza number {pizza['index']}: {pizza['name']}")

    order_number = input("Enter your order number: ")

    # Click on add to basket for the chosen pizza BUG: Can only 
    print(f"pizza {order_number} is, {pizza_menu[int(order_number)]['name']}")

    # get all buy buttons
    all_buy_buttons = driver.find_element(By.ID, 'Pizza').find_elements_by_xpath("//button[text()='Add To Basket']")

    # click the one relative to order number
    all_buy_buttons[int(order_number)].click()

    time.sleep(1)

def navigate_to_basket(driver):
    """Handles navigating to the basket page"""
    driver.get("https://www.dominos.co.uk/basketdetails/show")

def navigate_to_checkout(driver):
    """Handles navigating to the checkout page"""
    wait_for_page_load(id_string="checkoutButtonBottom", page_name="basket")
    time.sleep(1)

    basket_summary = driver.find_elements_by_class_name("basket-product-summary")
    ordered_pizza_info = []
    for index, item in enumerate(basket_summary):
        spans = item.find_elements_by_tag_name("span")
        pizza_info = [span.get_attribute("innerHTML") for span in spans]
        pizza_info_dict = {
            "item_index": index,
            "name": pizza_info[0],
            "size": pizza_info[1],
            "crust": pizza_info[2]
        }
        ordered_pizza_info.append(pizza_info_dict)
        
    driver.find_element(By.ID, "checkoutButtonBottom").click()

    return ordered_pizza_info
    

def checkout_place_order(driver, ordered_pizza_info):
    """Confirms order"""
    wait_for_page_load(id_string="page-content", page_name="fulfilment")
    time.sleep(1)
    # print the price
    sub_total = driver.find_element_by_class_name("checkout-total-price").get_attribute("innerHTML")
    address = driver.find_element_by_class_name("nav-store-name").get_attribute("innerHTML")

    print(f"\nYour order is:")
    for item in ordered_pizza_info:
        print(f"{item['size']} {item['name']} with {item['crust']}")

    print(f"\nYour order comes to a total of: {sub_total}\nDelivery to your {address} address")
    confirm = input("Confirm order [y/n]? ")
    
    # ask for input to confirm, if yes:
    if confirm is not "y":
        print("Order declined. Exiting...")
        driver.quit()
    else:
        driver.find_element_by_xpath("//button[@type='submit']").click()


if __name__ == "__main__":
    print_logo()
    user_details = user_details()
    driver = initialize_chrome_webdriver()
    login_and_navigate_to_menu(driver, user_details)
    select_pizza(driver)
    navigate_to_basket(driver)
    navigate_to_checkout(driver)
    # Checkout & Confirm
