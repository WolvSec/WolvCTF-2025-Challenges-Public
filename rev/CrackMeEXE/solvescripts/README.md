These solvescripts complement the reverse engineering

Steps:
1. unpack the binary using upx
2. reverse engineer unpacked binary to find relevant functions
3. notice that memory is being allocated and then decoded and executed
4. use frida to dump the decoded memory
5. reverse engineer decoded memory
6. use z3 to find solution from decoded memory
