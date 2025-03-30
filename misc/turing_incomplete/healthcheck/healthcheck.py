#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 1337))
vals = b"RB0 RB1 R11 R21 R31 R41 R51 R61 R71 R81 L00 LB0 H00 H00 H00 H00 L10 L20 L30 L40 L50 L60 L70 L80 L90 RA1 L10 RB1 H00 H00 H00 H00\n"

sock.send(vals)
time.sleep(0.1)

result = sock.recv(1024)
print(result)
if(b"wctf" in result):
    exit(0)
exit(1)

