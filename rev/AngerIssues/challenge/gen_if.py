
def main():
    f  = open("obfusc.txt",'r')
    constraints = f.readlines()
    
    # print out the function definitions
    # for i,c in enumerate(constraints):
    #     #print out the function definitions
    #     bracket = "{"
    #     print(f"void func{i}(char* pw){bracket}")
    #     print(f"if({c}){bracket}")
    #     print("return;\n}")
    #     print("else{")
    #     print("errorFunc();\n}")
    #     print("}")

    #call the functions
    for i,c in enumerate(constraints):
        print(f"func{i}(pw);")



if __name__ == "__main__":
    main()