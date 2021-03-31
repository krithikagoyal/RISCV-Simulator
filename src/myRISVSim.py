"""
The project is developed as part of Computer Architecture class.
Project Name: Functional Simulator for subset of RISCV Processor

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
from collections import defaultdict
# myRISCVSim.py
# Purpose of this file: Implementation file for myRISCVSim

# Register file
R = [0]*32

# Flags
N = C = V = Z = clock = 0

# Program Counter
PC = 0

# Memory
MEM = defaultdict(lambda: '00')

# Intermediate datapath and control path signals
instruction_word = 0
operand1 = 0
operand2 = 0


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
# Reset all registers and memory content to 0
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
    for i in range(1000,4):
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


# Reads the instruction register, operand1 and operand2 from register file; decides the operation to be performed in execute stage
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

    if op_type == 'R':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        rd = bin_instruction[20:25]
        operand1 = R[int(rs1,2)]
        operand2 = R[int(rs2,2)]

    elif op_type == 'I':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        imm = bin_instruction[0:7] + bin_instruction[20:25]
        operand1 = R[int(rs1,2)]
        operand2 = (imm)

    elif op_type == 'S':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        imm = bin_instruction[0:7] + bin_instruction[20:25]

    elif op_type == 'B':
        rs2 = bin_instruction[7:12]
        rs1 = bin_instruction[12:17]
        imm = bin_instruction[0] + bin_instruction[24] + bin_instruction[1:7] + bin_instruction[20:24] + '0'

    elif op_type == 'U':
        rd = bin_instruction[20:25]
        imm = bin_instruction[0:20] + '0'*12

    elif op_type == 'J':
        rd = bin_instruction[20:25]
        imm = bin_instruction[0] + bin_instruction[12:20] + bin_instruction[11] + bin_instruction[1:11] + '0'

    else:
        print("Unidentifiable machine code!")
        swi_exit()


# Executes the ALU operation based on ALUop
def execute():
    if operation == 'add':
        R[int(rd,2)] = hex(int(int(operand1,16) + int(operand2,16)))

    elif operation == 'sub':
        R[int(rd,2)] = hex(int(int(operand1,16) - int(operand2,16)))

    elif operation == 'and':
        R[int(rd,2)] = hex(int(int(operand1,16) & int(operand2,16)))

    elif operation == 'or':
        R[int(rd,2)] = hex(int(int(operand1,16) | int(operand2,16)))

    elif operation == 'sll':
        R[int(rd,2)] = hex(int(int(operand1,16) << int(operand2,16)))

    elif operation == 'slt':
        if (int(operand1,16) < int(operand2,16)):
            R[int(rd,2)] = hex(1)
        else:
            R[int(rd,2)] = hex(0)

    elif operation == 'sra':
        R[int(rd,2)] = hex(int(int(operand1,16) >> int(operand2,16)))

    elif operation == 'srl':
        R[int(rd,2)] = hex(int(operand1,16) >> int(operand2,16))

    elif operation == 'xor':
        R[int(rd,2)] = hex(int(int(operand1,16) ^ int(operand2,16)))

    elif operation == 'mul':
        R[int(rd, 2)] = hex(int(int(operand1,16) * int(operand2,16)))

    elif operation == 'div':
        R[int(rd, 2)] = hex(int(int(operand1,16) / int(operand2,16)))

    elif operation == 'rem':
        R[int(rd, 2)] = hex(int(int(operand1,16) % int(operand2,16)))

    elif operation == 'addi':
        R[int(rs1,2)] = hex(int(int(operand1,16) + int(operand2,2)))

    elif operation == 'andi':
        R[int(rs1, 2)] = hex(int(int(operand1,16) & int(operand2,2)))

    elif operation == 'ori':
        R[int(rs1, 2)] = hex(int(int(operand1,16) | int(operand2,2)))

    elif operation == 'lb':
        base = R[int(rs1, 2)]
        offset = imm
        memory_element = MEM[int(int(base, 16) + int(offset, 2))]
        R[int(rd, 2)] = '0x' + memory_element

    elif operation == 'lh':
        base = R[int(rs1, 2)]
        offset = imm
        element_address = int(int(base, 16) + int(offset, 2))
        memory_element = MEM[element_address + 1] + MEM[element_address]
        R[int(rd, 2)] = '0x' + memory_element

    elif operation == 'lw':
        base = R[int(rs1, 2)]
        offset = imm
        element_address = int(int(base, 16) + int(offset, 2))
        memory_element = MEM[element_address + 3] + MEM[element_address + 2] + MEM[element_address + 1] + MEM[element_address]
        R[int(rd, 2)] = '0x' + memory_element

    elif operation == 'jalr':
        R[int(rs2, 0)] = hex(PC)
        PC = int(imm, 2) + int(R[int(rs1, 2)], 16) - 4

    elif operation == 'sb':
        base = R[int(rs1, 2)]
        offset = imm
        memory_address = int(int(base, 16) + int(offset, 2))
        MEM[memory_address] = R[int(rs2, 2)][8:10]        

    elif operation == 'sw':
        base = R[int(rs1, 2)]
        offset = imm
        memory_address = int(int(base, 16) + int(offset, 2))
        MEM[memory_address] = R[int(rs2, 2)][8:10]
        MEM[memory_address + 1] = R[int(rs2, 2)][6:8]
        MEM[memory_address + 2] = R[int(rs2, 2)][4:6]
        MEM[memory_address + 3] = R[int(rs2, 2)][2:4]

    elif operation == 'sh':
        base = R[int(rs1, 2)]
        offset = imm
        memory_address = int(int(base, 16) + int(offset, 2))
        MEM[memory_address] = R[int(rs2, 2)][8:10]
        MEM[memory_address + 1] = R[int(rs2, 2)][6:8]

    elif operation == 'beq':
        if R[int(rs1, 2)] == R[int(rs2, 2)]:
            PC += int(imm, 2) - 4

    elif operation == 'bne':
        if R[int(rs1, 2)] != R[int(rs2, 2)]:
            PC += int(imm, 2) - 4

    elif operation == 'bge':
        if R[int(rs2, 2)] >= R[int(rs1, 2)]:
            PC += int(imm, 2) - 4

    elif operation == 'blt':
        if R[int(rs2, 2)] > R[int(rs1, 2)]:
            PC += int(imm, 2) - 4

    elif operation == 'auipc':

    elif operation == 'lui':

    elif operation == 'jal':


# Performs the memory operations
def mem():


# Writes the results back to the register file
def write_back():


# Memory write
def write_word(address, instruction):
  idx = int(address[2:],16)
  MEM[idx] = instruction[8:10]
  MEM[idx + 1] = instruction[6:8]
  MEM[idx + 2] = instruction[4:6]
  MEM[idx + 3] = instruction[2:4]
