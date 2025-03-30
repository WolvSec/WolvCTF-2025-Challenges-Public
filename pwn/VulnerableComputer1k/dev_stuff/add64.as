
#grab "function" args
lw r4, r0, A_ptr 
nand r4, r7
nand r4, r4
lw r5, r0, B_ptr
nand r5, r7
nand r5, r5
lw r6, r0, Sum_ptr
nand r6, r7
nand r6, r6

# sum the first 1/4
lw r2, r4, r0
lw r3, r5, r0
sw r2, r0, A 
add r2, r3
sw r3, r0, B
sw r2, r0, Sum 

# store and increase pointers
sw r2, r6, r0
lw r1, r0, one
add r4, r1
add r5, r1
add r6, r1
sw r4, r0, A_ptr
sw r5, r0, B_ptr 
sw r6, r0, Sum_ptr

$carry 

#restore pointers
lw r4, r0, A_ptr 
nand r4, r7
nand r4, r4
lw r5, r0, B_ptr
nand r5, r7
nand r5, r5
lw r6, r0, Sum_ptr
nand r6, r7
nand r6, r6

# sum the second 2/4
lw r2, r4, r0
lw r3, r5, r0
sw r2, r0, A 
add r2, r3
#add carry 
add r2, r1
sw r3, r0, B
sw r2, r0, Sum 

# store and increase pointers
sw r2, r6, r0
lw r1, r0, one
add r4, r1
add r5, r1
add r6, r1
sw r4, r0, A_ptr
sw r5, r0, B_ptr 
sw r6, r0, Sum_ptr

$carry 

#restore pointers
lw r4, r0, A_ptr 
nand r4, r7
nand r4, r4
lw r5, r0, B_ptr
nand r5, r7
nand r5, r5
lw r6, r0, Sum_ptr
nand r6, r7
nand r6, r6

# sum the second 3/4
lw r2, r4, r0
lw r3, r5, r0
sw r2, r0, A 
add r2, r3
#add carry 
add r2, r1
sw r3, r0, B
sw r2, r0, Sum 

# store and increase pointers
sw r2, r6, r0
lw r1, r0, one
add r4, r1
add r5, r1
add r6, r1
sw r4, r0, A_ptr
sw r5, r0, B_ptr 
sw r6, r0, Sum_ptr

$carry 

#restore pointers
lw r4, r0, A_ptr 
nand r4, r7
nand r4, r4
lw r5, r0, B_ptr
nand r5, r7
nand r5, r5
lw r6, r0, Sum_ptr
nand r6, r7
nand r6, r6

# sum the second 4/4
lw r2, r4, r0
lw r3, r5, r0
sw r2, r0, A 
add r2, r3
#add carry 
add r2, r1
sw r3, r0, B
sw r2, r0, Sum 

# store 
sw r2, r6, r0
