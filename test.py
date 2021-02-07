from os import write


def sin_liquidar(paciente):
    with open('doc_integrales/sin_liquidar.txt','a') as file:
        file.write(paciente)
        file.close()

def deleteline(filein):
    
    try:
        fin = open(filein, "r")
        usuarios = fin.readlines()
        fin.close()
        
        usuarios.pop(0)
        
        fout=open(filein, 'w')
        fout.writelines(usuarios)
        fout.close()
    except IndexError:
        print('no hay mas datos')
    
#deleteline('doc_integrales/datos.txt')
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
        
a ="hola mundo"
b="hola mundo"

if a != b :
    print('entro')

