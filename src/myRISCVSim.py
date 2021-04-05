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
from sys import exit
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
is_mem = [-1, -1] # [-1/0/1(no memory operation/load/store), type of load/store if any]
write_back_signal = False


# Utility functions
def nhex(num):
    if num < 0:
        num += 2**32
    return hex(num)

def nint(s, base, bits=32):
    num = int(s, base)
    if num >= 2**(bits-1):
        num -= 2**bits
    return num

def sign_extend(data):
    if data[2] == '8' or data[2] == '9' or data[2] == 'a' or data[2] == 'b' or data[2] == 'c' or data[2] == 'd' or data[2] == 'e' or data[2] == 'f':
        data = data[:2] + (10 - len(data)) * 'f' + data[2:]
    else:
        data = data[:2] + (10 - len(data)) * '0' + data[2:]
    return data


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
    exit(0)


# Reads from the instruction memory and updates the instruction register
def fetch():
    global PC, instruction_word

    instruction_word = '0x' + MEM[PC + 3] + MEM[PC + 2] + MEM[PC + 1] + MEM[PC]
    print("FETCH: Fetch instruction", instruction_word, "from address", nhex(PC))
    PC += 4


# Decodes the instruction and decides the operation to be performed in the execute stage; reads the operands from the register file.
def decode():
    global operation, operand1, operand2, instruction_word, rd, offset, register_data, memory_address, write_back_signal, PC, is_mem, MEM, R

    if instruction_word == '0x401010BB' or instruction_word == '0x00000000':
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

    if match_found == False:
        print("Unidentifiable machine code!")
        swi_exit()

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
        register_data = R[int(rs2, 2)]
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
    global operation, operand1, operand2, instruction_word, rd, offset, register_data, memory_address, write_back_signal, PC, is_mem, MEM, R

    if operation == 'add':
        register_data = nhex(int(nint(operand1, 16) + nint(operand2, 16)))

    elif operation == 'sub':
        register_data = nhex(int(nint(operand1, 16) - nint(operand2, 16)))

    elif operation == 'and':
        register_data = nhex(int(int(operand1, 16) & int(operand2, 16)))

    elif operation == 'or':
        register_data = nhex(int(int(operand1, 16) | int(operand2, 16)))

    elif operation == 'sll':
        if(nint(operand2, 16) < 0):
            print("ERROR IN SLL\n")
            swi_exit()
        else:
            register_data = nhex(int(int(operand1, 16) << int(operand2, 16)))

    elif operation == 'slt':
        if (nint(operand1, 16) < nint(operand2, 16)):
            register_data = hex(1)
        else:
            register_data = hex(0)

    elif operation == 'sra':
        if(nint(operand2, 16) < 0):
            print("ERROR IN SRA\n")
            swi_exit()
        else:
            register_data = hex(int(int(operand1, 16) >> int(operand2, 16)))
            if operand1[2] == '8' or operand1[2] == '9' or operand1[2] == 'a' or operand1[2] == 'b' or operand1[2] == 'c' or operand1[2] == 'd' or operand1[2] == 'e' or operand1[2] == 'f':
                i = 2
                while register_data[i] != '8' and register_data[i] != '9' and register_data[i] != 'a' and register_data[i] != 'b' and register_data[i] != 'c' and register_data[i] != 'd' and register_data[i] != 'e' and register_data[i] != 'f':
                    register_data[i] = 1
                    i = i + 1

    elif operation == 'srl':
        if(nint(operand2, 16) < 0):
            print("ERROR IN SRL\n")
            swi_exit()
        else:
            register_data = nhex(int(operand1, 16) >> int(operand2, 16))

    elif operation == 'xor':
        register_data = nhex(int(int(operand1, 16) ^ int(operand2, 16)))

    elif operation == 'mul':
        register_data = nhex(int(nint(operand1, 16) * nint(operand2, 16)))

    elif operation == 'div':
        if nint(operand2, 16) == 0:
            print("ERROR: Division by zero!")
            swi_exit()
        else:
            register_data = nhex(int(nint(operand1, 16) / nint(operand2, 16)))

    elif operation == 'rem':
        register_data = nhex(int(nint(operand1, 16) % nint(operand2, 16)))

    elif operation == 'addi':
        register_data = nhex(
            int(nint(operand1, 16) + nint(operand2, 2, len(operand2))))

    elif operation == 'andi':
        register_data = nhex(int(int(operand1, 16) & int(operand2, 2)))

    elif operation == 'ori':
        register_data = nhex(int(int(operand1, 16) | int(operand2, 2)))

    elif operation == 'lb':
        memory_address = int(int(operand1, 16) + nint(operand2, 2, len(operand2)))
        is_mem = [0, 0]

    elif operation == 'lh':
        memory_address = int(int(operand1, 16) + nint(operand2, 2, len(operand2)))
        is_mem = [0, 1]

    elif operation == 'lw':
        memory_address = int(int(operand1, 16) + nint(operand2, 2, len(operand2)))
        is_mem = [0, 3]

    elif operation == 'jalr':
        register_data = nhex(PC)
        PC = nint(operand2, 2, len(operand2)) + nint(operand1, 16)

    elif operation == 'sb':
        memory_address = int(int(operand1, 16) + nint(operand2, 2, len(operand2)))
        is_mem = [1, 0]

    elif operation == 'sh':
        memory_address = int(int(operand1, 16) + nint(operand2, 2, len(operand2)))
        is_mem = [1, 1]

    elif operation == 'sw':
        memory_address = int(int(operand1, 16) + nint(operand2, 2, len(operand2)))
        is_mem = [1, 3]

    elif operation == 'beq':
        if nint(operand1, 16) == nint(operand2, 16):
            PC += nint(offset, 2, len(offset)) - 4

    elif operation == 'bne':
        if nint(operand1, 16) != nint(operand2, 16):
            PC += nint(offset, 2, len(offset)) - 4

    elif operation == 'bge':
        if nint(operand1, 16) >= nint(operand2, 16):
            PC += nint(offset, 2, len(offset)) - 4

    elif operation == 'blt':
        if nint(operand1, 16) < nint(operand2, 16):
            PC += nint(offset, 2, len(offset)) - 4

    elif operation == 'auipc':
        register_data = nhex(int(PC + int(operand2, 2)))

    elif operation == 'lui':
        register_data = nhex(int(operand2, 2))

    elif operation == 'jal':
        register_data = nhex(PC)
        PC += nint(offset, 2, len(offset)) - 4

    register_data = register_data[:2] + \
        (10 - len(register_data)) * '0' + register_data[2:]


