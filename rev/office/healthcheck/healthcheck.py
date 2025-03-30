#!/usr/bin/env python3
from pwn import *
from z3 import *

p = None

# bits used on the event selector to determine events
tps_bits = [1, 3] 
meet_bits = [1, 2, 4]
jam_bits = [3, 4]
sat_bits = [3, 5]
fire_bits = [3, 5, 7]
stapler_bits = [5, 6]
quit_bits = [0]

# this value is initialized to a random value that we want to find
# assume for now that all the bits are 0
event_selector = 0;

# z3 bitvecs for the bits in the random byte
R = [BitVec('r%s' % i, 1) for i in range(8)]
s = Solver()

# return event_selector as a list of bits corresponding with z3 bitvecs
def es_bits():
    global event_selector
    es = []
    for i in range(8):
        es.append((event_selector >> (i)) & 1)
    return es

# change the daily pay rate to r, must be less than current rate
def set_rate(r):
    global p
    p.recvuntil(b'>')
    p.sendline(b'2')
    p.recvuntil(b'>')
    p.sendline(str(r).encode("utf-8"))

# select the work option n times
# updates event_selector, balance, and adds constraints based on events.
def work(n):
    global balance
    global event_selector
    global p
    global R
    global s
    for _ in range(n):
        esb = es_bits()
        p.recvuntil(b'> ')
        p.sendline(b'1')
        events = p.recvuntil(b'today')
        # invert the event_selector bit because we assumed the event_selector started at 0
        # real_es = solve_es ^ randomized_val 
        #   -> randomized_val = real_es(observed events) ^ solve_es
        # a bit set in this solve event_selector implies that randomized bit != solve bit
        if b"TPS" in events:
            b0 = tps_bits[0]
            b1 = tps_bits[1]
            s.add(Or(R[b0] == 1-esb[b0], R[b1] == 1-esb[b1]))
        if b"meeting" in events:
            b0 = meet_bits[0]
            b1 = meet_bits[1]
            b2 = meet_bits[2]
            s.add(Or(Or(R[b0] == 1-esb[b0], R[b1] == 1-esb[b1]), R[b2] == 1-esb[b2]))
        if b"jams" in events:
            b0 = jam_bits[0]
            b1 = jam_bits[1]
            s.add(Or(R[b0] == 1-esb[b0], R[b1] == 1-esb[b1]))
        if b"Saturday" in events:
            b0 = sat_bits[0]
            b1 = sat_bits[1]
            s.add(Or(R[b0] == 1-esb[b0], R[b1] == 1-esb[b1]))
        if b"fire" in events:
            b0 = fire_bits[0]
            b1 = fire_bits[1]
            b2 = fire_bits[2]
            s.add(Or(Or(R[b0] == 1-esb[b0], R[b1] == 1-esb[b1]), R[b2] == 1-esb[b2]))
        if b"stapler" in events:
            b0 = stapler_bits[0]
            b1 = stapler_bits[1]
            s.add(Or(R[b0] == 1-esb[b0], R[b1] == 1-esb[b1]))
        if b"quitting" in events:
            b0 = quit_bits[0]
            s.add(R[b0] == 1-esb[b0])
        p.recvuntil(b'Balance: $')
        balance_str = p.recvline()
        balance = int(balance_str.decode('utf-8'))
        event_selector = event_selector ^ (balance &0xff)

def solve():
    global p
    global balance
    global R
    global s
    global event_selector

    event_selector = 0

    # z3 bitvecs for the bits in the random byte
    R = [BitVec('r%s' % i, 1) for i in range(8)]
    s = Solver()

    p = remote("127.0.0.1", 1337)
    #p = process('../challenge/chal')

    p.recvuntil(b'Balance: $')
    balance_str = p.recvline()
    balance = int(balance_str.decode('utf-8'))
    set_rate(0x6d) # this will generate varied bit patterns and hopefully good constraints

    # do work 20 times to generate enough constraints that we get the right solution.
    work(20)

    # get the randomized value from z3 as a number
    s.check()
    solution = 0
    for i, r in enumerate(R):
        solution = solution | (s.model().evaluate(r).as_long() << i)

    # use the random value to compute the balance needed for the flag
    solve_balance = solution | (solution << 8)
    # set the rate to reach the required balance after working
    set_rate(solve_balance - balance)
    work(1)

    # select quit and check for flag
    p.recvuntil(b'> ')
    p.sendline(b'3')
    res = str(p.recvall().decode('ascii'))
    if 'wctf{' in res:
        print(res)
        return 0
    else:
        return 1


def main():
    for i in range(12):
        if solve() == 0:
            exit(0)
    exit(1)


if __name__ == "__main__":
    main()
