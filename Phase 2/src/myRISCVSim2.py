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
# Purpose of this file: This file contains all the classes and functions used for the simulator.

from collections import defaultdict
from sys import exit
import csv


# Instruction/State Class
class State:
	def __init__(self, pc = 0):
		self.reset_interRegisters()
		self.PC = pc
        self.next_PC = 0

	def reset_interRegisters(self):
        self.instruction_word = 0
        self.operand1 = 0
        self.operand2 = 0
        self.rd = 0
        self.offset = 0
        self.alu_control_signal = -1
        self.is_mem = is_mem = [-1, -1] # [-1/0/1(no memory operation/load/store), type of load/store if any]
        self.memory_address = 0
        self.write_back_signal = False
        self.register_data = '0x00000000'
        #
        self.inc_select = 0
        self.pc_select = 0
        self.return_address = -1
        self.pc_offset = 0
        #
        self.is_dummy = False
        self.stage = 0
        self.pc_update = -1
        self.branch_taken = False
        self.is_control = False

# terminate = False


# Brach table buffer
class BTB:
	table = {}

	def find(self, pc):
		if pc in self.table.keys():
			return True
		return False

	def enter(self, pc, to_take_address):
		self.table[pc] = [False, to_take_address]

	def predict(self, pc):
		return self.table[pc][0]

	def getTarget(self, pc):
		return self.table[pc][1]

	def changeprediction(self, pc):
		self.table[pc][0] = not self.table[pc][0]


