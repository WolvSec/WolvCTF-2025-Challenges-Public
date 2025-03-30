
# carry (1 or 0) is stored in r1 

# store registers
sw r4, r0, carrystore1
sw r5, r0, carrystore2
sw r6, r0, carrystore3

#grab "function" args
lw r4, r0, A 
nand r4, r7
nand r4, r4
lw r5, r0, B
nand r5, r7
nand r5, r5
lw r6, r0, Sum
nand r6, r7
nand r6, r6

# get the last bits
lw r1, r0, almost_bitmask
add r1, r1
nand r4, r1
nand r4, r4
nand r5, r1
nand r5, r5
nand r6, r1
nand r6, r6

# mathymath

# A&B
nand r4, r5
nand r4, r4
beq r4, r1, carry_one 

# (A^B) & ~Sum
lw r4, r0, A 
nand r4, r7
nand r4, r4
nand r4, r1
nand r4, r4
lw r6, r0, A 
nand r6, r7 
nand r6, r6
nand r6, r1
nand r6, r6

nand r4, r5
nand r5, r4
nand r4, r6
nand r4, r5
# r4 now contains A^B

lw r5, r0, Sum
nand r5, r7
nand r5, r5
nand r5, r1
# r5 contains ~Sum
nand r4, r5
nand r4, r4

beq r4, r1, carry_one
beq r0, r0, carry_zero

#return result in r1
# return 1 
.carry_one
lw r1, r0, one
beq r0, r0, carry_done

# return 0
.carry_zero
lw r1, r0, zero
beq r0, r0, carry_done

.carry_done
#restore registers
lw r4, r0, carrystore1
nand r4, r7
nand r4, r4
lw r5, r0, carrystore2
nand r5, r7
nand r5, r5
lw r6, r0, carrystore3
nand r6, r7
nand r6, r6
