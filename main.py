import time
import getpass

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# NOTE: To run headless
# TODO: Add arg parser to manage this
# from selenium import webdriver from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
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
    driver = Chrome()
    driver.get("https://www.dominos.co.uk/")
    return driver

def wait_for_page_load(id_string, page_name):
    """Waits for the id string to load, or raises error message"""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id_string)))
    except:
        print(f"Unable to load {page_name} page")
        driver.quit()

def navigate_from_postcode_to_menu(driver, user_details):
    """Enter postcode and navigate to menu"""
    wait_for_page_load(id_string="search-input", page_name="postcode")

    postcode_search = driver.find_element_by_id("search-input")
    postcode_search.send_keys(user_details["postcode"], Keys.RETURN)

def navigate_from_menu_to_login(driver):
    """Closes pop-up and clicks on Login"""
    wait_for_page_load(id_string="arrival-overlay-container", page_name="menu")

    driver.find_element_by_class_name("arrival-red").click()
    driver.find_element_by_class_name("account-link").click()

def login_and_navigate_to_menu(driver, user_details):
    """Log in with email and password, then navigate to menu"""
    wait_for_page_load(id_string="loginPanel", page_name="login")

    email_input = driver.find_element_by_xpath("//input[@name='email']")
    email_input.send_keys(user_details["email"])

    email_input = driver.find_element_by_xpath("//input[@name='password']")
    email_input.send_keys(user_details["password"], Keys.RETURN)

    # NOTE: Might need an IF condition to see if are navigated to welcome or not.
    #       If we are navigated to the welcome pacge, then run this code
    # wait_for_page_load(id_string="welcome-page", page_name="welcome")
    
    # driver.find_element_by_id("menu-selector").click()

def get_pizza_menu(driver):
    """Constructs a list containing dicts of the pizza information"""
    wait_for_page_load(id_string="Speciality Pizzas", page_name="menu")

    normal_menu = driver.find_element(By.ID, 'Speciality Pizzas')
    vegan_menu = driver.find_element(By.ID, 'Vegan Friendly Pizzas')

    normal_pizzas = normal_menu.find_elements(By.TAG_NAME, 'article')
    vegan_pizzas = vegan_menu.find_elements(By.TAG_NAME, 'article')

    all_pizzas = normal_pizzas + vegan_pizzas

    pizza_menu = []
    for index, pizza in enumerate(all_pizzas):

        item = pizza.find_element(By.CLASS_NAME, 'h6')
        item_name = item.get_attribute('innerHTML').replace('&amp;','&')
        item_to_basket = item.find_element_by_xpath("//button[text()='Add To Basket']")

        pizza_menu.append({"index": index, "item": item, "name": item_name, "buy": item_to_basket})

    return pizza_menu

def order_pizza(driver):
    """Handles user choosing a pizza, and adding it to basket"""
    pizza_menu = get_pizza_menu(driver)

    print("Choose a pizza number")
    for pizza in pizza_menu:
        index = pizza["index"]
        item_name = pizza["name"]
        print(f"Pizza number {index}: {item_name}")

    order_no = input('Enter your order number: ')

    # Click on add to basket for the chosen pizza
    pizza_menu[int(order_no)]["buy"].click()

def stop_webdriver():
    """Close webdriver"""
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    print_logo()
    user_details = user_details()
    driver = initialize_chrome_webdriver()
    navigate_from_postcode_to_menu(driver, user_details)
    navigate_from_menu_to_login(driver)
    login_and_navigate_to_menu(driver, user_details)
    order_pizza(driver)
    # Checkout & Confirm
