from selenium import webdriver
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

class appBot(): 
  def __init__(self):
    self.driver = webdriver.Chrome()
  def open_linkedin(self):
    self.driver.get('https://www.linkedin.com/')

    sleep(3)

    login = self.driver.find_element('xpath', '/html/body/nav/div/a[2]')
    login.click()
    
    sleep(2)
    bot.linkedin_login()

  def linkedin_login(self):
    username_input = self.driver.find_element('xpath', '/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input')
    password_input = self.driver.find_element('xpath', '/html/body/div[1]/main/div[2]/div[1]/form/div[3]/input')
    login_button = self.driver.find_element('xpath', '/html/body/div[1]/main/div[2]/div[1]/form/div[4]/button')

    username = os.getenv("BOT_USERNAME")
    password = os.getenv("BOT_PASSWORD")

    username_input.send_keys(username)
    password_input.send_keys(password)
    
    login_button.click()

    sleep(50)



bot = appBot()
bot.open_linkedin()
