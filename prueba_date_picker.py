from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver.exe")
driver.get("http://webapplayers.com/inspinia_admin-v2.9.4/form_advanced.html")
time.sleep(3)
elemento = driver.find_element_by_xpath('//*[@id="data_1"]/div/input')
elemento.clear()
elemento.send_keys("01-02-25")
elemento.send_keys(Keys.TAB)