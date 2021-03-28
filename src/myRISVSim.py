# The project is developed as part of Computer Architecture class
# Project Name: Functional Simulator for subset of RISCV Processor

# Developer's Name:
# Developer's Email id:
# Date: 


# myRISCVSim.cpp
# Purpose of this file: implementation file for myRISCVSim

# Register file
R = [0]*32

# flags
N = C = V = Z = 0

#Program Counter
PC = 0

# memory
# static unsigned char MEM[4000];
MEM = ['NAN']*1000

# intermediate datapath and control path signals
instruction_word = 0
int operand1 = 0
int operand2 = 0


def run_RISCVsim():
    while(1):
        fetch()
        decode()
        execute()
        mem()
        write_back()


# it is used to set the reset values
#reset all registers and memory content to 0
def reset_proc():
  for i in range(32):
    R[i] = '0x00000000'
  R[2] = '0x7FFFFFF0'
  R[3] = '0x10000000'


#load_program_memory reads the input memory, and pupulates the instruction 
# memory
def load_program_memory(string file_name):
  #address, instruction;
  try:
    fp = open(file_name, 'r')
    for line in fp:
        tmp = line.split()
        if len(tmp) == 2:
            address, instruction = tmp[0], tmp[1]
            write_word(address, instruction)
    fp.close()
  except:
    print("Error opening input mem file\n")
    exit(1)


#writes the data memory in "data_out.mem" file
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
    print("Error opening dataout.mem file for writing\n")



#should be called when instruction is swi_exit
def swi_exit():
  write_data_memory()
  exit(0)



#reads from the instruction memory and updates the instruction register
def fetch():
  instruction_word = MEM[PC/4]
  PC += 4

#reads the instruction register, reads operand1, operand2 from register file, decides the operation to be performed in execute stage
def decode():
  bin_instruction = bin(int(instruction_word,16))[2:]
  '''
  Krithika code here to identify operation and optype,
  and fill the operand1 and operand2 global variables (whereable applicable)
  '''
  instruction = (32 - len(bin_instruction)) * '0' + bin_instruction
  opcode = int(instruction[25:32], 2)
  func3 = int(instruction[17:20], 2)
  func7 = int(instruction[0:7], 2)
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
  if op_type == 'R':
    rs2 = bin_instruction[7:12]
    rs1 = bin_instruction[12:17]
    rd = bin_instruction[]

#executes the ALU operation based on ALUop
def execute():

#perform the memory operation
def mem():

#writes the results back to register file
def write_back():



def write_word(address, instruction):
  idx = int(address[2:],16)
  MEM[idx] = instruction

