

def config():
    valores = []
    
    with open('consultas/configuraciones.txt') as file:
        for i, line in enumerate(file):
            configuracion = (line.replace("\n",""))
            separador = "="
            servicios = configuracion.split(separador)[1]
            valores.append(servicios)
    
    return valores
