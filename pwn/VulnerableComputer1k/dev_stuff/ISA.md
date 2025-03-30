ideally 16bits 

operations:
- add rd, rs
- nand rd, rs
- lw rd, rb, offset
- sw rs, rb, offset 
- beq r1, r2, offset 
- halt

6 total 

000 add 
001 nand
010 beq 
011 halt 
10d lw 
11d sw  #lsb part of offset

13 bits left
3 rega
3 regb

5+1left for offset 

[ opcode ][ offset ][ reg a ][ reg b ]
    3b       7b        3b        3b 

