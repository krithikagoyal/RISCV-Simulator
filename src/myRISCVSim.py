"""
The project is developed as part of Computer Architecture class.
Project Name: Functional Simulator for subset of RISC-V Processor

-------------------------------------------------
| Developer's Name   | Developer's Email ID     |
|-----------------------------------------------|
| Akhil Arya         | 2019csb1066@iitrpr.ac.in |
| Harshwardhan Kumar | 2019csb1089@iitrpr.ac.in |
| Krithika Goyal     | 2019csb1094@iitrpr.ac.in |
| Rhythm Jain        | 2019csb1111@iitrpr.ac.in |
| Tarun Singla       | 2019csb1126@iitrpr.ac.in |
-------------------------------------------------
"""

# myRISCVSim.py
# Purpose of this file: Implementation file for myRISCVSim

from collections import defaultdict

# Register file
R = [0]*32

# Flags and clock
N = C = V = Z = clock = 0

# Program Counter
PC = 0

# Memory
MEM = defaultdict(lambda: '00')

# Intermediate datapath and control path signals
instruction_word = 0
operand1 = 0
operand2 = 0
operation = ''
rd = 0
register_data = '0x00000000'
memory_address = 0
memory_element = '00'
memory_data = '00'
is_mem = [False, 0, 'n']


# run_RISCVsim function
def run_RISCVsim():
    while(1):
        fetch()
        decode()
        execute()
        mem()
        write_back()
        clock += 1
        print("Number of clock cycles: ", clock)


# It is used to set the reset values
def reset_proc():
    for i in range(32):
        R[i] = '0x00000000'
    R[2] = '0x7FFFFFF0'
    R[3] = '0x10000000'


# load_program_memory reads the input memory, and populates the instruction memory
def load_program_memory(file_name):
    try:
        fp = open(file_name, 'r')
        for line in fp:
            tmp = line.split()
            if len(tmp) == 2:
                address, instruction = tmp[0], tmp[1]
                write_word(address, instruction)
        fp.close()
    except:
        print("Error opening input mem file.\n")
        exit(1)


# Writes the data memory in "data_out.mc" file
def write_data_memory():
    try:
        fp = open("data_out.mc", "w")
        out_tmp = []
        for i in range(1000, 4):
            out_tmp.append(hex(i) + ' 0x' + MEM[i * 4 + 3] + MEM[i * 4 + 2] + MEM[i * 4 + 1] + MEM[i * 4])
        fp.writelines(out_tmp)
        fp.close()
    except:
        print("Error opening data_out.mc file for writing.\n")


# It should be called when instruction is swi_exit
def swi_exit():
    write_data_memory()
    exit(0)


# Reads from the instruction memory and updates the instruction register
def fetch():
    instruction_word = '0x' + MEM[PC + 3] + MEM[PC + 2] + MEM[PC + 1] + MEM[PC]
    PC += 4


# Reads the instruction register, operand1 and operand2 from register file; decides the operation to be performed in the execute stage
def decode():
    if instruction_word == '0x401010BB':
        swi_exit()

    bin_instruction = bin(int(instruction_word[2:],16))[2:]

    bin_instruction = (32 - len(bin_instruction)) * '0' + bin_instruction
    opcode = int(bin_instruction[25:32], 2)
    func3 = int(bin_instruction[17:20], 2)
    func7 = int(bin_instruction[0:7], 2)

    f = open('Instruction_Set_List.csv')
    instruction_set_list = list(csv.reader(f))
    f.close()
    match_found = False
    track = 0

    for ins in instruction_set_list:
        if track == 0:
            match_found = False
        elif ins[4] != 'NA' and [int(ins[2], 2), int(ins[3], 2), int(ins[4], 2)] == [opcode, func3, func7]:
            match_found = True
        elif ins[4] == 'NA' and ins[3] != 'NA' and [int(ins[2], 2), int(ins[3], 2)] == [opcode, func3]:
            match_found = True
        elif ins[4] == 'NA' and ins[3] == 'NA' and int(ins[2], 2) == opcode:
            match_found = True
        if match_found:
            break
        track += 1

    op_type = instruction_set_list[track][0]
    operation = instruction_set_list[track][1]

    rd = 0
    register_data = '0x00000000'
    is_mem = [False, 0, 'n']
    if op_type == 'R':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        rd = bin_instruction[20:25]
        operand1 = R[int(rs1, 2)]
        operand2 = R[int(rs2, 2)]

    elif op_type == 'I':
        rs1 = bin_instruction[12:17]
        rd = bin_instruction[20:25]
        imm = bin_instruction[0:12]
        operand1 = R[int(rs1, 2)]
        operand2 = imm

    elif op_type == 'S':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        imm = bin_instruction[0:7] + bin_instruction[20:25]
        operand1 = R[int(rs1, 2)]
        operand2 = imm

    elif op_type == 'SB':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        operand1 = int(rs1, 2)
        operand2 = int(rs2, 2)
        imm = bin_instruction[0] + bin_instruction[24] + bin_instruction[1:7] + bin_instruction[20:24] + '0'

    elif op_type == 'U':
        rd = bin_instruction[20:25]
        imm = bin_instruction[0:20] + '0'*12

    elif op_type == 'UJ':
        rd = bin_instruction[20:25]
        imm = bin_instruction[0] + bin_instruction[12:20] + bin_instruction[11] + bin_instruction[1:11] + '0'

    else:
        print("Unidentifiable machine code!")
        swi_exit()


