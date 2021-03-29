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
  elif op_type == 'I':
    rs2 = bin_instruction[7:12]
    rs1 = bin_instruction[12:17]
    imm = bin_instruction[0:7] + bin_instruction[20:25]
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
  # akhil and rhythm, use variables imm, rs1, rs2, rd, operation they are predefined. Now execute
  # doing 4 for example
  if operation == 'add':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 + operand2
  else if operation == 'sub':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 - operand2
  else if operation == 'and':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 & operand2
  else if operation == 'or':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 | operand2
  else if operation == 'sll':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1<<operand2
  else if operation == 'slt':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    if (operand1<operand2):
        R[int(rd,2)] = 1
    else:
        R[int(rd,2)] = 0
  else if operation == 'sra':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 >> operand2
  else if operation == 'xor':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 ^ operand2 
  else if operation == 'mul':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 * operand2
  else if operation == 'div':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 / operand2
  else if operation == 'rem':
    operand1 = R[int(rs1,2)]
    operand2 = R[int(rs2,2)]
    R[int(rd,2)] = operand1 % operand2
   
   
   

# Performs the memory operations
def mem():


# Writes the results back to the register file
def write_back():


# Memory write
def write_word(address, instruction):
  idx = int(address[2:],16)
  MEM[idx] = instruction
