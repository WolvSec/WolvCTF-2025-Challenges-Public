from pwn import *
import z3
import re

p = process('./chal')  

def clock_in():
    p.sendlineafter(b'> ', b'1')
    output = p.recvuntil(b'Quit job').decode()
    return output

def ask_for_raise(new_income):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'> ', str(new_income).encode())

def quit_job():
    p.sendlineafter(b'> ', b'3')
    return p.recvall()

message_patterns = [
    ("You forget to put the cover sheet on your TPS report", 0x0A),
    ("You have a meeting with a consultant", 0x16),
    ("The printer jams", 0x18),
    ("Your boss tells you that you have to come in on Saturday", 0x28),
    ("The fire alarm goes off", 0xA8),
    ("Your cowworker asks if you have seen his stapler", 0x60),
    ("You think about quitting", 0x01)
]

def infer_randombyte(output_list):
    solver = z3.Solver()
    original_rand_byte = z3.BitVec('rand_byte', 8)
    rand_byte = original_rand_byte
    
    for i in range(len(output_list)):
        day = output_list[i]
        for message, bit_pattern in message_patterns:
            if message in day:
                solver.add((rand_byte & bit_pattern) != 0)
            else:
                solver.add((rand_byte & bit_pattern) == 0)
        
        income = get_income(day)
        balance = get_balance(day)
        print(day)
        print("Day ", i, ", income ", income, ", balance ", balance)
        rand_byte = rand_byte ^ (balance & 0xff)
    
    if solver.check() == z3.sat:
        model = solver.model()
        
        # Get the initial value
        initial_value = model[original_rand_byte].as_long()
        return initial_value

        # WARNING: here i got trolled by my own ghidra variable namings ...
        
        # Recompute the transformations to get the final value
        #final_value = initial_value
        #for i in range(len(output_list)):
        #    day = output_list[i]
        #    balance = get_balance(day)
        #    final_value = final_value ^ (balance & 0xff)
        #
        #return final_value

        # end of warning...
    else:
        return None

# Extract income from clockin output
def get_income(output):
    match = re.search(r"You made \$(\d+) today", output)
    if match:
        return int(match.group(1))
    return None

# Extract balance from clockin output
def get_balance(output):
    match = re.search(r"Balance: \$(\d+)", output)
    if match:
        return int(match.group(1))
    return None


# Main solving logic
def solve():
    log.info("Starting solver")
    

    # Clock in multiple times to determine randombyte_as_int
    output_list = []
    for i in range(20):
        output_list.append(clock_in())

    randombyte = infer_randombyte(output_list)
    current_income = get_income(output_list[-1])
    current_balance = get_balance(output_list[-1])

    log.info(f"Inferred randombyte: {hex(randombyte)}")
    log.info(f"Current income: ${current_income}")
    log.info(f"Current balance: ${current_balance}")
    
    solve_balance = randombyte | (randombyte << 8)
    ask_for_raise(solve_balance - current_balance)
    clock_in()
    print(quit_job())

if __name__ == "__main__":
    solve()
