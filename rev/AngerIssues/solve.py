import angr
import claripy
import logging

logging.getLogger('angr').setLevel('INFO')

def char(state, n):
    vec =  state.solver.BVS(f'char_{n}', 8)
    return vec, state.solver.Or(state.solver.And(vec >= 0x30, vec <= 0x39), state.solver.And(vec >= 0x41, vec <= 0x7d))

START_ADRR = 0x00004387
FIND_ADDR = 0x0000439a
AVOID_ADDR = 0x000011a9  
INPUT_LEN = 59
INPUT_ADDR = 0x00009040 

p = angr.Project("./original", main_opts={'base_addr': 0x0})

initial_state = p.factory.blank_state(addr=START_ADRR)
initial_state.options.add(angr.options.LAZY_SOLVES)

for i in range(INPUT_LEN):
    c, c_constr = char(initial_state, i)
    initial_state.memory.store(INPUT_ADDR + i, c)
    initial_state.add_constraints(c_constr)

sm = p.factory.simulation_manager(initial_state)
sm.explore(find=FIND_ADDR, avoid=AVOID_ADDR)

if sm.found:
    for solution_state in sm.found:
        flag = solution_state.solver.eval(solution_state.memory.load(INPUT_ADDR, INPUT_LEN), cast_to=bytes)
        print(flag)
else:
    print("Not found")

# wctf{1_h0p3_y0u_u53d_ANGR_f0r_th15_0r_y0U_w0uLd_b3_a_duMMy}