# Processor
class Processor:
	def __init__(self, file_name):
		self.MEM = defaultdict(lambda: '00')
		self.R = ['0x00000000' for i in range(32)]
		self.R[2]='0x7FFFFFF0'
		self.R[3]='0x10000000'
		self.load_program_memory(file_name)
		# Various Counts
        self.count_total_inst = 0
        self.count_mem_inst = 0
        self.count_control_inst = 0

    # Utility Functions
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
            print("ERROR: Error opening input .mc file\n")
            exit(1)

    # Memory write
    def write_word(self, address, instruction):
        idx = int(address[2:], 16)
        MEM[idx] =  instruction[8:10]
        MEM[idx + 1] = instruction[6:8]
        MEM[idx + 2] = instruction[4:6]
        MEM[idx + 3] = instruction[2:4]

    # Creates a "data_out.mc" file and writes the data memory in it. It also creates
    # a reg_out.mc file and writes the contents of registers in it.
    def write_data_memory(self):
        try:
            fp = open("data_out.mc", "w")
            out_tmp = []
            for i in range(268435456, 268468221, 4):
                out_tmp.append(
                    hex(i) + ' 0x' + MEM[i + 3] + MEM[i + 2] + MEM[i + 1] + MEM[i] + '\n')
            fp.writelines(out_tmp)
            fp.close()
        except:
            print("ERROR: Error opening data_out.mc file for writing\n")

        try:
            fp = open("reg_out.mc", "w")
            out_tmp = []
            for i in range(32):
                out_tmp.append('x' + str(i) + ' ' + R[i] + '\n')
            fp.writelines(out_tmp)
            fp.close()
        except:
            print("ERROR: Error opening reg_out.mc file for writing\n")

    # Reads from the instruction memory and updates the instruction register
    def fetch(self, pipelining_enabled, state, btb):
        state.stage += 1
        if pipelining_enabled:
            state.instruction_word = '0x' + MEM[state.PC + 3] + MEM[state.PC + 2] + MEM[state.PC + 1] + MEM[state.PC]
        else:
            if state.is_dummy:
                return
            else:
                state.instruction_word = '0x' + MEM[state.PC + 3] + MEM[state.PC + 2] + MEM[state.PC + 1] + MEM[state.PC]
                if btb.find(state.PC):
                    self.is_control = True
                    state.branch_taken = btb.predict(state.PC)
                    state.pc_update = btb.predict(state.PC)

    # Executes the ALU operation based on ALUop
    def execute(pipelining_enabled, state):
        state.stage += 1
        if state.is_dummy:
            return True

        if state.alu_control_signal == 2:
            state.register_data = nhex(int(nint(state.operand1, 16) + nint(state.operand2, 16)))

        elif state.alu_control_signal == 8:
            state.register_data = nhex(int(nint(state.operand1, 16) - nint(state.operand2, 16)))

        elif state.alu_control_signal == 1:
            state.register_data = nhex(int(int(state.operand1, 16) & int(state.operand2, 16)))

        elif state.alu_control_signal == 3:
            state.register_data = nhex(int(int(state.operand1, 16) | int(state.operand2, 16)))

        elif state.alu_control_signal == 4:
            if(nint(state.operand2, 16) < 0):
                print("ERROR: Shift by negative!\n")
                exit(1)
            else:
                state.register_data = nhex(int(int(state.operand1, 16) << int(state.operand2, 16)))

        elif state.alu_control_signal == 5:
            if (nint(state.operand1, 16) < nint(state.operand2, 16)):
                state.register_data = hex(1)
            else:
                state.register_data = hex(0)

        elif state.alu_control_signal == 6:
            if(nint(state.operand2, 16) < 0):
                print("ERROR: Shift by negative!\n")
                exit(1)
            else:
                state.register_data = bin(int(int(state.operand1, 16) >> int(state.operand2, 16)))
                if state.operand1[2] == '8' or state.operand1[2] == '9' or state.operand1[2] == 'a' or state.operand1[2] == 'b' or state.operand1[2] == 'c' or state.operand1[2] == 'd' or state.operand1[2] == 'e' or state.operand1[2] == 'f':
                    state.register_data = '0b' + (34 - len(state.register_data)) * '1' + state.register_data[2:]
                state.register_data = hex(int(state.register_data, 2))

        elif state.alu_control_signal == 7:
            if(nint(state.operand2, 16) < 0):
                print("ERROR: Shift by negative!\n")
                exit(1)
            else:
                state.register_data = nhex(int(state.operand1, 16) >> int(state.operand2, 16))

        elif state.alu_control_signal == 9:
            state.register_data = nhex(int(int(state.operand1, 16) ^ int(state.operand2, 16)))

        elif state.alu_control_signal == 10:
            state.register_data = nhex(int(nint(state.operand1, 16) * nint(state.operand2, 16)))

        elif state.alu_control_signal == 11:
            if nint(state.operand2, 16) == 0:
                print("ERROR: Division by zero!\n")
                exit(1)
            else:
                state.register_data = nhex(int(nint(state.operand1, 16) / nint(state.operand2, 16)))

        elif state.alu_control_signal == 12:
            state.register_data = nhex(int(nint(state.operand1, 16) % nint(state.operand2, 16)))

        elif state.alu_control_signal == 14:
            state.register_data = nhex(
                int(nint(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2))))

        elif state.alu_control_signal == 13:
            state.register_data = nhex(int(int(state.operand1, 16) & int(state.operand2, 2)))

        elif state.alu_control_signal == 15:
            state.register_data = nhex(int(int(state.operand1, 16) | int(state.operand2, 2)))

        elif state.alu_control_signal == 16:
            state.memory_address = int(int(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2)))
            state.is_mem = [0, 0]

        elif state.alu_control_signal == 17:
            state.memory_address = int(int(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2)))
            state.is_mem = [0, 1]

        elif state.alu_control_signal == 18:
            state.memory_address = int(int(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2)))
            state.is_mem = [0, 3]

        elif state.alu_control_signal == 19: # Jalr
            state.register_data = nhex(state.PC + 4)
            if pipelining_enabled:
                return
            state.return_address = nint(state.operand2, 2, len(state.operand2)) + nint(state.operand1, 16)
            state.pc_select = 1

        elif state.alu_control_signal == 20:
            state.memory_address = int(int(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2)))
            state.is_mem = [1, 0]

        elif state.alu_control_signal == 22:
            state.memory_address = int(int(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2)))
            state.is_mem = [1, 1]

        elif state.alu_control_signal == 21:
            state.memory_address = int(int(state.operand1, 16) + nint(state.operand2, 2, len(state.operand2)))
            state.is_mem = [1, 3]

        elif state.alu_control_signal == 23:
            if pipelining_enabled:
                return
            if nint(state.operand1, 16) == nint(state.operand2, 16):
                state.pc_offset = nint(state.offset, 2, len(state.offset))
                state.inc_select = 1

        elif state.alu_control_signal == 24:
            if pipelining_enabled:
                return
            if nint(state.operand1, 16) != nint(state.operand2, 16):
                state.pc_offset = nint(state.offset, 2, len(state.offset))
                state.inc_select = 1

        elif state.alu_control_signal == 25:
            if pipelining_enabled:
                return
            if nint(state.operand1, 16) >= nint(state.operand2, 16):
                state.pc_offset = nint(state.offset, 2,  len(state.offset))
                state.inc_select = 1

        elif state.alu_control_signal == 26:
            if pipelining_enabled:
                return
            if nint(state.operand1, 16) < nint(state.operand2, 16):
                state.pc_offset =  nint(state.offset, 2, len(state.offset))
                state.inc_select = 1

        elif state.alu_control_signal == 27:
            state.register_data = nhex(int(state.PC + 4 + int(state.operand2, 2)))

        elif state.alu_control_signal == 28:
            state.register_data = nhex(int(state.operand2, 2))

        elif state.alu_control_signal == 29: # Jal
            state.register_data = nhex(state.PC + 4)
            if pipelining_enabled:
                return
            state.pc_offset = nint(state.offset, 2, len(state.offset))
            state.inc_select = 1

        if len(state.register_data) > 10:
            state.register_data = state.register_data[:2] + state.register_data[-8:]

        state.register_data = state.register_data[:2] + \
            (10 - len(state.register_data)) * '0' + state.register_data[2::]

    # Performs the memory operations and also performs the operations of IAG.
    def mem(self, state):
        state.stage += 1
        if state.is_dummy:
            return

        if state.is_mem[0] == -1:
            return

        elif state.is_mem[0] == 0:
            state.register_data = '0x'
            if state.is_mem[1] == 0:
                state.register_data += MEM[state.memory_address]
            elif is_mem[1] == 1:
                state.register_data += (MEM[state.memory_address + 1] + MEM[state.memory_address])
            else:
                state.register_data += (MEM[state.memory_address + 3] + MEM[state.memory_address + 2] + MEM[state.memory_address + 1] + MEM[state.memory_address])

            state.register_data = sign_extend(state.register_data)

        else:
            if state.is_mem[1] >= 3:
                MEM[state.memory_address + 3] = state.register_data[2:4]
                MEM[state.memory_address + 2] = state.register_data[4:6]
            if is_mem[1] >= 1:
                MEM[state.memory_address + 1] = state.register_data[6:8]
            if is_mem[1] >= 0:
                MEM[state.memory_address] = state.register_data[8:10]

        if pipelining_enabled:
            return

        if state.pc_select:
            state.next_PC = state.return_address
        elif state.inc_select:
            state.next_PC += state.pc_offset
        else:
            state.next_PC += 4

    # Writes the results back to the register file
    def write_back(self, state):
        state.stage += 1
        if not state.is_dummy:
            state.stage += 1
            if state.write_back_signal:
                if int(state.rd, 2) != 0:
                    R[int(state.rd, 2)] = state.register_data


# How terminate program for non-pipelined version.
# swi_exit()? Terminate?
# Add decode part, When are we entering in BTB?, How handle jal and jalr?
# Returns...what required? Return states also
