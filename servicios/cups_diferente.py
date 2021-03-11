#cups es diferente
if (valor != cupus):
                cups_diferente = True
                elemento_siguiente = cont+1
                driver.execute_script("btn_productos_agregar();")    
                print('es diferente el CUPS')                
                
                #ingresando el cups a buscar
                elemento = driver.find_element_by_xpath('//*[@id="div_cod_producto_'+str(elemento_siguiente)+'_sel"]/span[2]/span[1]/span')
            
                #item creado
                while not elemento.is_displayed():
                    print('aun no esta listo')
                    None
                    
                #hacer click para buscar    
                elemento = driver.find_element_by_xpath('//*[@id="div_cod_producto_'+str(elemento_siguiente)+'_sel"]/span[2]/span[1]/span')
                print(elemento)
                movimiento = ActionChains(driver).click(elemento).perform()
                
                elemento = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
                elemento.send_keys(cups)
                
                
                #ul donde se cargan los li
                ul_lista = driver.find_element_by_xpath('//*[@id="select2-cod_producto_'+str(elemento_siguiente)+'-results"]')
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
                    driver.get("http://eidykos.com/Eidypymes/index.jsp#nav1")
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
                
                driver.execute_script("btn_abrir_modal(this,"+ str(elemento_siguiente) +");")
                time.sleep(3)
                
                #borrando comas
                elemento = driver.find_elements_by_id('camp_adicional_19')                  
                elemento[0].clear()   
                
                #diagnostico
                elemento = driver.find_element_by_id('camp_adicional_21') 
                if len(elemento.text)==0:
                    elemento.send_keys(diagnostico)                
                
                #guardar 
                elemento = opciones.find_element_by_xpath('//*[@id="modalCampos"]/div/div/div[3]/button[2]')
                movimiento = ActionChains(driver).click(elemento).perform()
            
                # #agregando valor de las terapias
                elemento = driver.find_element_by_id("precio_"+str(elemento_siguiente))            
                elemento.clear()
                elemento.send_keys(costo_terapias)
