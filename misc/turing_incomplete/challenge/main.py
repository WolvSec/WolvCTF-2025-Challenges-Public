from machine import Machine, Instruction

def main():

    instructions = input()
    encoded = []
    for instruction in instructions.split():
        move, write, state = instruction 
        encoded.append(Instruction(move, int(write, base=16), int(state, base=16)))

    for i in range(10):
        for j in range(10):
            for k in range(10):
                machine = Machine(encoded)
                tape = machine.tape
                tape[machine.head] = i
                tape[machine.head-1] = j
                tape[machine.head-2] = k
                tape[machine.head+1] = 0xa
                tape[machine.head+2] = 0xa

                end_location = machine.head + 1

                machine.run()

                assert (machine.tape[end_location] == i + j + k) or (machine.tape[end_location] + machine.tape[end_location + 1] * 10) == i + j + k

    
    with open("flag.txt", "rb") as flag:
        print(flag.read())

        
                
if __name__ == "__main__":
    main()
