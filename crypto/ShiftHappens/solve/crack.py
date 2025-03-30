#!/usr/bin/sage -python

from sage.all import *

# length of known ciphertext
l = 16
# plaintext must be 2l bits, where l is the length of the 
# key bits obtained by bitwise XORing the known plaintext with the ciphertext

#obetained from gen_keybits file
kbits = [0,0,0,0,1,1,0,0,1,0,1,0,0,1,1,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,1,0] # this is the initial state

# create the U matrix
ulist = []
for i in range(l):
    state = kbits[i:l+i]
    ulist.append(state)

U = matrix(GF(2), ulist)
print(f"Determinant of U: {det(U)}")

# generate inverse of U
W = U.inverse()

# generate V matrix
vlist = []
for i in range(1,l+1):
    state = kbits[i:l+i]
    vlist.append(state)

V = matrix(GF(2), vlist)

#Generate S matrix
S = V*W
print(S[-1])
# last row of s is the FEEDBACK

# now I know the initial state and also I know the feedback
state = 0b0000110010100110  #1100111111010010 next 
print("init State: ",state)
feedback = 0
for i in range(16):
    feedback += int(S[-1][i])*(2**(15-i))
print("Feedback: ",bin(feedback))

# generate the bitstream for the XOR
def next(current_state,feedback):
    bit = 0
    for i in range(16):
        bit = bit ^ ( ((current_state >> i) & 1) & ((feedback >> i) & 1 ) )
    new_state = (current_state << 1) | (bit)
    return new_state;

bitstream = []
for i in range(60*8):
    bit = (state >> 15) & 1;
    bitstream.append(bit)
    state = next(state,feedback)

# now that the bitstream has been generated
# we can xor the ciphertext with the bitstream
f = open("ciphertext.txt","r")
lines = f.readlines()
for i in range(60):
    line = lines[i]
    num = int(line,2)
    new = []
    for j in range(8):
        to_print = (num >> (7-j)) & 1
        to_print = to_print ^ bitstream[i*8 + j]
        new.append(to_print)
    print(chr(int(''.join(map(str, new)),2)),end='')
print()

