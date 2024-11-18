from selenium import webdriver
from time import sleep
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import os
import random
import logging

load_dotenv()

class appBot(): 
  def __init__(self):

    #### Chrome Profile Setup. Adjust to your own profile path.
    self.user_data_dir = os.getenv("USER_DATA_DIR")
    self.profile_dir = os.getenv("PROFILE_DIR")
    
    #### Driver Setup & Anti-Anti-Bot Countermeasures. 
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={self.user_data_dir}")
    options.add_argument(f"profile-directory={self.profile_dir}") 
    options.add_argument("--remote-debugging-port=9222")  # Debugging port
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    options.add_experimental_option("detach", True)


    self.driver = webdriver.Chrome(options=options)
    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    userAgentArray = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    ]

    for i in range(len(userAgentArray)):
        # setting User Agent iteratively as Chrome 108 and 107
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride", {"userAgent": userAgentArray[i]}
        )
        print(self.driver.execute_script("return navigator.userAgent;"))
        self.driver.get("https://httpbin.io/headers")
    
    self.current_jobs_page = 0

  def iteration_loop(self):
    current_el = ''

    while True:
      try:
        user_input = input()

        if user_input:
          print(user_input)
          split_input = user_input.split()
          command_type = split_input[0] 
          command_input = split_input[1]

          if command_type == 'method':
            self.invoke_method(command_input)
          elif command_type == 'xpath':
            current_el = self.driver.find_element('xpath', command_input)
            print(current_el.get_attribute("outerHTML"))
          elif command_type == 'click':
            if current_el:
              print(current_el)
            else: 
              print('No element selected')
          elif command_type == 'input':
            if current_el:
              current_el.send_keys(command_input)
          elif command_type == 'exit':
            break
          else: 
              print('Invalid command')
      except Exception as e:
        logging.error(e)
        print('An error occurred')

  def run_app(self): 
    self.open_linkedin()
    # self.wait_random_time() #wait for site to load

    # self.navigate_to_signin()
    # self.wait_random_time() #wait for page load before invoking next function.

    # self.linkedin_login()
    # self.wait_random_time() #wait for login to process

    # self.await_security_check_if_present()

    # self.move_to_jobs()
    # self.wait_random_time()

    # self.search_matching_jobs()

    self.iteration_loop()

  #################################
  ###### MAIN FUNCTIONALITY #######
  #################################

  def open_linkedin(self):
    self.driver.get('https://www.linkedin.com/') 

  def navigate_to_signin(self):
    button_one = self.driver.find_element('xpath', '/html/body/nav/div/a[1]')
    button_two = self.driver.find_element('xpath', '/html/body/nav/div/a[2]')
    
    if button_one.text.strip().lower() == 'sign in': #due to alternative possible layouts we need to check button position
      button_one.click()
    else:
      button_two.click()

  def linkedin_login(self):
    potential_username_input_locations = ['/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input', '/html/body/div/main/div[2]/div[1]/form/div[1]/input']
    potential_password_input_locations = ['/html/body/div[1]/main/div[2]/div[1]/form/div[3]/input', '/html/body/div/main/div[2]/div[1]/form/div[3]/input', '/html/body/div/main/div[2]/div[1]/form/div[2]/input']
    potential_login_button_locations = ['/html/body/div[1]/main/div[2]/div[1]/form/div[4]/button','/html/body/div/main/div[2]/div[1]/form/div[4]/button', '/html/body/div/main/div[2]/div[1]/form/div[3]/button', '/html/body/div/main/div[2]/div[1]/form/div[5]/button']

    username_input = self.find_element_from_possible_locations(potential_username_input_locations, 'Email or phone')
    password_input = self.find_element_from_possible_locations(potential_password_input_locations, 'Password')
    login_button = self.find_element_from_possible_locations(potential_login_button_locations, 'Sign in')

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
    jobs_button = self.driver.find_element(By.XPATH, '//a[@href="https://www.linkedin.com/jobs/?"]')
    jobs_button.click()

  def search_matching_jobs(self):
    job_title_input = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Search by title, skill, or company']")   
    job_location_input = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Search by title, skill, or company']")

    job_title_input.send_keys('Web Developer')
    job_location_input.send_keys('Dallas, Texas, United States')
    job_location_input.send_keys(Keys.ENTER)
    self.current_jobs_page = 1

  def crawl_job_list(self):
    jobs_container = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
    print('was valid')
    jobs_list = jobs_container.find_elements(By.TAG_NAME, "li")
    print('was also valid')
    print(jobs_list)
    for job in jobs_list:
      try:
        print('trying')
        # Find and log the h1 text
        job_title = job.find_element(By.TAG_NAME, "strong")
        print(f"Job Title: {job_title.text}")
        
        # Find and click the button inside the li
        job_title_link = job.find_element(By.TAG_NAME, "a")
        # job_title_link.click()
        
        # Wait for content to load
        sleep(2)  # Adjust based on loading time or use WebDriverWait
        
        # loaded_content = driver.find_element(By.CSS_SELECTOR, "div.loaded-content")  # Example selector
        # print(f"Loaded Content: {loaded_content.text}")
        print("tried")
      except Exception as e:
          print(f"Error processing li: {e}")

  def next_jobs_page(self):
    next_page = self.driver.find_elements(By.CSS_SELECTOR, f'[aria-label="Page {self.current_jobs_page + 1}"]')
    next_page.click()

  #################################
  ########### UTILITIES ###########
  #################################

  #Used to make bot wait random times to seem less bot-like.
  def wait_random_time(self):
    sleep(random.randint(3,7))

  #Can probably rework how we select elements to make this obsolete. See move_to_jobs
  def find_element_from_possible_locations(self, possible_locations, aria_label_value): 
    for xpath in possible_locations:
        try:
            element = self.driver.find_element('xpath', xpath)
            aria_label = element.get_attribute("aria-label")

            if aria_label == aria_label_value:
              print(f"Found element at: {xpath} with aria-label '{aria_label_value}'")
              return element  # Return the element as soon as it's found with the correct aria-label
            else:
              print(f"Element found at: {xpath}, but aria-label '{aria_label}' does not match '{aria_label_value}'")
              continue  # Go to the next XPath if aria-label does not match
        except NoSuchElementException:
            print(f"Element not found at: {xpath}")
            continue  # Move to the next XPath if element is not found
    print(f"{aria_label_value} could not be located with any provided XPath.")
    return None  # Return None if none of the locations work

  #For testing or manually invoking functions while app is running
  def invoke_method(self, method_name): 
    print(method_name)
    if hasattr(self, method_name):
        method = getattr(self, method_name)
        method()
    else:
        print(f"Method '{method_name}' not found.")

bot = appBot()
bot.run_app()


