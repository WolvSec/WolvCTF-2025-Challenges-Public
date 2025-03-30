import re
#from z3 import *
import random

password = "011101010110111001001100001100000110001101001011"

index_regex = r"([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]"
parse_gates_regex = r"(\w+)\s+(_\d+_)\s*\(\s*\.A\s*\(\s*([^)]+)\s*\)\s*,\s*\.B\s*\(\s*([^)]+)\s*\)\s*,\s*\.Y\s*\(\s*([^)]+)\s*\)\s*\)"

def formatGate(gate):
    gateFmtString = f"""
{gate[0]} {gate[1]} (
    .A({gate[2]}),
    .B({gate[3]}),
    .Y({gate[4]})
);"""
    return gateFmtString

def inv(gate):
    if gate == "XOR":
        return "XNOR"
    elif gate == "XNOR":
        return "XOR"
    elif gate == "AND":
        return "NAND"
    elif gate == "NAND":
        return "AND"
    elif gate == "OR":
        return "NOR"
    elif gate == "NOR":
        return "OR"
    elif gate == "NOT":
        return "BUF"
    elif gate == "BUF":
        return "NOT"
    else:
        print(f"Invalid gate type: {gate}")

with open("chall/synth.v","r") as f:
    file_contents = f.read()

gates = re.findall(parse_gates_regex,file_contents)

usedIndices = set()
lockGates = []
newGates = {}
newWires = []

for i in range(len(password)-1, -1, -1):
    print(password[i], end="")
    actIndex = len(password) - i - 1
    if password[i] == "0":
        a =  random.randint(0,len(gates))
        while(a in usedIndices):
            a = random.randint(0,len(gates))
        usedIndices.add(a)
        locked = (gates[a][0], gates[a][1], gates[a][2], gates[a][3], f"_l{actIndex}_")
        lock = ("XOR", f"_lock{actIndex}_", f"_l{actIndex}_", f"password[{actIndex}]", gates[a][-1])
        newWires.append(f"_l{actIndex}_")
        newGates[a] = locked
        lockGates.append(lock)
    else:
        a =  random.randint(0,len(gates))
        while(a in usedIndices):
            a = random.randint(0,len(gates))
        usedIndices.add(a)
        locked = (inv(gates[a][0]), gates[a][1], gates[a][2], gates[a][3], f"_l{actIndex}_")
        lock = ("XOR", f"_lock{actIndex}_", f"_l{actIndex}_", f"password[{actIndex}]", gates[a][-1])
        newWires.append(f"_l{actIndex}_")
        newGates[a] = locked
        lockGates.append(lock)

print("Processing done")

with open("newWires.txt", "w") as f:
    for i in newWires:
        f.write("wire " + i + ";\n")

with open("newGates.txt", "w") as f:
    for i in range(len(gates)):
        if i in usedIndices:
            f.write(formatGate(newGates[i]) + "\n")
        else:
            f.write(formatGate(gates[i]) + "\n")
    for i in lockGates:
        f.write(formatGate(i) + "\n")

print("Done")