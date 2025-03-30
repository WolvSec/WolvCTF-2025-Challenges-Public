import random

def main():
    
    print("Let's play a game, I am thinking of a number between 0 and", 2 ** 64, "\n")

    try:
        guess = eval(input("What is the number?: "))
    except:
        guess = 0

    correct = random.randint(0, 2**64)
    
    if (guess == correct):
        print("\nCorrect! You won the flag!")
        flag = open("flag.txt", "r").readline()
        print(flag)
    else:
        print("\nYou lost lol")

main()

