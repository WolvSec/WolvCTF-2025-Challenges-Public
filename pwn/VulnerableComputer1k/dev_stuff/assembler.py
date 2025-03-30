#!/bin/python3
import struct

# Opcodes mapping
opcodes = {
    "add": "000",
    "nand": "001",
    "beq": "010",
    "halt": "011",
    "lw": "100",
    "sw": "110",
}

# Register mapping
register_map = {
    'r0': '000',
    'r1': '001',
    'r2': '010',
    'r3': '011',
    'r4': '100',
    'r5': '101',
    'r6': '110',
    'r7': '111',
}

def assemble_instruction(line, labels, address, loop_labels):
    parts = [p.strip(',') for p in line.strip().split()]
    opcode = parts[0]
    print(address//2, parts)

    if opcode == "halt":
        binary_instruction = f"{opcodes[opcode]}0000000000000"
    elif opcode in ["add", "nand"]:
        rd, rs = register_map[parts[1]], register_map[parts[2]]
        binary_instruction = f"{opcodes[opcode]}0000000{rd}{rs}"
    elif opcode in ["lw", "sw"]:
        rd, rb = register_map[parts[1]], register_map[parts[2]]
        offset = labels[parts[3]] // 2 if parts[3] in labels else int(register_map[parts[3]], 2)
        # Debug print for data access
        offset_bin = f"{offset & 0x7F:07b}"
        binary_instruction = f"{opcodes[opcode]}{offset_bin}{rd}{rb}"
    elif opcode == "beq":
        r1, r2 = register_map[parts[1]], register_map[parts[2]]
        offset = (loop_labels[parts[3]]-address) // 2 if parts[3] in loop_labels else int(register_map[parts[3]], 2)
        offset_bin = f"{offset & 0x7F:07b}"
        binary_instruction = f"{opcodes[opcode]}{offset_bin}{r1}{r2}"

    instruction = int(binary_instruction, 2) & 0xFFFF
    return struct.pack('<H', instruction)

def parse_code_sections(lines):
    data_section = []
    text_section = []
    
    # First pass: separate data and text sections
    for line in lines:
        if line.startswith("."):
            try:
                label, value = line.split()
                print(f"Found data label: {label}")
                data_section.append((label[1:], value))
            except:
                text_section.append(line)
                print(f"Found loop label: {line}")
        else:
            print(f"Found instruction: {line}")
            text_section.append(line)
    
    # Calculate addresses
    address = 2  # Start at 2 to account for initial jump
    labels = {}
    
    # Process data section labels
    print("\nData section layout:")
    for label, value in data_section:
        labels[label] = address
        print(f"Label {label:15s} at address {address:04x}")
        address += 2
    
    text_start_address = address
    print(f"\nText section starts at: {text_start_address:04x}\n")
    
    # Process text section labels
    loop_labels = {}
    for line in text_section:
        if line.startswith("."):
            label = line[1:]
            loop_labels[label] = address 
            print(f"Loop label {label:15s} at address {address:04x}")
        else:
            address += 2
            
    return data_section, text_section, labels, loop_labels, text_start_address

def remove_comments(lines):
    return [line for line in lines if not line.strip().startswith("#") and len(line.strip()) > 0]

def do_macros(assembly_code):
    macro_counter = 0
    
    def replace_macro(match_name, macro_content):
        nonlocal macro_counter
        current_counter = macro_counter
        macro_counter += 1
        
        lines = macro_content.split('\n')
        new_lines = []
        label_map = {}
        
        # First pass: identify and map labels
        for line in lines:
            if line.startswith('.') and len(line.split()) == 1:
                old_label = line[1:]
                new_label = f"{old_label}_{match_name}_{current_counter}"
                label_map[old_label] = new_label

        # Second pass: replace labels and references
        for line in lines:
            if line.startswith('.') and len(line.split()) == 1:
                new_lines.append(f".{label_map[line[1:]]}")
            elif "beq" in line:
                parts = line.split()
                target_label = parts[-1]
                if target_label in label_map:
                    parts[-1] = label_map[target_label]
                new_lines.append(" ".join(parts))
            else:
                new_lines.append(line)
                
        return '\n'.join(new_lines)

    while "$carry" in assembly_code or "$add64" in assembly_code:
        if "$carry" in assembly_code:
            carry = open('./determine_carry.as').read()
            assembly_code = assembly_code.replace("$carry", replace_macro('carry', carry), 1)
        if "$add64" in assembly_code:
            add64 = open('./add64.as').read()
            assembly_code = assembly_code.replace("$add64", replace_macro('add64', add64), 1)
            
    return assembly_code
    
def assemble_code(assembly_code):
    assembly_code = do_macros(assembly_code)
    print(assembly_code)
    lines = assembly_code.strip().splitlines()
    lines = remove_comments(lines)
    
    # Parse sections and get labels
    data_section, text_section, labels, loop_labels, text_start_address = parse_code_sections(lines)
    
    binary_output = bytearray()
    
    # Add initial jump to text section
    offset = (text_start_address - 0) // 2
    print(f"Initial jump offset: {offset} (to address {text_start_address:04x})")
    jump_instruction = f"{opcodes['beq']}{offset & 0x7F:07b}{register_map['r0']}{register_map['r0']}"
    binary_output.extend(struct.pack('<H', int(jump_instruction, 2)))
    
    # Add data section
    for _, value in data_section:
        binary_output.extend(struct.pack('<H', int(value, 16)))
    
    # Add text section
    address = text_start_address
    for line in text_section:
        if not line.startswith("."):
            instruction = assemble_instruction(line, labels, address, loop_labels)
            binary_output.extend(instruction)
            address += 2

    # Prepend the length of the output in words
    output_length = struct.pack('<H', len(binary_output) // 2)
    return output_length + binary_output

if __name__ == "__main__":
    assembly_code = open("exploit.as").read()
    binary_output = assemble_code(assembly_code)
    
    with open("exploit.bin", "wb") as f:
        f.write(binary_output)
    
    print("\nBinary output:", binary_output.hex())
