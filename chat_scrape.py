from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from datetime import date
from datetime import datetime

class SeleniumScrape:
  def __init__(self):
    self.url = None
    self.driver = None
    self.pane = None
    self.fhandle = None
    self.position = None
    self.target = None

  # arg u is the url, "https://teams.blah"
  def session_setup(self, u):
    self.url = u
    self.driver = webdriver.Firefox()
    self.driver.get(self.url)

  # arg fname is the 'path/filename' where messages will be written
  def capture_setup(self, fname):
    self.pane = self.driver.find_element_by_xpath("//div[@id='page-content-wrapper']")
    self.position = 0
    self.fhandle = open(fname,'a')

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

  # argument t is data-scroll-pos target number
  # i.e. the position of the message you are scolling back to
  def scrollback_setup(self, t):
    self.position = 0
    self.target = t

  def scrollback_loop(self):
    while self.position < self.target:
      message = WebDriverWait(self.driver, timeout=20).until(lambda d:
      self.pane.find_element_by_xpath("//div[@data-scroll-pos='{0}']".format(self.position)))
      self.driver.execute_script("arguments[0].scrollIntoView();", message)
      self.position +=5

  # 4 digit year, non-padded month and day as integers
  # pos is current data-scroll-pos, 0 if at the bottom/most recent message
  # e.g. scrollback_to_date(2020,6,1,0)
  def scrollback_to_date(self, y, m, d):
    target = date(y, m, d).toordinal()
    d = date.today().toordinal()
    while d >= target:
      message = WebDriverWait(self.driver, timeout=20).until(lambda d:
      self.pane.find_element_by_xpath("//div[@data-scroll-pos='{0}']".format(self.position)))
      self.driver.execute_script("arguments[0].scrollIntoView();", message)
      date_time = message.find_element(By.CLASS_NAME, "message-datetime")
      d = self.get_date_ordinal(date_time.get_attribute('title'))
      self.position +=5

  def get_date_ordinal(self, date_str):
    return datetime.strptime(date_str, '%b %d, %Y %I:%M %p').toordinal()

  ## cleanup
  def cleanup(self):
    self.fhandle.close()
    self.driver.quit()

