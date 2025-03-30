#!/usr/bin/env python3
from time import sleep
from pwn import *

def main():
    r = remote("127.0.0.1", 1337)
    r.sendline(b'0105001083000b')
    
    sleep(1)
    out = r.recv(1024)
    print(out)

    if (b'wctf' in out):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
