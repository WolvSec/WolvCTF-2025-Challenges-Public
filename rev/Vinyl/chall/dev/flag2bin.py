import re

flag = "wctf{$cr@tcH1-1;K3-4-1337~c47-2}"
print("Flag is ", flag)

res = ''.join(format(ord(i), '08b') for i in flag)
print('Flag in bits ', res)

moves = {
    '00': "RR",  # Rotate Right
    '11': "RL",  # Rotate Left
    '10': "VF",  # Flip along vertical
    '01': "HF"   # Flip along horizontal
}

previous_move = None
repeated_characters = []

for i, move in enumerate(re.findall("..", res)):
    current_move = moves[move]
    print(current_move, end=' ')
    
    if current_move == previous_move and 'F' in current_move :
        # Calculate which character caused the repeated move
        char_index = i // 4  # Each character is represented by 4 moves (8 bits / 2 bits per move)
        repeated_characters.append((char_index, flag[char_index]))
    
    previous_move = current_move

print()

if repeated_characters:
    print("\nCharacters causing repeated moves:")
    for char_index, char in repeated_characters:
        print(f"Character '{char}' at position {char_index + 1} caused a repeated move.")
else:
    print("\nNo characters caused repeated moves.")