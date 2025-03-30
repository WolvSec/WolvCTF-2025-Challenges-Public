
f = open("ciphertext.txt","r")

lines = f.readlines()
crib = ['w','c','t','f']
for i in range(4):
    num = int(lines[i],2)
    print(bin(num^ord(crib[i])))

