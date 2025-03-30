#! /usr/bin/env python3
from pwn import *

# Block length is 16 bytes
AES_BLOCK_LEN = 16

flag = ''

known_blocks = []
incomplete_block = b''
padding = b'A'*(AES_BLOCK_LEN-1)

io = remote("127.0.0.1", 1337)
#io = process(['python3','chall.py'])
flag = b''
# 0x21 - 0x7E is the range of printable characters
while True:
    #guess one byte
    found = False
    for byte in range(0x21,0x7e):

        io.sendline(b'Y')
        
        #craft guess
        # padding + known_blocks(N*16 bytes) + incomplete_block + byte + padding + incomplete_block 
        # padding + incomplete_block + byte (16 bytes)
        guess = padding
        for block in known_blocks:
            guess += block
        guess += incomplete_block
        guess += byte.to_bytes(1,'little')
        guess += padding

        io.sendline(guess)

        io.recvuntil(b'message is: ')
        recieved = io.recvline()[1:-1]
        
        split_blocks = [recieved[x:x+AES_BLOCK_LEN].decode() for x in range(0,len(recieved),AES_BLOCK_LEN)]
        
        comp1 = 2*len(known_blocks)
        comp2 = 4*len(known_blocks) + 2
        
        if split_blocks[comp1] == split_blocks[comp2]:
            log.success(f'FOUND BYTE: {chr(byte)}')
            found = True
            flag += byte.to_bytes(1,'little')
            print(flag)
            if(len(flag) == 90):
                exit(0)
            incomplete_block += byte.to_bytes(1,'little')
            padding = b'A'*(len(padding)-1)
            if len(incomplete_block) == AES_BLOCK_LEN:
                known_blocks.append(incomplete_block)
                incomplete_block = b''
                padding = b'A'*(AES_BLOCK_LEN-1)
                
            break
    if not found:
        exit(1)
            



