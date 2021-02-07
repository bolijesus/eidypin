#hacer click para buscar    
            elemento = driver.find_element_by_xpath('//*[@id="div_cod_producto_'+str(cont)+'_sel"]/span[2]/span[1]/span/span[2]')
            
            elemento.click()
            
            #ingresando el cups a buscar
            elemento = driver.find_element_by_xpath('/html/body/span')
           
            
            while not elemento.is_displayed():
                None
            
            elemento = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
            elemento.send_keys(cups)
            
            
            #ul donde se cargan los li
            ul_lista = driver.find_element_by_xpath('//*[@id="select2-cod_producto_'+str(cont)+'-results"]')
            li_elementos_del_ul = ul_lista.find_elements_by_tag_name("li")
            print('antes')
            
            #esperar a que cargue el cups
            try:
                while ul_lista.find_element_by_tag_name("li").get_attribute('class') == "select2-results__option" or ul_lista.find_element_by_tag_name("li").get_attribute('class') == "select2-results__option loading-results":
                    ul_lista.find_element_by_tag_name("li").get_attribute('class')
            except Exception:
                print('no hay redultados del cups')
            elemento.send_keys(Keys.ENTER)