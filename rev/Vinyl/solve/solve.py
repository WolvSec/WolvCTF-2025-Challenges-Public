import copy
import re
import numpy as np
import random
import sys

SIZE = 96
START = [48, 48]
CENTER = START
CHECKPOINTS = [
    [0, 28, 34],
    [0, 35, 32],
    [1, 26, 15],
    [0, 20, 33],
    [1, 31, 17],
    [0, 60, 89],
    [0, 46, 51],
    [0, 44, 85]
]
filename = 'maze.txt'

def load_from_file(filename):
    maze = DualSideMaze()
    current_side = None
    side_data = {0: [], 1: []}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "Side A":
                reading_checkpoints = False
                current_side = 0
                continue
            if line == "Side B":
                current_side = 1
                continue
            elif current_side is not None:
                side_data[current_side].append(list(line))

    # Convert the loaded data into numpy arrays
    for side in [0, 1]:
        if side_data[side]:
            maze.sides[side] = np.array(side_data[side])

    return maze

class DualSideMaze:
    def __init__(self):
        
        self.sides = [[],[]]
        self.gravity = (1, 0)  # Initial gravity: down
        self.pos = CENTER
        self.active_side = 0

        self.checkpoint_positions = []
        self.positions = []

    def do_command(self, command):
        if command == 'RR':
            self.clockwise_rot()
        if command == 'RL':
            self.counter_clockwise_rot()
        if command == 'HF':
            self.horizontal_flip()
        if command == 'VF':
            self.vertical_flip()
    
    def clockwise_rot(self):
        # active side rotates -90
        self.sides[self.active_side] = np.rot90(self.sides[self.active_side], -1)
        # other side rotates 90
        self.sides[1-self.active_side] = np.rot90(self.sides[1-self.active_side], 1)
        # position vector rotates -90
        self.pos = (self.pos[1], 95 - self.pos[0])
    
    def counter_clockwise_rot(self):
        # active side rotates 90
        self.sides[self.active_side] = np.rot90(self.sides[self.active_side], 1)
        # other side rotates -90
        self.sides[1-self.active_side] = np.rot90(self.sides[1-self.active_side], -1)
        # position vector rotates 90
        self.pos = (95 - self.pos[1], self.pos[0])


    def horizontal_flip(self):
        #horizontal position flips
        self.pos = (self.pos[0], SIZE-1-self.pos[1])
        #toggle active side
        self.active_side = 1 - self.active_side

        #make sure you didnt land on a wall 
        if self.sides[self.active_side][self.pos[0]][self.pos[1]] == '#':
            raise Exception("error generating maze")
        return 

    def vertical_flip(self):
        #vertical position flips
        self.pos = (SIZE-1-self.pos[0], self.pos[1])
        #toggle active side 
        self.active_side = 1 - self.active_side
        # sides flip vertically
        self.sides[self.active_side] = self.sides[self.active_side][::-1]
        self.sides[1-self.active_side] = self.sides[1-self.active_side][::-1]

        #make sure you didnt land on a wall 
        if self.sides[self.active_side][self.pos[0]][self.pos[1]] == '#':
            raise Exception("error generating maze") 
        return


    def simulate_n(self, commands):
        for i, command in enumerate(commands):
            #update orientation and position
            self.do_command(command)

            self.sides[self.active_side][self.pos] = 'X'
            #tick gravity until wall
            while True:
                nextpos = np.add(self.pos, self.gravity)
                if self.sides[self.active_side][nextpos[0]][nextpos[1]] == '#':
                    break
                self.pos = nextpos
                self.sides[self.active_side][self.pos[0]][self.pos[1]] = 'X'
            self.sides[self.active_side][self.pos[0]][self.pos[1]] = 'X'

            #self.positions.append([command, self.active_side, self.pos[0], self.pos[1]])
            #print(i,command, self.active_side, self.pos[0], self.pos[1])
            #self.print_maze()
        # Save final position
        #if len(commands) % 16 != 0:
        #    self.checkpoint_positions.append((self.active_side, self.pos))
        return
       
    def print_maze(self):
        print("Side B" if self.active_side else "Side A")
        print('\n'.join([''.join(row) for row in self.sides[self.active_side]]))

