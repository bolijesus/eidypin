from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver.exe")
driver.get("http://webapplayers.com/inspinia_admin-v2.9.4/form_advanced.html")
#driver.get("http://google.com")

elemento = driver.find_element_by_class_name("select2_demo_1")
opciones = elemento.find_elements_by_tag_name("option")
for option in opciones:  
    option.click()  
    print(option)

seleccionar = Select(driver.find_element_by_class_name('select2_demo_1'))
seleccionar.select_by_value("3")
seleccion = seleccionar.first_selected_option
print(seleccion.get_attribute("data-select2-id"))
#try:
#    element = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.ID, "select2-cpvw-container"))
#    )
#except Exception as e:
#    print(e.msg,"hubo error")
#movimiento1 = driver.find_element_by_id("select2-cpvw-container")
#movimiento2 = driver.find_element_by_id("select2-cpvw-result-sy29-3")
#movimiento = action_chains(driver)

#movimiento.move_to_element(movimiento1).move_to_element(movimiento2).click().perform()


