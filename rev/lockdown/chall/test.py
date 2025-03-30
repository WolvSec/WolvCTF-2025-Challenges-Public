import re
from z3 import *

# Regex to parse gates (already tested and working)
index_regex = r"([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]"
parse_gates_regex = r"(\w+)\s+(_lock\d+_|_\d+_)\s*\(\s*\.A\s*\(\s*([^)]+)\s*\)\s*,\s*\.B\s*\(\s*([^)]+)\s*\)\s*,\s*\.(Y|C)\s*\(\s*([^)]+)\s*\)\s*\)"

# Initialize buses and password
a = BitVec('a', 32)  # Input a (32-bit)
b = BitVec('b', 32)  # Input b (32-bit)
c = BitVec('c', 32)  # Output c (32-bit)
password = BitVec('password', 48)  # Password (48-bit)

# Initialize solver
s = Solver()

# Read the Verilog file
with open("synth.v", "r") as f:
    file_contents = f.read()

# Parse gates from the Verilog file
gates = re.findall(parse_gates_regex, file_contents)

# Create symbolic variables for wires
wires = {}
for gate in gates:
    gate_type, _, a_wire, b_wire, _, out_wire = gate
    if '[' not in a_wire and a_wire not in wires:
        wires[a_wire] = BitVec(a_wire, 1)  # Assume 1-bit wires
    if '[' not in b_wire and b_wire not in wires:
        wires[b_wire] = BitVec(b_wire, 1)  # Assume 1-bit wires
    if '[' not in out_wire and out_wire not in wires:
        wires[out_wire] = BitVec(out_wire, 1)  # Assume 1-bit wires

# Function to get symbolic representation of a wire
def get_symbolic(variable):
    if '[' in variable:
        match = re.search(index_regex, variable)
        if not match:
            print("index regex failed: ", variable)
            exit()
        array_name = match.group(1)
        index = int(match.group(2))
        if array_name == 'a':
            return Extract(index, index, a)
        elif array_name == 'b':
            return Extract(index, index, b)
        elif array_name == 'c':
            return Extract(index, index, c)
        elif array_name == 'password':
            return Extract(index, index, password)
        else:
            print(f"Unknown array: {array_name}")
            exit()
    else:
        return wires[variable]

# Add gate functionality as constraints
for gate in gates:
    gate_type, gate_name, a_wire, b_wire, _, out_wire = gate

    # Get symbolic representations of the wires
    a_wire_sym = get_symbolic(a_wire)
    b_wire_sym = get_symbolic(b_wire)
    out_wire_sym = get_symbolic(out_wire)

    # Add gate constraints based on gate type
    if gate_type == "AND":
        s.add(out_wire_sym == (a_wire_sym & b_wire_sym))
    elif gate_type == "OR":
        s.add(out_wire_sym == (a_wire_sym | b_wire_sym))
    elif gate_type == "XOR":
        s.add(out_wire_sym == (a_wire_sym ^ b_wire_sym))
    elif gate_type == "NAND":
        s.add(out_wire_sym == ~(a_wire_sym & b_wire_sym))
    elif gate_type == "NOR":
        s.add(out_wire_sym == ~(a_wire_sym | b_wire_sym))
    elif gate_type == "XNOR":
        s.add(out_wire_sym == ~(a_wire_sym ^ b_wire_sym))
    elif gate_type == "XOR" and "lock" in gate_name:
        # Handle password XOR gates
        s.add(out_wire_sym == (a_wire_sym ^ b_wire_sym))

# Add the adder constraint: for all a and b, a + b == c
s.add(ForAll([a, b], c == a + b))

# Check if the constraints are satisfiable
if s.check() == sat:
    model = s.model()
    print("Found a password that makes the circuit work for all inputs:")
    password_value = model[password].as_long()
    print("Password (decimal):", password_value)

    # Extract bytes and convert to ASCII
    ascii_password = ""
    bytes_array = []
    for i in range(6):  # For a 48-bit password, extract 6 bytes
        byte_val = (password_value >> (i * 8)) & 0xFF
        bytes_array.append(byte_val)
        if 32 <= byte_val <= 126:  # Printable ASCII range
            ascii_password = chr(byte_val) + ascii_password  # Prepend for correct order
        else:
            ascii_password = f"\\x{byte_val:02x}" + ascii_password

    print("Password as bytes:", bytes_array)
    print("Password as ASCII:", ascii_password)
else:
    print("No solution found (unsat)")