def str2command(s):
    bin_str = ''.join(format(ord(c), '08b') for c in s)
    cmd_map = {'00':'RR', '11':'RL', '01':'HF', '10':'VF'}
    commands = [cmd_map[bin_str[i:i+2]] for i in range(0, len(bin_str), 2)]
    return commands

def check_correct(maze,checkpoint_n):
    if (maze.active_side == CHECKPOINTS[checkpoint_n][0]
           and maze.pos[0] == CHECKPOINTS[checkpoint_n][1]
           and maze.pos[1] == CHECKPOINTS[checkpoint_n][2]):
        return True
    return False

def guess_next(curr, checkpoint_n, info):
    valid = []
    def get_char_range(pos):
        if isinstance(info[pos], str):  
            return [ord(info[pos])]
        return range(32, 127)  

    # Use nested loops only for unknown characters
    for c1 in get_char_range(0):
        for c2 in get_char_range(1):
            for c3 in get_char_range(2):
                for c4 in get_char_range(3):
                    guess = chr(c1) + chr(c2) + chr(c3) + chr(c4)
                    maze = load_from_file(filename)
                    try:
                        maze.simulate_n(str2command(curr + guess))
                    except:
                        continue
                    if check_correct(maze, checkpoint_n):
                        valid.append(curr + guess)
    return valid



def main():
    starting = 'wctf'
    checkpoint_n = 0
    #verify that first 4 work
    maze = load_from_file(filename)
    maze.simulate_n(str2command(starting))
    assert(maze.active_side == CHECKPOINTS[checkpoint_n][0]
           and maze.pos[0] == CHECKPOINTS[checkpoint_n][1]
           and maze.pos[1] == CHECKPOINTS[checkpoint_n][2])
    
    # I tested each checkpoint one by one to make sure theres only one solution
    # 1
    info = ["{",0,0,'r']
    checkpoint_n = 1
    nextfour = guess_next(starting,checkpoint_n,info)
    print(nextfour)
    
    # 2
    nextfour = ['wctf{$cr']
    possible = []
    checkpoint_n = 2
    info = [0,'t',0,'H']
    for guess in nextfour:
        p = guess_next(guess, checkpoint_n, info)
        possible += p
    print(possible)
    
    # 3 
    curr = ['wctf{$cr@tcH']
    checkpoint_n = 3
    possible = []
    info = ['1',0,'1',0]
    for guess in curr:
         p = guess_next(guess, checkpoint_n, info)
         possible += p
    print(possible)

    # 4 
    curr = ['wctf{$cr@tcH1-1;']
    checkpoint_n = 4
    possible = []
    info = ['K',0,0,'4']
    for guess in curr:
         p = guess_next(guess, checkpoint_n, info)
         possible += p
    print(possible)

    # 5
    curr = ['wctf{$cr@tcH1-1;K3-4']
    checkpoint_n = 5
    possible = []
    info = ['-',0,'3','3']
    for guess in curr:
         p = guess_next(guess, checkpoint_n, info)
         possible += p
    print(possible)

    # 6
    curr = ['wctf{$cr@tcH1-1;K3-4-133']
    checkpoint_n = 6
    possible = []
    info = ['7','~','c',0]
    for guess in curr:
         p = guess_next(guess, checkpoint_n, info)
         possible += p
    print(possible)
   
    # 7
    curr = ['wctf{$cr@tcH1-1;K3-4-1337~c4']
    checkpoint_n = 7
    possible = []
    info = [0,0,'2','}']
    for guess in curr:
         p = guess_next(guess, checkpoint_n, info)
         possible += p
    print(possible)


    







    

if __name__ == '__main__':
    main()