from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time
import sys

class SeleniumScrape:
  def __init__(self):
    self.url = None
    self.driver = None
    self.pane = None
    self.fhandle = None
    self.position = None
    self.target = None

  #session setup
  def session_setup(self, u):
    self.url = u
    self.driver = webdriver.Firefox()
    self.driver.get(self.url)

  #capture setup
  def capture_setup(self, fname):
    self.pane = self.driver.find_element_by_xpath("//div[@id='page-content-wrapper']")
    self.position = 0
    self.fhandle = open(fname,'a')

  # capture messages loop
  def capture_loop(self):
    while True:
      message = WebDriverWait(self.driver, timeout=20).until(lambda d:
      self.pane.find_element_by_xpath("//div[@data-scroll-pos='{0}']".format(self.position)))
      self.position += 1
      text_div = message.find_element(By.CLASS_NAME,"message-body-content")
      person = message.find_element(By.CLASS_NAME, "ts-msg-name")
      time = message.find_element(By.CLASS_NAME, "message-datetime")
      date_time = time.get_attribute('title')
      self.fhandle.write(person.text + " " + date_time + "\n")
      self.fhandle.write(text_div.text + "\n")
      self.driver.execute_script("arguments[0].scrollIntoView();", message)
      print("position is " + str(self.position) + "\n")

  # fast scrollback setup
  def scrollback_setup(self, t):
    self.position = 0
    self.target = t

  # fast scrollback loop
  def scrollback_loop(self):
    while self.position < self.target:
      message = WebDriverWait(self.driver, timeout=20).until(lambda d:
      self.pane.find_element_by_xpath("//div[@data-scroll-pos='{0}']".format(self.position)))
      self.driver.execute_script("arguments[0].scrollIntoView();", message)
      self.position +=5

  ## cleanup
  def cleanup(self):
    self.fhandle.close()
    self.driver.quit()