# Executes the ALU operation based on ALUop
def execute():
    if operation == 'add':
        register_data = hex(int(int(operand1, 16) + int(operand2, 16)))

    elif operation == 'sub':
        register_data = hex(int(int(operand1, 16) - int(operand2, 16)))

    elif operation == 'and':
        register_data = hex(int(int(operand1, 16) & int(operand2, 16)))

    elif operation == 'or':
        register_data = hex(int(int(operand1, 16) | int(operand2, 16)))

    elif operation == 'sll':
        register_data = hex(int(int(operand1, 16) << int(operand2, 16)))

    elif operation == 'slt':
        if (int(operand1, 16) < int(operand2, 16)):
            register_data = hex(1)
        else:
            register_data = hex(0)

    elif operation == 'sra':
        register_data = hex(int(int(operand1, 16) >> int(operand2, 16)))

    elif operation == 'srl':
        register_data = hex(int(operand1, 16) >> int(operand2, 16))

    elif operation == 'xor':
        register_data = hex(int(int(operand1, 16) ^ int(operand2, 16)))

    elif operation == 'mul':
        register_data = hex(int(int(operand1, 16) * int(operand2, 16)))

    elif operation == 'div':
        register_data = hex(int(int(operand1, 16) / int(operand2, 16)))

    elif operation == 'rem':
        register_data = hex(int(int(operand1, 16) % int(operand2, 16)))

    elif operation == 'addi':
        register_data = hex(int(int(operand1, 16) + int(operand2, 2)))

    elif operation == 'andi':
        register_data = hex(int(int(operand1, 16) & int(operand2, 2)))

    elif operation == 'ori':
        register_data = hex(int(int(operand1, 16) | int(operand2, 2)))

    elif operation == 'lb':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [True, 0, 'l']

    elif operation == 'lh':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [True, 1, 'l']

    elif operation == 'lw':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [True, 3, 'l']

    elif operation == 'jalr':
        register_data = hex(PC)
        PC = int(operand2, 2) + int(operand1, 16) - 4

    elif operation == 'sb':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [True, 0, 's']

    elif operation == 'sw':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [True, 3, 's']

    elif operation == 'sh':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [True, 1, 's']

    elif operation == 'beq':
        if operand1 == operand2:
            PC += int(imm, 2) - 4

    elif operation == 'bne':
        if operand1 != operand2:
            PC += int(imm, 2) - 4

    elif operation == 'bge':
        if operand2 >= operand1:
            PC += int(imm, 2) - 4

    elif operation == 'blt':
        if operand2 > operand1:
            PC += int(imm, 2) - 4

    elif operation == 'auipc':
        # (Add Upper Immediate to Program Counter): this sets rd to the sum of the current PC and a 32-bit value with the low 12 bits as 0 and the high 20 bits coming from the U-type immediate.
        curr_instruction_word = '0x' + MEM[PC + 3] + MEM[PC + 2] + MEM[PC + 1] + MEM[PC]
        register_data = hex(int(int(curr_instruction_word, 16) + int(imm, 2)))

    elif operation == 'lui':
        # lui (Load Upper Immediate): this sets rd to a 32-bit value with the low 12 bits being 0 and the high 20 bits coming from the U-type immediate.
        register_data = hex(int(imm, 2))

    elif operation == 'jal':
        register_data = '0x' + MEM[PC + 3] + MEM[PC + 2] + MEM[PC + 1] + MEM[PC]  # Storing next instruction
        updated_intruction_word = hex(int(imm, 2))
        MEM[PC + 3] = updated_intruction_word[2:4]
        MEM[PC + 2] = updated_intruction_word[4:6]
        MEM[PC + 1] = updated_intruction_word[6:8]
        MEM[PC] = updated_intruction_word[8:10]


# Performs the memory operations
def mem():
    if is_mem[0] == True:
        if is_mem[2] == 'l':
            register_data = '0x'
            for i in range(is_mem[1] + 1):
                register_data += MEM[memory_address + is_mem[1] - i]
        else:
            for i in range(is_mem[1] + 1):
                MEM[memory_address + is_mem[1] - i] = register_data[i:i + 2]


# Writes the results back to the register file
def write_back():
    if is_mem[0] == True:
        register_data = memory_element
    R[int(rd, 2)] = register_data


# Memory write
def write_word(address, instruction):
    idx = int(address[2:],16)
    MEM[idx] = instruction[8:10]
    MEM[idx + 1] = instruction[6:8]
    MEM[idx + 2] = instruction[4:6]
    MEM[idx + 3] = instruction[2:4]
