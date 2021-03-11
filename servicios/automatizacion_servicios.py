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
driver.get("http://62.171.155.205/Eidypymes/login.jsp")

nombre_usuario = "JBOLIVAR"
clave_usuario = "123456789"
fecha_ingreso = "29-12-2020"

# fonseca -> "FON001" , sanjuan -> "SNJ001", maicao-> "MAI001"
sede = "FON001"
# costo_terapias = "30000"
#archivo a donde iran los que no estan liquidados
file_no_liquidados = 'servicios/doc_servicios/sin_liquidar.txt'
sin_resultados_cups = False

paciente_sin_liquidar = False
#fecha de hoy
hoy = datetime.now()
hoy = hoy.strftime('%d-%m-%Y')
#ingresando usuario
usuario = driver.find_element_by_id("usuario")
usuario.send_keys(nombre_usuario) 

#ingresando password
clave = driver.find_element_by_id("password")
clave.send_keys(clave_usuario)
clave.send_keys(Keys.ENTER)
time.sleep(2)


def sin_liquidar(paciente):
    with open('servicios/doc_servicios/sin_liquidar.txt','a') as file:
        file.write(paciente)
        file.close()

def buscar_cups_y_valor(cups):
    with open('servicios/doc_servicios/cups.txt') as file:
        for i, line in enumerate(file):
            integral = (line.replace("\n",""))
            separador = "="
            servicios = integral.split(separador)

            if(str(servicios[0]) == str(cups)):
                # cups = [servicios[0] , servicios[1]]
                return servicios

def cups_sistema_esta_servicios(cups_sistema,cups_servicios:list):
    for item in cups_servicios:
        print('::::',cups_servicios,type(item),type(cups_servicios),type(item),item,cups_sistema,type(cups_sistema))
        if int(cups_sistema) == int(item):
            print('entro')
            return True
    return False
            
        


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



driver.get("http://62.171.155.205/Eidypymes/index.jsp#nav1")
driver.get("http://62.171.155.205/Eidypymes/index.jsp#nav1")

