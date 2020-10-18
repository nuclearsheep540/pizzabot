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
    # username = input('Enter your username: ')
    # password = input('Enter your password: ')
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

def navigate_from_menu_to_login(driver, user_details):
    """TODO"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "arrival-overlay-container"))
        )
    except:
        print("Unable to load menu page")
        driver.quit()


    driver.find_element_by_class_name("arrival-red").click()



def stop_webdriver():
    """Close webdriver"""
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    print_logo()
    user_details = user_details()
    driver = initialize_webdriver()
    navigate_from_postcode_to_menu(driver, user_details)
    navigate_from_menu_to_login(driver, user_details)
