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
static unsigned char MEM[4000];
MEM = ['']*4000

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
void reset_proc() {

}

#load_program_memory reads the input memory, and pupulates the instruction 
# memory
void load_program_memory(char *file_name) {
  FILE *fp;
  unsigned int address, instruction;
  fp = fopen(file_name, "r");
  if(fp == NULL) {
    printf("Error opening input mem file\n");
    exit(1);
  }
  while(fscanf(fp, "%x %x", &address, &instruction) != EOF) {
    write_word(MEM, address, instruction);
  }
  fclose(fp);
}

#writes the data memory in "data_out.mem" file
void write_data_memory() {
  FILE *fp;
  unsigned int i;
  fp = fopen("data_out.mem", "w");
  if(fp == NULL) {
    printf("Error opening dataout.mem file for writing\n");
    return;
  }
  
  for(i=0; i < 4000; i = i+4){
    fprintf(fp, "%x %x\n", i, read_word(MEM, i));
  }
  fclose(fp);
}

#should be called when instruction is swi_exit
void swi_exit() {
  write_data_memory();
  exit(0);
}


#reads from the instruction memory and updates the instruction register
def fetch() {
}
#reads the instruction register, reads operand1, operand2 fromo register file, decides the operation to be performed in execute stage
def decode() {
}
#executes the ALU operation based on ALUop
def execute() {
}
#perform the memory operation
def mem() {
}
#writes the results back to register file
def write_back() {
}


int read_word(char *mem, unsigned int address) {
  int *data;
  data =  (int*) (mem + address);
  return *data;
}

void write_word(char *mem, unsigned int address, unsigned int data) {
  int *data_p;
  data_p = (int*) (mem + address);
  *data_p = data;
}
