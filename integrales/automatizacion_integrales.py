from selenium import webdriver
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains


driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver.exe")
driver.get("http://eidykos.com/Eidypymes/login.jsp#nav215")

nombre_usuario = "JBOLIVAR"
clave_usuario = "123456789"
fecha_ingreso = "08-01-2021"
# fonseca -> "FON001" , sanjuan -> "SNJ001", maicao-> "MAI001"
sede = "FON001"
costo_terapias = "12222"
#archivo a donde iran los que no estan liquidados
file_no_liquidados = 'doc_integrales/sin_liquidar.txt'

paciente_sin_liquidar = False
#fecha de hoy
hoy = datetime.now()
dia = hoy.day
mes = hoy.month
año = str(hoy.year)

if mes >= 1 or mes <= 9:
    
    mes = "0"+ str(mes)
    
if dia >= 1 or dia <= 9:
    
    dia = "0"+ str(dia)

fecha_parseada = dia + "-" + mes + "-" + año
#ingresando usuario
usuario = driver.find_element_by_id("usuario")
usuario.send_keys(nombre_usuario) 

#ingresando password
clave = driver.find_element_by_id("password")
clave.send_keys(clave_usuario)
clave.send_keys(Keys.ENTER)
time.sleep(2)
driver.get("http://eidykos.com/Eidypymes/index.jsp#nav1")

def sin_liquidar(paciente):
    with open('doc_integrales/sin_liquidar.txt','a') as file:
        file.write(paciente)
        file.close()

def borrar(filein, linea_a_buscar=None):
    
    try:
        fin = open(filein, "r")
        usuarios = fin.readlines()
        fin.close()
        if linea_a_buscar == None:
            usuarios.pop(0)
        else:
            usuarios.remove(linea_a_buscar)
        
        fout=open(filein, 'w')
        fout.writelines(usuarios)
        fout.close()
    except IndexError:
        print('no hay mas datos')

