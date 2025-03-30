flag = "wctf{v3n!_V!dI_v!C!_!1!1}"
print(flag)
print("\n")

matrix = [['' for _ in range(5)] for _ in range(5)]
i = 0
for diag in range(2 * 5 - 1):
    for row in range(5):
        col = diag - row
        if 0 <= col < 5 and 0 <= row < 5:
            if row < 5 and col >= 0 and (row * 5 + col) < len(flag):
                matrix[row][col] = flag[i]
                i += 1

transposition = ""
for row in matrix:
    print(''.join(row))
    transposition += "".join(row)
print("\n")

print(transposition)
print("\n")

caesar = ""
for char in transposition:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            caesar += chr((ord(char) - base + 23) % 26 + base)
        else:
            caesar += char

print(caesar)