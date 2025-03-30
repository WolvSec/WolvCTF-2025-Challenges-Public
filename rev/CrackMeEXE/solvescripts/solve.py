from z3 import *

def solve_challenge():
    solver = Solver()
    
    # length 0x12 (18)
    input_bytes = [BitVec(f'input_{i}', 8) for i in range(18)]
    
    # Add constraint that all input bytes are printable ASCII
    for b in input_bytes:
        solver.add(b >= 32, b <= 126)
    
    xorbytes1 = [ord('f'), ord('l'), ord('a'), ord('g'), 0, 0, 0, 0]
    
    xorbytes2 = [0] * 25  # Initialize with zeros
    
    data1 = [0x11, 0x0f, 0x15, 0x01, 0x1d, 0x2d, 0x0f, 0x09]
    for i in range(8):
        xorbytes2[i + 1] = data1[i]
    
    data2 = [0x56, 0x15, 0x52, 0x03, 0x39, 0x35, 0x52, 0x13, 0x59, 0x11, 0x00]
    for i in range(len(data2)):
        xorbytes2[i + 9] = data2[i]
    
    # Add contraints
    for i in range(0x12, 0, -1):
        index = (i - 1) % 4
        solver.add(xorbytes2[i] == (input_bytes[i-1] ^ xorbytes1[index]))
    
    if solver.check() == sat:
        model = solver.model()
        solution = ''.join(chr(model[b].as_long()) for b in input_bytes)
        return solution
    else:
        return "No solution found"

result = solve_challenge()
print(f"Found solution: {result}")