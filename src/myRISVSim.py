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

# myRISCVSim.py
# Purpose of this file: Implementation file for myRISCVSim

# Register file
R = [0]*32

# Flags
N = C = V = Z = 0

# Program Counter
PC = 0

# Memory
MEM = ['NAN']*1000

# Intermediate datapath and control path signals
instruction_word = 0
int operand1 = 0
int operand2 = 0


# run_RISCVsim function
def run_RISCVsim():
    while(1):
        fetch()
        decode()
        execute()
        mem()
        write_back()


# It is used to set the reset values
# Reset all registers and memory content to 0
def reset_proc():
  for i in range(32):
    R[i] = '0x00000000'
  R[2] = '0x7FFFFFF0'
  R[3] = '0x10000000'


# load_program_memory reads the input memory, and populates the instruction memory
def load_program_memory(string file_name):
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


# Writes the data memory in "data_out.mem" file
def write_data_memory():
  try:
    fp = open("data_out.mem", "w")
    out_tmp = []
    for i in range(4000,4):
        if MEM[i/4] != 'NAN':
            out_tmp.append(hex(i) + ' ' + MEM[i/4])
    fp.writelines(out_tmp)
    fp.close()
  except:
    print("Error opening dataout.mem file for writing.\n")


# It should be called when instruction is swi_exit
def swi_exit():
  write_data_memory()
  exit(0)


# Reads from the instruction memory and updates the instruction register
def fetch():
  instruction_word = MEM[PC/4]
  PC += 4


# Reads the instruction register, operand1 and operand2 from register file; decides the operation to be performed in execute stage
def decode():
  #0110111-> LUI
  #0010111-> AUIPC
  #1101111-> JAL
  #1100111-> JALR
  #1100011-> BEQ(f3 = 000) BNE(f3 = 001) BLT(f3 = 100) BGE(f3 = 101)
  #0000011-> LB(f3 = 000) LH(f3 = 001) LW(f3 = 010)
  #0100011-> SB(f3 = 000) SH(f3 = 001) SW(f3 = 010)
  #0010011-> ORI(f3 = 110) ANDI(f3 = 111)
  #0110011->(f7 = 0)[SLL]
#executes the ALU operation based on ALUop

def execute():


# Performs the memory operations
def mem():


# Writes the results back to the register file
def write_back():


# Memory write
def write_word(address, instruction):
  idx = int(address[2:],16)
  MEM[idx] = instruction