with open('servicios/doc_servicios/servicios.txt') as file:
    for i, line in enumerate(file):
        integral = (line.replace('\n',""))
        separador = ","
        dividir = integral.split(separador)
        try:
            got_data =dividir[1]
            cedula = dividir[0]
            nombre = dividir[1] + dividir[2]
            fecha_atencion = dividir[3]
            nua = dividir[4]
            cod_admision = "118382"
            diagnostico = dividir[5]
            cups = dividir[6].split('-')
            cantidad = dividir[7].split('-')
            suma = 0
            for item in cantidad:
                suma += int(item)
            cantidad = suma
            cantidad_servicios = len(cups)
      
            paciente = cedula +","+ dividir[1] +","+ dividir[2] +","+ dividir[3] +","+ dividir[4] +","+fecha_atencion +","+ nua +","+ diagnostico+"\n"
        except IndexError:
            got_data = ""

        print(nombre)
        print(cedula)
        print(fecha_atencion)
        print(nua)
        print(diagnostico)
        print(cups)
        print(paciente)        
        
        
        #esperando a que cargue datos del comprobante
        try:
            element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//form[@id="frm_nuevo"]/div/div/div/span/span/span/span[2]')))
        except:
            print("error: sperando a que cargue datos del comprobante")
        time.sleep(4)
        
        #select de FACTURA POR EVENTO
        seleccionar = Select(driver.find_element_by_id('cod_documento'))
        seleccionar.select_by_value("1")
        seleccion = seleccionar.first_selected_option
        
        #fecha de hoy en el date picker
        elemento = driver.find_element_by_xpath('//*[@id="fec_comprobante"]')
        elemento.clear()
        elemento.send_keys(hoy)
        
        elemento.send_keys(Keys.TAB)  
        
        #originar de
        elemento = driver.find_element_by_xpath('//*[@id="contenedor_principal"]/div[2]/div[2]/div/div/div[1]/div/div/button')
        movimiento = ActionChains(driver).move_to_element(elemento).perform()
        movimiento = ActionChains(driver).click(elemento).perform()
        
        elemento = driver.find_element_by_xpath('//*[@id="contenedor_principal"]/div[2]/div[2]/div/div/div[1]/div/div/ul/li[2]/a')
        movimiento = ActionChains(driver).move_to_element(elemento).perform()
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

            alerta_sin_liquidar_x_id = driver.find_element_by_xpath('//*[@id="div_mensaje_admisiones"]')
            if opcion.get_attribute("data-cant_servicios") == str(cantidad) and opcion.get_attribute("data-fec_ingreso") == fecha_atencion and opcion.text == cod_admision:
                numeros_servicios = opcion
                print('si esta el servicio')
                paciente_sin_liquidar = False
                break                                       
            #si no esta el servicio, quiere decir que no se ha facturado
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

        time.sleep(1)
        #nro.autorizacion
        elemento = driver.find_element_by_xpath('//*[@id="camp_adicional_12"]')
        
        ActionChains(driver).move_to_element(elemento).perform()
        elemento.clear()

        ActionChains(driver).move_to_element(elemento).send_keys(nua).perform()
        elemento.send_keys(nua)
         
        
        #detalles
        elemento = driver.find_element_by_xpath('//*[@id="tbl_comprobantes_detalles"]/tbody')
        opciones_de_detalles = elemento.find_elements_by_tag_name('tr')
        cont = 1
        cont2 = 0
        cont3 = 0 
        ultimo = 0
        
        flag = False
        cups_estan = []
        cups_no_estan = []
        objetos_a_borrar = []
        posicion_objetos_borrar = []
        #llenando la  lista de los cups que estan en el sistema y en el servicio
        for item in opciones_de_detalles:
            cont+=1
            #verificando si el cups del paciente es el mismo que el del sistema
            elemento = driver.find_element_by_xpath('//*[@id="codigo_'+ str(cont) +'"]')
            valor = elemento.get_attribute('value').replace(" ","")
            valor = int(valor)
            print(type(valor),'<----cups sistema')
            print(type(cups),'tipo cups dato')
            # cupus = int(cups)
            cups_diferente = False
            print(len(opciones_de_detalles),'opciones de detalle')

            if cups_sistema_esta_servicios(valor, cups):
                cups_estan.append(int(valor))
        #separando los que no estan en el servicio pero si en el sistema
        for item in cups:
            print(item, type(item))
            if not int(item) in cups_estan:
                cups_no_estan.append(item)

        cont = 2
        for opciones in opciones_de_detalles:
            #verificando si el cups del paciente es el mismo que el del sistema
            elemento = driver.find_element_by_xpath('//*[@id="codigo_'+ str(cont) +'"]')
            valor = elemento.get_attribute('value').replace(" ","")
            valor = int(valor)
            # cupus = int(cups)
            cups_diferente = False
            
            #cups es diferente
            
            if not flag:
                ultimo = len(opciones_de_detalles) + 2

            if not cups_sistema_esta_servicios(valor, cups):
                #colocando el objeto web element a borrar dentro de una lista
                objetos_a_borrar.append(opciones)
                pocicion = cont - 1
                posicion_objetos_borrar.append(pocicion)
                cups_diferente=True
                
                
          
            # if cups_diferente:
            #     eliminar = opciones.find_element_by_xpath('//*[@id="tbl_comprobantes_detalles"]/tbody/tr[1]/td[1]/i[3]')    
            #     movimiento = ActionChains(driver).click(eliminar).perform()              
            
            if not cups_diferente:
                
                driver.execute_script("btn_abrir_modal(this,"+ str(cont) +");")
                time.sleep(3)
                
                #borrando nua
                elemento = driver.find_elements_by_id('camp_adicional_19')                  
                elemento[0].clear()      
                
                #diagnostico
                elemento = driver.find_element_by_id('camp_adicional_21') 
                texto_elemento = driver.find_element_by_xpath('//*[@id="det_camp_adicional_'+str(cont)+'_21"]').get_attribute('value')
                print('dentro de diagnostico: ',texto_elemento, len(texto_elemento),type(texto_elemento))
                if len(texto_elemento)==0:
                    elemento.send_keys(diagnostico)
                
                #guardar 
                elemento = opciones.find_element_by_xpath('//*[@id="modalCampos"]/div/div/div[3]/button[2]')
                movimiento = ActionChains(driver).click(elemento).perform()
            
                # #agregando valor de las terapias
                
                elemento = opciones.find_element_by_id("precio_"+str(cont))
                elemento.clear()
                valor_cups = None
                print(cups_sistema_esta_servicios(valor, cups),"--",buscar_cups_y_valor(valor))
                if cups_sistema_esta_servicios(valor, cups) and buscar_cups_y_valor(valor)!=None:
                        valor_cups = buscar_cups_y_valor(valor)
                        print('entro **')                        
                else:
                    print('no esta', cups_sistema_esta_servicios(valor, cups))
                
                print(valor_cups)
                elemento.send_keys(valor_cups[1])
                
            cont+=1
            cont2+=1
        
        #borrando los objetos que no estan
        for item in objetos_a_borrar:
            # print(cups,buscar_cups_y_valor(cups[cont2]),cups[cont2],cups_sistema_esta_servicios(valor, cups),valor,'::::::')
            cups_diferente = True
            
            driver.execute_script("btn_productos_agregar();")    
            print('es diferente el CUPS')                
            
            #ingresando el cups a buscar
            elemento = driver.find_element_by_xpath('//*[@id="div_cod_producto_'+str(ultimo)+'_sel"]/span[2]/span[1]/span')
        
            #item creado
            while not elemento.is_displayed():
                print('aun no esta listo')
                None
                
            #hacer click para buscar    
            elemento = driver.find_element_by_xpath('//*[@id="div_cod_producto_'+str(ultimo)+'_sel"]/span[2]/span[1]/span')
            print(elemento,"<---elemento")
            movimiento = ActionChains(driver).click(elemento).perform()
            
            elemento = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
            print(cups,"-",ultimo,'<-------')
            elemento.send_keys(cups_no_estan[cont3])
            
            
            #ul donde se cargan los li
            ul_lista = driver.find_element_by_xpath('//*[@id="select2-cod_producto_'+str(ultimo)+'-results"]')
            li_elementos_del_ul = ul_lista.find_elements_by_tag_name("li")
            print('antes')
            time.sleep(2)
            #esperar a que cargue el cups
            # try:
            
            
            while ul_lista.find_element_by_tag_name("li").get_attribute('class') == "select2-results__option" or ul_lista.find_element_by_tag_name("li").get_attribute('class') == "select2-results__option loading-results":
                print('repitiendose', ul_lista.find_element_by_tag_name("li").get_attribute('class'))
                time.sleep(2)
                
                if (ul_lista.find_element_by_tag_name("li").text == "No se encontraron resultados"):
                    sin_liquidar('NO SE ENCONTRO CODIGO CUPS: '+paciente)
                    print('no hay redultados del cups')
                    sin_resultados_cups = True
                    break
                
                sin_resultados_cups=False 
            
            print(sin_resultados_cups)
            
            if sin_resultados_cups:
                print('aqui')
                driver.get("http://62.171.155.205/Eidypymes/index.jsp#nav1")
                time.sleep(3)
                break                     
                                                
            # except Exception:
            #     print('no hay redultados del cups')
            #     # sin_liquidar('NO SE ENCONTRO CODIGO CUPS'+paciente)
            #     continue
            elemento.send_keys(Keys.ENTER)
            
            nua_cero = driver.find_element_by_xpath('//*[@id="camp_adicional_9"]')
            nua_cero.clear()
            nua_cero.send_keys("0")
            
            driver.execute_script("btn_abrir_modal(this,"+ str(ultimo) +");")
            time.sleep(3)
            
            #borrando comas
            elemento = driver.find_elements_by_id('camp_adicional_19')                  
            elemento[0].clear()   
            
            #diagnostico
            elemento = driver.find_element_by_id('camp_adicional_21') 
            if len(elemento.text)==0:
                elemento.send_keys(diagnostico)                
            
            #guardar 
            elemento = item.find_element_by_xpath('//*[@id="modalCampos"]/div/div/div[3]/button[2]')
            movimiento = ActionChains(driver).click(elemento).perform()
        
            # #agregando valor de las terapias
            elemento = driver.find_element_by_id("precio_"+str(ultimo))            
            elemento.clear()
            valor_cups = buscar_cups_y_valor(cups_no_estan[cont3])[1]
            print(valor_cups, '<-VALOR CUP')
            elemento.send_keys(valor_cups)
            ultimo += 1
            cont3+=1
            flag=True
        
        cont = 2
        for item in opciones_de_detalles:
            #verificando si el cups del paciente es el mismo que el del sistema
            elemento = driver.find_element_by_xpath('//*[@id="codigo_'+ str(cont) +'"]')
            valor = elemento.get_attribute('value').replace(" ","")

            if not cups_sistema_esta_servicios(valor, cups):
                #eliminando dinamicamenta los servicios que no estan 
                eliminar = item.find_element_by_tag_name('td').find_elements_by_tag_name('i') 
                movimiento = ActionChains(driver).click(eliminar[2]).perform()
                
            cont+=1
            
            
        print("se habilito")  
        print (posicion_objetos_borrar,"<--",cont,"--",cont2,"--",cont3,"--",ultimo,"--",flag,"--",cups_estan,"--",cups_no_estan,"--",objetos_a_borrar)
        