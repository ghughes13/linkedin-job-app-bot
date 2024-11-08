from selenium import webdriver
from time import sleep
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
import os
import random

load_dotenv()

class appBot(): 
  def __init__(self):
    self.driver = webdriver.Chrome()

  def run_app(self): 
    self.open_linkedin()
    self.wait_random_time() #wait for site to load

    self.navigate_to_signin()
    self.wait_random_time() #wait for page load before invoking next function.

    self.linkedin_login()
    self.wait_random_time() #wait for login to process

    self.await_security_check_if_present()

    print('Past security')
    self.move_to_jobs()
    print('should have clicked on jobs')
    sleep(30)

  def open_linkedin(self):
    self.driver.get('https://www.linkedin.com/')

  def navigate_to_signin(self):
    button_one = self.driver.find_element('xpath', '/html/body/nav/div/a[1]')
    button_two = self.driver.find_element('xpath', '/html/body/nav/div/a[2]')
    
    if button_one.text.strip().lower() == 'sign in': #due to alternative possible layouts we need to check button position
      button_one.click()
    else:
      button_two.click()

  def find_element_from_possible_locations(self, possible_locations, element_name):
    """Tries each XPath in possible_locations and returns the element if found."""
    for xpath in possible_locations:
        try:
            element = self.driver.find_element('xpath', xpath)
            print(f"Found element at: {xpath}")
            return element  # Return the element as soon as it's found
        except NoSuchElementException:
            print(f"Element not found at: {xpath}")
            continue  # Move to the next XPath if element is not found
    print(f"{element_name} could not be located with any provided XPath.")
    return None  # Return None if none of the locations work

  def linkedin_login(self):
    potential_username_input_locations = ['/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input', '/html/body/div/main/div[2]/div[1]/form/div[1]/input']
    potential_password_input_locations = ['/html/body/div[1]/main/div[2]/div[1]/form/div[3]/input', '/html/body/div/main/div[2]/div[1]/form/div[3]/input']
    potential_login_button_locations = ['/html/body/div[1]/main/div[2]/div[1]/form/div[4]/button','/html/body/div/main/div[2]/div[1]/form/div[4]/button', '/html/body/div/main/div[2]/div[1]/form/div[3]/button', '/html/body/div/main/div[2]/div[1]/form/div[5]/button']

    username_input = self.find_element_from_possible_locations(potential_username_input_locations, 'Username Input')
    password_input = self.find_element_from_possible_locations(potential_password_input_locations, 'Password Inputs')
    login_button = self.find_element_from_possible_locations(potential_login_button_locations, 'Login Button')

      # Check if all elements were found before proceeding
    if not username_input or not password_input or not login_button:
        print("One or more login elements were not found.")
        sleep(10)
        return  # Exit the function if any element is missing

      
    self.wait_random_time()

    username = os.getenv("BOT_USERNAME")
    password = os.getenv("BOT_PASSWORD")

    sleep(1)
    username_input.send_keys(username)
    sleep(1)
    password_input.send_keys(password)
    sleep(1)
    
    login_button.click()

  def await_security_check_if_present(self):
    if "Let’s do a quick security check" in self.driver.page_source: 
      print('!!! BOT SECURITY CHECK PRESENT. PLEASE MANUALLY PASS WITHIN 15 SECONDS !!!')
      sleep(5) # Allow user to manually bypass bot test
      print('!!! 10 Seconds left !!!')
      sleep(5)
      print('!!! 5 seconds left !!!')
      sleep(5)
    
  def move_to_jobs(self):
    jobs_button = self.driver.find_element('xpath', '/html/body/div[6]/header/div/nav/ul/li[3]/a')  
    jobs_button.click()

  def search_matching_jobs(self):
    job_title_input = self.driver.find_element('xpath', '/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]')   #job input path  ||/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]
    job_location_input = self.driver.find_element('xpath', '/html/body/div[6]/header/div/div/div/div[2]/div[3]/div/div/input[1]')

    job_title_input.send_keys('Web Developer')
    job_location_input.send_keys('Dallas, Texas')

  def wait_random_time(self):
    sleep(random.randint(4,7))


bot = appBot()
bot.run_app()


