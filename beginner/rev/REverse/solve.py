def unmix_flag(mixed_flag):
    length = len(mixed_flag)
    flag_list = list(mixed_flag)  

    for i in range(0, length - 1, 2):
        next_index = length - 1 - (i + 1)
        flag_list[i], flag_list[next_index] = flag_list[next_index], flag_list[i]

    flag = ''.join([chr(ord(char) + 3) for char in flag_list])

    return flag

mixed_flag = "t`qcxo0s0o2.kd\.k\o0s0o20z"  
original_flag = unmix_flag(mixed_flag)

print("Original Flag:", original_flag)
