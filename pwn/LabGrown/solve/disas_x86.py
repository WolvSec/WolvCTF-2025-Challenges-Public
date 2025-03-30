from capstone import Cs, CS_ARCH_X86, CS_MODE_32
import re

def parse_bytecode(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    num_instrs_match = re.search(r'\(= NumInstrs (0b[01]+)\)', content)
    if num_instrs_match:
        num_instrs = int(num_instrs_match.group(1), 2)
    else:
        num_instrs = 0
        print("Warning: NumInstrs not found, assuming 0")
    
    bytecode = bytearray()
    bytecode_pattern = re.compile(r'\(= bytecode([0-9A-F]{2}) (0b[01]+)\)')
    
    for match in bytecode_pattern.finditer(content):
        offset = int(match.group(1), 16)
        value = int(match.group(2), 2)
        
        if offset >= len(bytecode):
            bytecode.extend([0] * (offset - len(bytecode) + 1))
        
        bytecode[offset] = value
    
    return bytecode, num_instrs

def disassemble_bytecode(bytecode, num_instrs):
    # Initialize Capstone disassembler for x86 32-bit
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    
    md.detail = True
    
    with open('shellcode.txt', 'a') as f:
        print(f"Disassembling {len(bytecode)} bytes of code, expecting {num_instrs} instructions:")
        print("Address\t\tBytes\t\t\tDisassembly")
        print("-" * 60)
        
        count = 0
        for i, (address, size, mnemonic, op_str) in enumerate(md.disasm_lite(bytes(bytecode), 0)):
            byte_str = ' '.join([f"{bytecode[address+j]:02x}" for j in range(size)])
            print(f"0x{address:04x}\t\t{byte_str:<16}\t{mnemonic} {op_str}")
            f.write(f"{byte_str} ");
            count += 1
            
            if count >= num_instrs and num_instrs > 0:
                break
        
        if count < num_instrs:
            print(f"Warning: Only found {count} instructions, but expected {num_instrs}")

def main():
    file_path = "esi.txt"  # Change this 
    bytecode, num_instrs = parse_bytecode(file_path)
    disassemble_bytecode(bytecode, num_instrs)

if __name__ == "__main__":
    main()