# Performs the memory operations
def mem():
    global operation, operand1, operand2, instruction_word, rd, offset, register_data, memory_address, write_back_signal, PC, is_mem, MEM, R

    if is_mem[0] == -1:
        print("No memory operation.")

    elif is_mem[0] == 0:
        register_data = '0x'
        if is_mem[1] == 0:
            register_data += MEM[memory_address]
        elif is_mem[1] == 1:
            register_data += (MEM[memory_address + 1] + MEM[memory_address])
        else:
            register_data += (MEM[memory_address + 3] + MEM[memory_address + 2] + MEM[memory_address + 1] + MEM[memory_address])

        register_data = sign_extend(register_data)

    else:
        if is_mem[1] >= 3:
            MEM[memory_address + 3] = register_data[2:4]
            MEM[memory_address + 2] = register_data[4:6]
        if is_mem[1] >= 1:
            MEM[memory_address + 1] = register_data[6:8]
        if is_mem[1] >= 0:
            MEM[memory_address] = register_data[8:10]


# Writes the results back to the register file
def write_back():
    if write_back_signal == True:
        if int(rd, 2) != 0:
            R[int(rd, 2)] = register_data
        else:
            print("WRITEBACK: No change in R0")

    else:
        print("No write-back operation.")


# Memory write
def write_word(address, instruction):
    idx = int(address[2:], 16)
    MEM[idx] = instruction[8:10]
    MEM[idx + 1] = instruction[6:8]
    MEM[idx + 2] = instruction[4:6]
    MEM[idx + 3] = instruction[2:4]
