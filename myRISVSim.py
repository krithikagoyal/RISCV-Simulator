# The project is developed as part of Computer Architecture class
# Project Name: Functional Simulator for subset of RISCV Processor

# Developer's Name:
# Developer's Email id:
# Date: 


# myRISCVSim.cpp
# Purpose of this file: implementation file for myRISCVSim

#include "myRISCVSim.h"
#include <stdlib.h>
#include <stdio.h>
from myRISCVSim import *


# Register file
R = [0]*32

# flags
N = C = V = Z = 0

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
        if MEM[i/4] != 'untouched':
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

#reads the instruction register, reads operand1, operand2 fromo register file, decides the operation to be performed in execute stage
def decode():

#executes the ALU operation based on ALUop
def execute():

#perform the memory operation
def mem():

#writes the results back to register file
def write_back():



def write_word(address, instruction) {
  idx = int(address[2:],16)
  MEM[idx] = instruction
}
