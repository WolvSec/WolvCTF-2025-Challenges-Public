
#!/usr/bin/python3.10
# This file is modified from TAMUctf constraintgen
# https://github.com/tamuctf/TAMUctf-2021/blob/master/reversing/dubious/constraintgen/main.py
from random import getrandbits, sample, choice
from binascii import b2a_hex

from z3 import *
from typing import Union, Dict

from Crypto.Cipher import AES


def prove(solver: Solver, stmt: Union[BoolRef, bool]):
    res = solver.check(Not(stmt))
    return res.r == -1


def generate_relatives(pw: Dict[BitVecRef, BitVecVal]) -> [BoolRef]:
    avail = list(pw.keys())
    rels = []
    used = {}
    for elem in pw.keys():
        used[elem] = 0
    while not all(used[elem] > 2 for elem in pw.keys()):
        rel = sample(avail, 2)
        if all(used[elem] > 2 for elem in rel):  # remove too many redundants
            continue
        used[rel[0]] += 1
        used[rel[1]] += 1
        r = choice([0, 1])
        if r == 0:
            if pw[rel[0]].as_long() > pw[rel[1]].as_long():
                rels.append(rel[0] == rel[1] + simplify(pw.get(rel[0]) - pw.get(rel[1])))
            else:
                rels.append(rel[0] == rel[1] - simplify(pw.get(rel[1]) - pw.get(rel[0])))
        if r == 1:
            rels.append(rel[0] == (rel[1] ^ simplify(pw.get(rel[0]) ^ pw.get(rel[1]))))

    return rels


def squeeze(solver: Solver, pw: Dict[BitVecRef, BitVecVal]) -> int:
    avail = list(pw.keys())
    count = 0
    while not prove(solver, And([sym == val for sym, val in pw.items()])):
        count += 1
        pick = choice(avail)
        avail.remove(pick)
        solver.add(pick == pw.get(pick))

    return count


def generate(password: str):
    ctx = Context()
    solver = Solver(ctx=ctx)
    bvsort = BitVecSort(8, ctx)
    pw = {}
    for i, c in enumerate(password):
        pw[BitVec(f"pw[{str(i)}]", bvsort, ctx)] = BitVecVal(ord(c), bvsort, ctx)
    rels = generate_relatives(pw)
    solver.add(rels)
    squeezes = squeeze(solver, pw)
    template = "//<constraints>//"
    constraints = ''
    for i, assertion in enumerate(solver.assertions()):
        print(assertion)
        constraints += f"        pass&=({assertion});\n".replace(" == ", " == (").replace(");", "));")
    template = template.replace("//<constraints>//", constraints)


if __name__ == '__main__':
    #extra = b2a_hex(bytearray(getrandbits(8) for _ in range(15))).decode('ascii')
    flag = r"wctf{1_h0p3_y0u_u53d_ANGR_f0r_th15_0r_y0U_w0uLd_b3_a_duMMy}"
    generate(flag)

