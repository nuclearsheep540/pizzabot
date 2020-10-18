from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def print_logo():
    print("#### PIZZABOT ####")

def user_details():
    """Get user details required to enter the website"""
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    # postcode = input('Enter your postcode: ')
    postcode = "CM12 0HD"
    return dict(username=username, password=password, postcode=postcode)

def initialize_webdriver():
    """TODO"""
    driver = Chrome()
    driver.get("https://www.dominos.co.uk/")
    return driver

def navigate_from_postcode_to_menu(driver, user_details):
    """TODO"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-input"))
        )
    except:
        print("Unable to load postcode page")
        driver.quit()

    postcode_search = driver.find_element_by_id("search-input")
    postcode_search.send_keys(user_details["postcode"], Keys.RETURN)

def navigate_from_menu_to_login(driver):
    """TODO"""
    # might need to get another ID of the menu just incase the pop-up stops showing up
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "arrival-overlay-container"))
        )
    except:
        print("Unable to load menu page")
        driver.quit()

    # Close pop-up
    driver.find_element_by_class_name("arrival-red").click()

    # Click login
    driver.find_element_by_class_name("account-link").click()

def login_and_navigate_to_menu(driver):
    """TODO"""
    

    

# pizza_menu = #selenium get class menu-products-list
# for "pizza" in pizza_menu, do:
    # pizza_id = article id

    # for (selenium get every article tag in pizza) do:
        # return pizza_name = the innerHTML where p class = "product title"
    
    # return pizza(pizza_id, pizza_name)



def stop_webdriver():
    """Close webdriver"""
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    print_logo()
    user_details = user_details()
    driver = initialize_webdriver()
    navigate_from_postcode_to_menu(driver, user_details)
    navigate_from_menu_to_login(driver)
    login_and_navigate_to_menu(driver)
