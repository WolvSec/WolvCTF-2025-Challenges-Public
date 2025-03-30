import re
from z3 import *
import random

index_regex = r"([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]"
parse_gates_regex = r"(\w+)\s+(_lock\d+_|_\d+_)\s*\(\s*\.A\s*\(\s*([^)]+)\s*\)\s*,\s*\.B\s*\(\s*([^)]+)\s*\)\s*,\s*\.(Y|C)\s*\(\s*([^)]+)\s*\)\s*\)"

buses = {}
buses['a'] = BitVec('a',32)
buses['b'] = BitVec('b',32)
buses['c'] = BitVec('c',32)
buses['password'] = BitVec('password',48)
s = Solver()
constraints = []

with open("synth.v","r") as f:
    file_contents = f.read()

gates = re.findall(parse_gates_regex,file_contents)

# make all wires symbolic BitVecs of Length 1
wires = {}
for gate in gates:
    gate_type, _, a_wire, b_wire, _, out_wire = gate
    if '[' not in a_wire and a_wire not in wires:
        wires[a_wire] = BitVec(a_wire,1)
    if '[' not in b_wire and b_wire not in wires:
        wires[b_wire] = BitVec(b_wire,1)
    if '[' not in out_wire and out_wire not in wires:
        wires[out_wire] = BitVec(out_wire,1)

def get_symbolic(variable):
    if '[' in variable:
        match = re.search(index_regex,variable)
        if not match:
            print("index regex failed: ",variable)
            exit()
        array_name = match.group(1)
        index = int(match.group(2))
        return Extract(index,index,buses[array_name])
    else:
        return wires[variable]

# add gate functionality as constraints to the solver
print("Matched N Gates = ",len(gates))
for gate in gates:
    gate_type, _, a_wire, b_wire, _, out_wire = gate

    #get symbolic vars
    a_wire = get_symbolic(a_wire)
    b_wire = get_symbolic(b_wire)
    out_wire = get_symbolic(out_wire)

    if gate_type == "AND":
        constraint = out_wire == (a_wire & b_wire)
    elif gate_type == "OR":
        constraint = out_wire == (a_wire | b_wire)
    elif gate_type == "XOR":
        constraint = out_wire == (a_wire ^ b_wire)
    elif gate_type == "NAND":
        constraint = out_wire == ~(a_wire & b_wire)
    elif gate_type == "NOR":
        constraint = out_wire == ~(a_wire | b_wire)
    elif gate_type == "XNOR":
        constraint = out_wire == ~(a_wire ^ b_wire)

    print(constraint)
    constraints.append(constraint)

#specify adder
a = buses['a']
b = buses['b']
c = buses['c']
constraints.append(a+b == c)

circuit_constraints = And(constraints)

s.add(ForAll([a,b],circuit_constraints))


if s.check() == sat:
    model = s.model()
    print()
    print("A = ",model[a])
    print("B = ",model[b])
    print("C = ", model[c])
    print("Found a password that makes the circuit work for all inputs:")
    print("password =", model[buses['password']])
    password_value = model[buses['password']].as_long()

     # Extract bytes and convert to ASCII
    ascii_password = ""
    bytes_array = []

    # Extract each byte (assuming 8 bits per character)
    for i in range(6):  # For a 48-bit password, we can get 6 bytes (6*8=48)
        # Extract 8 bits at a time, starting from the least significant byte
        byte_val = (password_value >> (i*8)) & 0xFF
        bytes_array.append(byte_val)

        # Convert to ASCII if in printable range
        if 32 <= byte_val <= 126:  # Printable ASCII range
            ascii_password = chr(byte_val) + ascii_password  # Prepend because we're going LSB to MSB
        else:
            ascii_password = f"\\x{byte_val:02x}" + ascii_password

    print("Password as bytes:", bytes_array)
    print("Password as ASCII:", ascii_password)


else:
    print("unsat")
    print("Core:",s.unsat_core())
