import copy
import re
import numpy as np
import random
import sys


SIZE = 64+32 
CENTER = (SIZE//2, SIZE//2)

def load_from_file(filename):
    maze = DualSideMaze()
    current_side = None
    side_data = {0: [], 1: []}
    reading_checkpoints = False

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "=== Checkpoints ===":
                reading_checkpoints = True
                continue
            if line == "=== Side A ===":
                reading_checkpoints = False
                current_side = 0
                continue
            if line == "=== Side B ===":
                current_side = 1
                continue
            if reading_checkpoints:
                # Store checkpoint information in maze object
                if line.startswith("Checkpoint"):
                    # Parse checkpoint line
                    parts = line.split(": ")
                    side_str = parts[1].split(",")[0]
                    pos_str = ",".join(parts[1].split(",")[1:]).strip()
                    side = 1 if "B" in side_str else 0
                    pos = eval(pos_str.replace("Position ", ""))
                    maze.checkpoint_positions.append((side, pos))
            elif current_side is not None:
                side_data[current_side].append(list(line))

    # Convert the loaded data into numpy arrays
    for side in [0, 1]:
        if side_data[side]:
            maze.sides[side] = np.array(side_data[side])

    return maze

class DualSideMaze:
    def __init__(self):
        # Initialize both sides with boundary walls only
        self.sides = {
            0: np.full((SIZE, SIZE), '#', dtype=str),
            1: np.full((SIZE, SIZE), '#', dtype=str)
        }
        # Create circular boundary
        for s in [0, 1]:
            for i in range(SIZE):
                for j in range(SIZE):
                    if (i-CENTER[0])**2 + (j-CENTER[1])**2 <= (CENTER[0]-4)**2:
                        self.sides[s][i,j] = '.'
        
        self.gravity = (1, 0)  # Initial gravity: down
        self.pos = CENTER
        self.active_side = 0

        self.sides[1] = np.fliplr(self.sides[1])

        self.sides[0][0,0] = 'O'
        self.sides[0][0,1] = 'O'
        self.sides[1][0,0] = 'O'
        self.sides[1][0,1] = 'O'
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
            print("ERROR GENERATING MAZE")
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
            print("ERROR GENERATING MAZE")
            raise Exception("error generating maze") 
        return


    def build_maze(self, commands):
        """Build maze doing commands and simulating physics"""
        for i, command in enumerate(commands):
            # Save position every 16 moves
            if i > 0 and i % 16 == 0:
                self.checkpoint_positions.append((self.active_side, self.pos))

            #update orientation and position
            self.do_command(command)

            self.sides[self.active_side][self.pos] = '@'
            #tick gravity a random number of times
            guesses = 0
            while True:
                guesses += 1
                n = random.randint(2,16) #choose rand that wont ruin path
                if self.pos[0]+n+1 < SIZE and self.sides[self.active_side][self.pos[0]+n+1][self.pos[1]] != '@':
                    break
                if guesses > 30:
                    raise Exception("AAAAA")
                
            for _ in range(n):
                nextpos = np.add(self.pos, self.gravity)
                if self.sides[self.active_side][nextpos[0]][nextpos[1]] == '#':
                    break
                self.pos = nextpos
                self.sides[self.active_side][self.pos[0]][self.pos[1]] = '@'
            self.sides[self.active_side][self.pos[0]][self.pos[1]] = '@'

            #put floor underneath you
            if self.sides[self.active_side][self.pos[0]+1][self.pos[1]] == '@':
                raise Exception("WHAT IS GOING ON")
            self.sides[self.active_side][self.pos[0]+1][self.pos[1]] = '#'

            #self.positions.append([command, self.active_side, self.pos[0], self.pos[1]])
            print(i,command, self.active_side, self.pos[0], self.pos[1])
            self.print_maze()


        # Save final position
        if len(commands) % 16 != 0:
            self.checkpoint_positions.append((self.active_side, self.pos))
        return
       
    def print_maze(self):
        print("Side B" if self.active_side else "Side A")
        print('\n'.join([''.join(row) for row in self.sides[self.active_side]]))
        
    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(f"Start = {CENTER} , End = {self.pos}\n")
            # Add checkpoint positions
            f.write("=== Checkpoints ===\n")
            for i, (side, pos) in enumerate(self.checkpoint_positions):
                f.write(f"Checkpoint {i+1}: Side {'B' if side else 'A'}, Position {pos}\n")
            f.write("\n=== Side A ===\n")
            f.write('\n'.join([''.join(row) for row in self.sides[0]]))
            f.write("\n\n=== Side B ===\n")
            f.write('\n'.join([''.join(row) for row in self.sides[1]]))

    def complete_maze(self):
        path_ends = self.find_path_ends()
        for node in path_ends:
            self.extend_paths(node)

        # Randomly place walls, avoiding the solution path
        for side in range(2):
            for i in range(SIZE):
                for j in range(SIZE):
                    if self.sides[side][i][j] == '.':
                        if random.randint(1, 10) <= 5:
                            self.sides[side][i][j] = '#'

        # Clean up, ensuring the solution path is preserved
        for side in range(2):
            for i in range(SIZE):
                for j in range(SIZE):
                    if self.sides[side][i][j] != '#' and self.sides[side][i][j] != '@':
                        self.sides[side][i][j] = '.'

    def find_path_ends(self):
        nodes = [] # [side,x,y,vertical/horizontal]
        for side in range(2):
            for x in range(1,SIZE-1):
                for y in range(1,SIZE-1):
                    curr = self.sides[side][x][y]
                    left = self.sides[side][x][y-1]
                    right = self.sides[side][x][y+1]
                    up = self.sides[side][x-1][y]
                    down = self.sides[side][x+1][y]
                    if curr != '@':
                        continue #not in path

                    #check horizontal
                    if (left == '#' and right == '@') or (left == '@' and right == '#'):
                        nodes.append([side,x,y,'v']) #extend vertically
                        continue
                    #check vertical
                    if (up == '#' and down == '@') or (up == '@' and down == '#'):
                        nodes.append([side,x,y,'h']) #extend horizontally
                        continue
        return nodes

    def extend_paths(self, node):
        side, x, y, dir = node
        if dir == 'h':
            #extend horizontally
            #go left
            curx = x
            cury = y
            for i in range(random.randint(1,8)):
                cury-=1
                if self.sides[side][curx][cury] == '#':
                    break #hit a wall
                #mark it
                if self.sides[side][curx][cury] == '.':
                    self.sides[side][curx][cury] = 'X'
            # put a wall at the end
            if self.sides[side][curx][cury] != '@':
                self.sides[side][curx][cury] = '#'

            #go right
            curx = x
            cury = y
            for i in range(random.randint(1,8)):
                cury+=1
                if self.sides[side][curx][cury] == '#':
                    break #hit a wall
                #mark it
                if self.sides[side][curx][cury] == '.':
                    self.sides[side][curx][cury] = 'X'
            # put a wall at the end
            if self.sides[side][curx][cury] != '@':
                self.sides[side][curx][cury] = '#'

        elif dir == 'v':
            #extend vertically
            #go up
            curx = x
            cury = y
            for i in range(random.randint(1,8)):
                curx-=1
                if self.sides[side][curx][cury] == '#':
                    break #hit a wall
                #mark it
                if self.sides[side][curx][cury] == '.':
                    self.sides[side][curx][cury] = 'X'
            # put a wall at the end
            if self.sides[side][curx][cury] != '@':
                self.sides[side][curx][cury] = '#'

            #go down
            curx = x
            cury = y
            for i in range(random.randint(1,8)):
                curx+=1
                if self.sides[side][curx][cury] == '#':
                    break #hit a wall
                #mark it
                if self.sides[side][curx][cury] == '.':
                    self.sides[side][curx][cury] = 'X'
            # put a wall at the end
            if self.sides[side][curx][cury] != '@':
                self.sides[side][curx][cury] = '#'

        return
        
import re

def update_c_code(maze_data, template_file, output_file):
    with open(template_file, 'r') as f:
        template = f.read()

    # Replace placeholders with maze data
    template = template.replace("START_POS", f"{{{maze_data['start'][0]}, {maze_data['start'][1]}}}")
    template = template.replace("START_X", str(maze_data['start'][0]))
    template = template.replace("START_Y", str(maze_data['start'][1]))
    template = template.replace("END_POS", f"{{{maze_data['end_active_side']},{maze_data['end'][0]}, {maze_data['end'][1]}}}")

    checkpoints_data = ",\n    ".join([f"{{{side}, {pos[0]}, {pos[1]}}}" for side, pos in maze_data['checkpoints']])
    template = template.replace("CHECKPOINT_DATA", checkpoints_data)

    side_a_data = ",\n            ".join([f'"{row}"' for row in maze_data['side_a'].split('\n')])
    template = template.replace("SIDE_A_DATA", side_a_data)

    side_b_data = ",\n            ".join([f'"{row}"' for row in maze_data['side_b'].split('\n')])
    template = template.replace("SIDE_B_DATA", side_b_data)

    with open(output_file, 'w') as f:
        f.write(template)


if __name__ == "__main__":
    yn = input("Do you want to generate a solving path? (Y/N): ")
    if yn != 'N':
        flag = "wctf{$cr@tcH1-1;K3-4-1337~c47-2}"
        bin_str = ''.join(format(ord(c), '08b') for c in flag)
        cmd_map = {'00':'RR', '11':'RL', '01':'HF', '10':'VF'}
        commands = [cmd_map[bin_str[i:i+2]] for i in range(0, len(bin_str), 2)]
        attempts = 0
        while True: 
            try:
                #DEBUG
                sys.stdout = open('generate_out.txt', 'w')
                #END DEBUG
                print("\n============================= START =============================\n")
                maze = DualSideMaze()
                maze.build_maze(commands)
                maze.save("maze.txt")
                break
            except Exception as e:
                print(e)
                continue
        print("Took ",attempts, " attempts to generate maze")
        print("Ending position ", maze.pos)
        print("Number of moves ", len(commands))
        for pos in maze.positions:
            print(pos)
    else:
        maze = load_from_file("maze.txt")

    yn = input("Do you want to complete the generated maze (Y/N): ")
    if yn != 'N':
        maze.complete_maze()
        maze.save("extended_maze.txt")
        maze.print_maze()

        #align maze sides before writing them
        for side in range(2):
            for i in range(8):
                if i == 4:
                    maze.sides[side] = maze.sides[side][::-1]
                if maze.sides[side][0,0] == '.' and maze.sides[side][0,1] == '.':
                    break
                maze.sides[side] = np.rot90(maze.sides[side], 1)
                

        maze_data = {
        "start": CENTER,
        "end_active_side": maze.active_side,
        "end": maze.pos,
        "checkpoints": maze.checkpoint_positions,
        "side_a": '\n'.join([''.join(row) for row in maze.sides[0]]),
        "side_b": '\n'.join([''.join(row) for row in maze.sides[1]])
        }
        update_c_code(maze_data, "template.c", "vinyl.c")
