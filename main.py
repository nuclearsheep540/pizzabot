import time
import getpass

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def print_logo():
    """Prints inital load ASCII"""
    print("#### PIZZABOT ####")

def user_details():
    """Get user details required to enter the website"""
    email = input('Enter your email address: ')
    password = getpass.getpass('Enter your password: ')
    postcode = input('Enter your postcode: ')
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
    """Navigate from menu to login"""
    wait_for_page_load(id_string="arrival-overlay-container", page_name="menu")

    # Close pop-up
    driver.find_element_by_class_name("arrival-red").click()

    # Click login
    driver.find_element_by_class_name("account-link").click()

def login_and_navigate_to_menu(driver, user_details):
    """Log in with email and password, then navigate to menu"""
    wait_for_page_load(id_string="loginPanel", page_name="login")
    
    # Input email
    email_input = driver.find_element_by_xpath("//input[@name='email']")
    email_input.send_keys(user_details["email"])

    # Input password
    email_input = driver.find_element_by_xpath("//input[@name='password']")
    email_input.send_keys(user_details["password"], Keys.RETURN)

    wait_for_page_load(id_string="welcome-page", page_name="welcome")

    # Navigate from welcome to menu
    driver.find_element_by_id("menu-selector").click()

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
