class Instruction:
    def __init__(self, move: str, write: int, state: int):
        self.move = move
        self.write = write
        self.state = state
    
class Machine:
    
    
    def __init__(self, instructions):
        assert len(instructions) == 0x20
        self.table = [{},{}]
        self.head = 0x100
        self.tape = [0xf] * 0x200
        self.state = 0
        for i in range(0x20):
            self.table[i//0x10][i%0x10] = instructions[i]


    def run(self):
        while True:
            instruction = self.tape[self.head]
            instruction = self.table[self.state][instruction]

            self.tape[self.head] = instruction.write
            self.state = instruction.state
            
            if instruction.move == "H":
                break
            elif instruction.move == "R":
                self.head+=1
            elif instruction.move == "L":
                self.head-=1
            

            

            
    