with open('doc_integrales/realcion_integrales_enero_2021.txt') as file:
    for i, line in enumerate(file):
        integral = (line)
        separador = ","
        dividir = integral.split(separador)
        try:
            got_data =dividir[1]
            nombre = dividir[0]
            cedula = dividir[1]
            diagnostico = dividir[2]
            nua = dividir[3]
            paciente = nombre +","+ cedula +","+ diagnostico +","+ nua +","+ "\n"
        except IndexError:
            got_data = ""

        print(nombre)
        print(cedula)
        print(diagnostico)
        print(nua)
        
        
        #esperando a que cargue datos del comprobante
        try:
            element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//form[@id="frm_nuevo"]/div/div/div/span/span/span/span[2]')))
        except:
            print("error: sperando a que cargue datos del comprobante")
        time.sleep(5)
        
        #select de FACTURA POR EVENTO
        seleccionar = Select(driver.find_element_by_id('cod_documento'))
        seleccionar.select_by_value("1")
        seleccion = seleccionar.first_selected_option
        
        #fecha de hoy en el date picker
        elemento = driver.find_element_by_xpath('//*[@id="fec_comprobante"]')
        elemento.clear()
        elemento.send_keys(fecha_parseada)
        elemento.send_keys(Keys.TAB)  
        
        #originar de
        elemento = driver.find_element_by_xpath('//*[@id="contenedor_principal"]/div[2]/div[2]/div/div/div[1]/div/div/button')
        movimiento = ActionChains(driver).click(elemento).perform()
        
        elemento = driver.find_element_by_xpath('//*[@id="contenedor_principal"]/div[2]/div[2]/div/div/div[1]/div/div/ul/li[2]/a')
        movimiento = ActionChains(driver).click(elemento).perform()
        
        try:
            
            element = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="btn_guardar_admisiones"]')))
        except:
            print("error")
        #time.sleep(3)
        
        #buscar por CEDULA
        elemento = driver.find_element_by_xpath('//*[@id="id_paciente"]')
        elemento.send_keys(cedula)
        elemento.send_keys(Keys.ENTER)
        
        #esperando a que carguen los resultados en la admicion
        try:
            while not driver.find_element_by_xpath('//*[@id="div_sel_factura"]').is_displayed():
                None
                #element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="div_sel_factura"]')))
        except:
            print("error esperando a que carguen los resultados en la admicion")
        #time.sleep(20)
        
        ##select de cuenta medica
        
        select = driver.find_element_by_xpath('//*[@id="sel_factura"]')   
        elementos_select = select.find_elements_by_tag_name('option') 
        numeros_servicios = None
        alerta_sin_liquidar = driver.find_element_by_xpath('//*[@id="div_mensaje_admisiones"]')
        
        if len(elementos_select) == 0 or (alerta_sin_liquidar.is_displayed()):
            
            sin_liquidar(paciente)
            #borrar(file_no_liquidados,paciente)
            select.send_keys(Keys.ESCAPE)            
            print('no hay elemetos en select')
            continue
        
        for opcion in elementos_select:
            print('entro al for')            
            alerta_sin_liquidar_x_id = driver.find_element_by_xpath('//*[@id="div_mensaje_admisiones"]')
            if opcion.get_attribute("data-cant_servicios") == "45" and opcion.get_attribute("data-fec_ingreso") == fecha_ingreso:
                numeros_servicios = opcion
                paciente_sin_liquidar = False
                break
                                       
            #si no esta el servicio, quiere decir que no se ha facturado                 
            print('si no esta el servicio, quiere decir que no se ha facturado')
            paciente_sin_liquidar = True           
        
        if paciente_sin_liquidar :
            sin_liquidar(paciente)
            print('por aca')
            select.send_keys(Keys.ESCAPE)
            continue
          
        print(numeros_servicios.get_property("value"))
        

        seleccionar = Select(select)
        seleccionar.select_by_value(numeros_servicios.get_property("value"))
        seleccion = seleccionar.first_selected_option
        
        #guardando lo que se selecciono
        guardar = driver.find_element_by_xpath('//*[@id="btn_guardar_admisiones"]')
        while not guardar.is_enabled():
            None
            
        movimiento = ActionChains(driver).click(guardar).perform()
        
        #select centro de costo
        select = driver.find_element_by_xpath('//*[@id="cod_centro_costo"]')
        seleccionar = Select(select)
        seleccionar.select_by_value(sede)
        seleccion = seleccionar.first_selected_option

        #nro.autorizacion
        elemento = driver.find_element_by_xpath('//*[@id="camp_adicional_12"]')
        elemento.send_keys(nua)
        
        #detalles
        elemento = driver.find_element_by_xpath('//*[@id="tbl_comprobantes_detalles"]/tbody')
        opciones_de_detalles = elemento.find_elements_by_tag_name('tr')
        cont = 1
        for opciones in opciones_de_detalles:
            cont+=1
            elemento = opciones.find_element_by_xpath('//*[@id="tbl_comprobantes_detalles"]/tbody/tr[1]/td[1]/i[2]')
            driver.execute_script("btn_abrir_modal(this,"+ str(cont) +");")
            time.sleep(3)
            #borrando comas
            elemento = driver.find_elements_by_id('camp_adicional_19')                  
            elemento[0].clear()      
              
               
            #guardar 
            elemento = opciones.find_element_by_xpath('//*[@id="modalCampos"]/div/div/div[3]/button[2]')
            movimiento = ActionChains(driver).click(elemento).perform()
        
            # #agregando valor de las terapias
            elemento = opciones.find_element_by_id("precio_"+str(cont))
            elemento.clear()
            elemento.send_keys(costo_terapias)
            
        #guardando_borrador
        guardar = driver.find_element_by_id('btn_guardar')
        movimiento = ActionChains(driver).click(guardar).perform()
        
        #crear otro comprobante
        try:            
            while not driver.find_element_by_xpath('//*[@id="frm_nuevo"]').is_displayed():
                print('...')
                element = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="frm_nuevo"]')))
        except:
            print("error: crear otro comprobante")
        time.sleep(5)

        
        otro_comprobante = driver.find_element_by_xpath('/html/body/div[6]/div[7]/div/button')
        print(elemento)
        ActionChains(driver).click(otro_comprobante).perform()
        
            
            
        
        print("se habilito")
        
        
        
              
        
        
        
         
    

