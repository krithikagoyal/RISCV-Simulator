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
import csv

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
offset = 0
register_data = '0x00000000'
memory_address = 0
# [-1/0/1(no memory operation/load/store), type of load/store if any]
is_mem = [-1, -1]
write_back_signal = False


# run_RISCVsim function
def run_RISCVsim():
    global clock
    while(1):
        fetch()
        decode()
        execute()
        mem()
        write_back()
        clock += 1
        print("Number of clock cycles: ", clock, '\n')


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
        print("Error opening input .mc file.\n")
        exit(1)


# Creates a "data_out.mc" file and writes the data memory in it.
def write_data_memory():
    try:
        fp = open("data_out.mc", "w")
        out_tmp = []
        for i in range(268435456, 268468221, 4):
            out_tmp.append(
                hex(i) + ' 0x' + MEM[i + 3] + MEM[i + 2] + MEM[i + 1] + MEM[i] + '\n')
        fp.writelines(out_tmp)
        fp.close()
    except:
        print("Error opening data_out.mc file for writing.\n")


# It is called to end the program and write the updated data memory in "data_out.mc" file
def swi_exit():
    write_data_memory()
    # for i in range(32):
    #     print(R[i])
    exit(0)


# Reads from the instruction memory and updates the instruction register
def fetch():
    global PC, instruction_word
    instruction_word = '0x' + MEM[PC + 3] + MEM[PC + 2] + MEM[PC + 1] + MEM[PC]
    print("FETCH: Fetch instruction", instruction_word, "from address", hex(PC))
    PC += 4


# Decodes the instruction and decides the operation to be performed in the execute stage; reads the operands from the register file.
def decode():
    if instruction_word == '0x401010BB':
        swi_exit()

    bin_instruction = bin(int(instruction_word[2:], 16))[2:]
    bin_instruction = (32 - len(bin_instruction)) * '0' + bin_instruction

    opcode = int(bin_instruction[25:32], 2)
    func3 = int(bin_instruction[17:20], 2)
    func7 = int(bin_instruction[0:7], 2)

    f = open('src/Instruction_Set_List.csv')
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

    # print(track)
    op_type = instruction_set_list[track][0]
    operation = instruction_set_list[track][1]

    is_mem = [-1, -1]

    if op_type == 'R':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        rd = bin_instruction[20:25]
        operand1 = R[int(rs1, 2)]
        operand2 = R[int(rs2, 2)]
        write_back_signal = True

    elif op_type == 'I':
        rs1 = bin_instruction[12:17]
        rd = bin_instruction[20:25]
        imm = bin_instruction[0:12]
        operand1 = R[int(rs1, 2)]
        operand2 = imm
        write_back_signal = True

    elif op_type == 'S':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        imm = bin_instruction[0:7] + bin_instruction[20:25]
        operand1 = R[int(rs1, 2)]
        operand2 = imm
        register_data = rs2
        write_back_signal = False

    elif op_type == 'SB':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        operand1 = R[int(rs1, 2)]
        operand2 = R[int(rs2, 2)]
        imm = bin_instruction[0] + bin_instruction[24] + \
            bin_instruction[1:7] + bin_instruction[20:24] + '0'
        offset = imm
        write_back_signal = False

    elif op_type == 'U':
        rd = bin_instruction[20:25]
        imm = bin_instruction[0:20] + '0'*12
        operand2 = imm
        write_back_signal = True

    elif op_type == 'UJ':
        rd = bin_instruction[20:25]
        imm = bin_instruction[0] + bin_instruction[12:20] + \
            bin_instruction[11] + bin_instruction[1:11] + '0'
        offset = imm
        write_back_signal = True

    else:
        print("Unidentifiable machine code!")
        swi_exit()


# Executes the ALU operation based on ALUop
def execute():
    global register_data

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
        # checking MSB
        if(operand1[2] == '1'){
            i = 2
            while(register_data[i] != 1){
                register_data[i] = 1
                i = i+1
            }
        }

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
        is_mem = [0, 0]

    elif operation == 'lh':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [0, 1]

    elif operation == 'lw':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [0, 3]

    elif operation == 'jalr':
        register_data = hex(PC)
        PC = int(operand2, 2) + int(operand1, 16) - 4

    elif operation == 'sb':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [1, 0]

    elif operation == 'sh':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [1, 1]

    elif operation == 'sw':
        memory_address = int(int(operand1, 16) + int(operand2, 2))
        is_mem = [1, 3]

    elif operation == 'beq':
        if operand1 == operand2:
            PC += int(offset, 2) - 4

    elif operation == 'bne':
        if operand1 != operand2:
            PC += int(offset, 2) - 4

    elif operation == 'bge':
        if operand2 >= operand1:
            PC += int(offest, 2) - 4

    elif operation == 'blt':
        if operand2 > operand1:
            PC += int(offset, 2) - 4

    elif operation == 'auipc':
        register_data = hex(int(PC + int(operand2, 2)))

    elif operation == 'lui':
        register_data = hex(int(operand2, 2))

    elif operation == 'jal':
        register_data = hex(PC)
        PC += int(offset, 2) - 4

    register_data = (34 - len(register_data)) * '0' + register_data[2:]


# Performs the memory operations
def mem():
    if is_mem[0] == -1:
        print("No memory operation.")

    elif is_mem[0] == 0:
        register_data = '0x'
        for i in range(3 - is_mem[1]):
            register_data += '00'
        for i in range(is_mem[1] + 1):
            register_data += MEM[memory_address + is_mem[1] - i]

    else:
        if is_mem[1] >= 3:
            MEM[memory_address + 3] = register_data[0:2]
            MEM[memory_address + 2] = register_data[2:4]
        if is_mem[1] >= 1:
            MEM[memory_address + 1] = register_data[4:6]
        if is_mem[1] >= 0:
            MEM[memory_address] = register_data[6:8]


# Writes the results back to the register file
def write_back():
    if write_back_signal == True:
        R[int(rd, 2)] = register_data

    else:
        print("No write-back operation.")


# Memory write
def write_word(address, instruction):
    idx = int(address[2:], 16)
    MEM[idx] = instruction[8:10]
    MEM[idx + 1] = instruction[6:8]
    MEM[idx + 2] = instruction[4:6]
    MEM[idx + 3] = instruction[2:4]
