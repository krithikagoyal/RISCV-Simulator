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
import os
import csv

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


# Instruction/State Class
class State:
	def __init__(self, pc = 0):
		self.reset_interRegisters()
		self.PC = pc

	def reset_interRegisters(self):
		self.instruction_word = 0
		self.rs1 = -1
		self.rs2 = -1
		self.operand1 = 0
		self.operand2 = 0
		self.rd = -1
		self.offset = 0
		self.register_data = '0x00000000'
		self.memory_address = 0
		self.alu_control_signal = -1
		self.is_mem = is_mem = [-1, -1] # [-1/0/1(no memory operation/load/store), type of load/store if any]
		self.write_back_signal = False
		#
		self.is_dummy = False
		self.stage = 0
		self.pc_update = -1
		self.branch_taken = False
		self.inc_select = 0
		self.pc_select = 0
		self.next_pc = -1
		self.pc_offset = 0

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

# Processor
class Processor:
	def __init__(self, file_name):
		self.MEM = defaultdict(lambda: '00')
		self.R = ['0x00000000' for i in range(32)]
		self.R[2] = '0x7FFFFFF0'
		self.R[3] = '0x10000000'
		self.load_program_memory(file_name)
		self.pipelining_enabled = False
		self.terminate = False
		self.next_PC = 0
		# self.inc_select = 0
		# self.pc_select = 0
		self.return_address = -1
		self.pc_offset = 0
		# Various Counts
		self.count_total_inst = 0
		self.count_alu_inst = 0
		self.count_mem_inst = 0
		self.count_control_inst = 0
		self.all_dummy = False

	# load_program_memory reads the input memory, and populates the instruction memory
	def load_program_memory(self, file_name):
		try:
			fp = open(file_name, 'r')
			for line in fp:
				tmp = line.split()
				if len(tmp) == 2:
					address, instruction = tmp[0], tmp[1]
					self.write_word(address, instruction)
			fp.close()
		except:
			print("ERROR: Error opening input .mc file\n")
			exit(1)

	# Memory write
	def write_word(self, address, instruction):
		idx = int(address[2:], 16)
		self.MEM[idx] =  instruction[8:10]
		self.MEM[idx + 1] = instruction[6:8]
		self.MEM[idx + 2] = instruction[4:6]
		self.MEM[idx + 3] = instruction[2:4]

	# Creates a "data_out.mc" file and writes the data memory in it. It also creates
	# a reg_out.mc file and writes the contents of registers in it.
	def write_data_memory(self):
		try:
			fp = open("data_out.mc", "w")
			out_tmp = []
			for i in range(268435456, 268468221, 4):
				out_tmp.append(
					hex(i) + ' 0x' + self.MEM[i + 3] + self.MEM[i + 2] + self.MEM[i + 1] + self.MEM[i] + '\n')
			fp.writelines(out_tmp)
			fp.close()
		except:
			print("ERROR: Error opening data_out.mc file for writing\n")

		try:
			fp = open("reg_out.mc", "w")
			out_tmp = []
			for i in range(32):
				out_tmp.append('x' + str(i) + ' ' + self.R[i] + '\n')
			fp.writelines(out_tmp)
			fp.close()
		except:
			print("ERROR: Error opening reg_out.mc file for writing\n")

	# Instruction address generator
	def IAG(self, state):
		if state.pc_select:
			self.next_PC = state.return_address
		elif state.inc_select:
			# print("Enter inc select")
			self.next_PC += state.pc_offset
		else:
			self.next_PC += 4

		state.pc_select = 0
		state.inc_select = 0

	# Reads from the instruction memory and updates the instruction register
	def fetch(self, state, *args):
		state.stage += 1

		if state.is_dummy:
			return state

		if self.all_dummy:
			state.is_dummy = True
			return state

		state.instruction_word = '0x' + self.MEM[state.PC + 3] + self.MEM[state.PC + 2] + self.MEM[state.PC + 1] + self.MEM[state.PC]
		print("FETCH: Fetch instruction", state.instruction_word, "from address", nhex(state.PC))
		if not self.pipelining_enabled:
			return
		
		bin_instruction = bin(int(state.instruction_word[2:], 16))[2:]
		bin_instruction = (32 - len(bin_instruction)) * '0' + bin_instruction
		opcode = int(bin_instruction[25:32], 2)
		if opcode == 23 or opcode == 55 or opcode == 111:
			pass
        
		#I format
		elif opcode == 3 or opcode == 19 or opcode == 103:
			state.rs1 = bin_instruction[12:17]
			state.rs2 = -1
            
		#R S SB format
		else:
			state.rs1 = bin_instruction[12:17]
			state.rs2 = bin_instruction[7:12]

		btb = args[0]
        
		if btb.find(state.PC):
			state.branch_taken = btb.predict(state.PC)
			state.next_pc = btb.getTarget(state.PC)

		return state

	# Decodes the instruction and decides the operation to be performed in the execute stage; reads the operands from the register file.
	def decode(self, state, *args):
		state.stage += 1
		if state.is_dummy:
			return False, 0, state

		if state.instruction_word == '0x401080BB':
			self.terminate = True
			self.all_dummy = True
			print("END PROGRAM\n")
			return False, 0, state

		bin_instruction = bin(int(state.instruction_word[2:], 16))[2:]
		bin_instruction = (32 - len(bin_instruction)) * '0' + bin_instruction

		opcode = int(bin_instruction[25:32], 2)
		func3 = int(bin_instruction[17:20], 2)
		func7 = int(bin_instruction[0:7], 2)

		path = os.path.dirname(__file__)
		f = open(os.path.join(path,'Instruction_Set_List.csv'))
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

		if not match_found:
			print("ERROR: Unidentifiable machine code!\n")
			self.all_dummy = True
			self.terminate = True
			return False, 0, state

		op_type = instruction_set_list[track][0]
		operation = instruction_set_list[track][1]
		state.alu_control_signal = track

		state.is_mem = [-1, -1]

		if op_type == 'R':
			state.rs2 = bin_instruction[7:12]
			state.rs1 = bin_instruction[12:17]
			state.rd = bin_instruction[20:25]
			state.operand1 = self.R[int(state.rs1, 2)]
			state.operand2 = self.R[int(state.rs2, 2)]
			state.write_back_signal = True
			print("DECODE: Operation is ", operation.upper(), ", first operand is R", str(int(state.rs1, 2)), ", second operand is R", str(int(state.rs2, 2)), ", destination register is R", str(int(state.rd, 2)), sep="")
			print("DECODE: Read registers: R", str(int(state.rs1, 2)), " = ", nint(state.operand1, 16), ", R", str(int(state.rs2, 2)), " = ", nint(state.operand2, 16), sep="")

		elif op_type == 'I':
			state.rs1 = bin_instruction[12:17]
			state.rd = bin_instruction[20:25]
			imm = bin_instruction[0:12]
			state.operand1 = self.R[int(state.rs1, 2)]
			state.operand2 = imm
			state.write_back_signal = True
			print("DECODE: Operation is ", operation.upper(), ", first operand is R", str(int(state.rs1, 2)), ", immediate is ", nint(state.operand2, 2, len(state.operand2)), ", destination register is R", str(int(state.rd, 2)), sep="")
			print("DECODE: Read registers: R", str(int(state.rs1, 2)), " = ", nint(state.operand1, 16), sep="")

		elif op_type == 'S':
			state.rs2 = bin_instruction[7:12]
			state.rs1 = bin_instruction[12:17]
			imm = bin_instruction[0:7] + bin_instruction[20:25]
			state.operand1 = self.R[int(state.rs1, 2)]
			state.operand2 = imm
			state.register_data = self.R[int(state.rs2, 2)]
			state.write_back_signal = False
			print("DECODE: Operation is ", operation.upper(), ", first operand is R", str(int(state.rs1, 2)), ", immediate is ", nint(state.operand2, 2, len(state.operand2)), ", data to be stored is in R", str(int(state.rs2, 2)), sep="")
			print("DECODE: Read registers: R", str(int(state.rs1, 2)), " = ", nint(state.operand1, 16), ", R", str(int(state.rs2, 2)), " = ", nint(state.register_data, 16), sep="")

		elif op_type == 'SB':
			state.rs2 = bin_instruction[7:12]
			state.rs1 = bin_instruction[12:17]
			state.operand1 = self.R[int(state.rs1, 2)]
			state.operand2 = self.R[int(state.rs2, 2)]
			imm = bin_instruction[0] + bin_instruction[24] + \
				bin_instruction[1:7] + bin_instruction[20:24] + '0'
			state.offset = imm
			state.write_back_signal = False
			print("DECODE: Operation is ", operation.upper(), ", first operand is R", str(int(state.rs1, 2)), ", second operand is R", str(int(state.rs2, 2)), ", immediate is ", nint(state.offset, 2, len(state.offset)), sep="")
			print("DECODE: Read registers: R", str(int(state.rs1, 2)), " = ", nint(state.operand1, 16), ", R", str(int(state.rs2, 2)), " = ", nint(state.operand2, 16), sep="")

		elif op_type == 'U':
			state.rd = bin_instruction[20:25]
			imm = bin_instruction[0:20] 
			state.write_back_signal = True
			print("DECODE: Operation is ", operation.upper(), ", immediate is ", nint(imm, 2, len(imm)), ", destination register is R", str(int(state.rd, 2)), sep="")
			print("DECODE: No register read")
			imm += '0'*12
			state.operand2 = imm

		elif op_type == 'UJ':
			state.rd = bin_instruction[20:25]
			imm = bin_instruction[0] + bin_instruction[12:20] + \
				bin_instruction[11] + bin_instruction[1:11] + '0'
			state.write_back_signal = True
			state.offset = imm
			print("DECODE: Operation is ", operation.upper(), ", immediate is ", nint(imm, 2, len(imm)), ", destination register is R", str(int(state.rd, 2)), sep="")
			print("DECODE: No register read")

		else:
			print("ERROR: Unidentifiable machine code!\n")
			self.terminate = True
			self.all_dummy = True
			return False, 0, state
		
		if self.pipelining_enabled:
			branch_ins = [23, 24, 25, 26, 29, 19]
			if state.alu_control_signal not in branch_ins:
				return False, 0, state
			else:
				self.execute(state)
				self.next_PC = state.PC
				print("state.alu_control_signal", state.alu_control_signal)
				print("pc_offset = ", self.pc_offset)
				self.IAG(state)		
				orig_pc = self.next_PC
				btb = args[0]
				if not btb.find(state.PC):
					# self.inc_select = state.inc_select
					# self.pc_select = state.pc_select
					# self.pc_offset = state.pc_offset
					# self.return_address = state.return_address
					# self.IAG()
					# state.pc_update = self.next_PC
					btb.enter(state.PC, state.PC + 4)
				if orig_pc != state.next_pc:
					print("orig_pc = ", orig_pc)
					return True, orig_pc, state
				else:
					return False, 0, state
			
	# Executes the ALU operation based on ALUop
	def execute(self, state):
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
				self.terminate = True
				self.all_dummy = True
				return
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
				self.terminate = True
				self.all_dummy = True
				return
			else:
				state.register_data = bin(int(int(state.operand1, 16) >> int(state.operand2, 16)))
				if state.operand1[2] == '8' or state.operand1[2] == '9' or state.operand1[2] == 'a' or state.operand1[2] == 'b' or state.operand1[2] == 'c' or state.operand1[2] == 'd' or state.operand1[2] == 'e' or state.operand1[2] == 'f':
					state.register_data = '0b' + (34 - len(state.register_data)) * '1' + state.register_data[2:]
				state.register_data = hex(int(state.register_data, 2))

		elif state.alu_control_signal == 7:
			if(nint(state.operand2, 16) < 0):
				print("ERROR: Shift by negative!\n")
				self.terminate = True
				self.all_dummy = True
				return
			else:
				state.register_data = nhex(int(state.operand1, 16) >> int(state.operand2, 16))

		elif state.alu_control_signal == 9:
			state.register_data = nhex(int(int(state.operand1, 16) ^ int(state.operand2, 16)))

		elif state.alu_control_signal == 10:
			state.register_data = nhex(int(nint(state.operand1, 16) * nint(state.operand2, 16)))

		elif state.alu_control_signal == 11:
			if nint(state.operand2, 16) == 0:
				print("ERROR: Division by zero!\n")
				self.terminate = True
				self.all_dummy = True
				return
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
			#self.return_address = nint(state.operand2, 2, len(state.operand2)) + nint(state.operand1, 16)
			#self.pc_select = 1
			state.pc_select = 1
			state.return_address = nint(state.operand2, 2, len(state.operand2)) + nint(state.operand1, 16)

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
			if nint(state.operand1, 16) == nint(state.operand2, 16):
				state.pc_offset = nint(state.offset, 2, len(state.offset))
				state.inc_select = 1
			#state.pc_offset = nint(state.offset, 2, len(state.offset))
			#state.inc_select = 1

		elif state.alu_control_signal == 24:
			if nint(state.operand1, 16) != nint(state.operand2, 16):
				state.pc_offset = nint(state.offset, 2, len(state.offset))
				state.inc_select = 1
			#state.pc_offset = nint(state.offset, 2, len(state.offset))
			#state.inc_select = 1

		elif state.alu_control_signal == 25:
			if nint(state.operand1, 16) >= nint(state.operand2, 16):
				# print("BGE is true")
				state.pc_offset = nint(state.offset, 2,  len(state.offset))
				state.inc_select = 1
			# print("pc select and inc select = ", state.pc_select, state.inc_select)
			# state.pc_offset = nint(state.offset, 2,  len(state.offset))
			# state.inc_select = 1

		elif state.alu_control_signal == 26:
			if nint(state.operand1, 16) < nint(state.operand2, 16):
				state.pc_offset =  nint(state.offset, 2, len(state.offset))
				state.inc_select = 1
			# state.pc_offset =  nint(state.offset, 2, len(state.offset))
			# state.inc_select = 1

		elif state.alu_control_signal == 27:
			state.register_data = nhex(int(state.PC + 4 + int(state.operand2, 2)))

		elif state.alu_control_signal == 28:
			state.register_data = nhex(int(state.operand2, 2))

		elif state.alu_control_signal == 29: # Jal
			state.register_data = nhex(state.PC + 4)
			# self.pc_offset = nint(state.offset, 2, len(state.offset))
			# self.inc_select = 1
			state.pc_offset = nint(state.offset, 2, len(state.offset))
			state.inc_select = 1

		if len(state.register_data) > 10:
			state.register_data = state.register_data[:2] + state.register_data[-8:]

		state.register_data = state.register_data[:2] + \
			(10 - len(state.register_data)) * '0' + state.register_data[2::]

	# Performs the memory operations
	def mem(self, state):
		state.stage += 1

		if not self.pipelining_enabled:
			self.IAG(state)

		if state.is_dummy:
			return

		if state.is_mem[0] == -1:
			return

		elif state.is_mem[0] == 0:
			state.register_data = '0x'
			if state.is_mem[1] == 0:
				state.register_data += self.MEM[state.memory_address]
			elif state.is_mem[1] == 1:
				state.register_data += (self.MEM[state.memory_address + 1] + self.MEM[state.memory_address])
			else:
				state.register_data += (self.MEM[state.memory_address + 3] + self.MEM[state.memory_address + 2] + self.MEM[state.memory_address + 1] + self.MEM[state.memory_address])

			state.register_data = sign_extend(state.register_data)

		else:
			if state.is_mem[1] >= 3:
				self.MEM[state.memory_address + 3] = state.register_data[2:4]
				self.MEM[state.memory_address + 2] = state.register_data[4:6]
			if state.is_mem[1] >= 1:
				self.MEM[state.memory_address + 1] = state.register_data[6:8]
			if state.is_mem[1] >= 0:
				self.MEM[state.memory_address] = state.register_data[8:10]


	# Writes the results back to the register file
	def write_back(self, state):
		state.stage += 1

		if not state.is_dummy:
			if state.write_back_signal:
				if int(state.rd, 2) != 0:
					self.R[int(state.rd, 2)] = state.register_data
					print("WRITEBACK: Write", nint(state.register_data, 16), "to", "R" + str(int(state.rd, 2)))
		print("x20 = ", self.R[20])


class HDU:
	def __init__(self):
		self.E2E=0#data in EtoE data line.
		self.M2E=0
		self.M2M=0
		self.E2D=0
		self.M2D=0

	def data_hazard_forwarding(self,states):
		forwarding_paths = set()
		# forwarding_paths.add("X->X")
		new_states = []     # updated states
		new_states = [states[0]]
		toDecode = states[1]
		toExecute = states[2]
		toMem = states[3]
		toWB = states[4]
		isHazard = False    # is there a data hazard?
		doStall = False     # do we need to stall in case of data forwarding?
		stallWhere = 3      # stall at the decode stage or execute stage?
							# 1 = at execute, 2 = at decode, 3 = don't stall
							# Sorted according to priority

		toDecode_opcode = toDecode.instruction_word & (0x7F)
		toExecute_opcode = toExecute.instruction_word & (0x7F)
		toMem_opcode = toMem.instruction_word & (0x7F)
		toWB_opcode = toWB.instruction_word & (0x7F)

		# M->E and M->M forwarding before E->E forwarding, because E->E forward takes
		# precedence over the other two, and should have the capacity to overwrite


		# if toWB_opcode==3  and toMem_opcode==35:
		# load-toWB and store-toMem instructions
		# state function use these variables.
		# rs1,rs2,rd -global declare

		# register_data=WB_data;
		# RA=operand1
		# RB=operand2
		# final address in memory=memory_address.
		# M->M forwarding
		if (toWB_opcode==3) and (toMem_opcode==35):
			if toWB.rd > 0 and toWB.rd == toMem.rs2:
				toMem.register_data = toWB.register_data
				isHazard = True
				self.M2M=toWB.register_data
				forwarding_paths.add("M->M")


		# M->E forwarding
		if toWB.rd > 0:
			if toWB.rd == toExecute.rs1:
				toExecute.operand1 = toWB.register_data
				self.M2E=toWB.register_data
				isHazard = True
				forwarding_paths.add("M->E")

			if toWB.rd == toExecute.rs2:
				toExecute.operand2 = toWB.register_data
				self.M2E=toWB.register_data
				isHazard = True
				forwarding_paths.add("M->E")

		# E->E forwarding
		if toMem.rd > 0:

			# If the producer is a load instruction
			# if toMem_opcode == 3 or toMem_opcode == 55:
			if toMem_opcode == 3:

				# If the consumer is a store instruction
				if toExecute_opcode == 35:

					# Stall required for address calculation of store instruction
					if toExecute.rs1 == toMem.rs2:
						isHazard = True
						doStall = True
						stallWhere = min(stallWhere, 1)

				# If the consumer isn't a store instruction, then we need a stall
				else:
					isHazard = True
					doStall = True
					stallWhere = min(stallWhere, 1)

			# If the producer isn't a load instruction then  E->E data forwarding can be performed
			else:
				if toExecute.rs1 == toMem.rs2:
					toExecute.operand1 = toMem.register_data
					self.E2E=toMem.register_data
					isHazard = True
					forwarding_paths.add("E->E")

				if toExecute.rs2 == toMem.rs2:
					toExecute.operand2 = toMem.register_data
					self.E2E=toMem.register_data
					isHazard = True
					forwarding_paths.add("E->E")

		new_states = new_states + [toDecode, toExecute, toMem, toWB]
		return [isHazard, doStall, new_states, stallWhere, forwarding_paths]

	def data_hazard_stalling(self, pipeline_instructions):
		states_to_check = pipeline_instructions[:-1] #removed the fetch stage instruction
		print(len(states_to_check))
		exe_state = states_to_check[-2]
		decode_state = states_to_check[-1]
		if exe_state.rd != -1 and decode_state.rs1 != -1:
			if exe_state.rd == decode_state.rs1 and exe_state.rd:
				return [True, 2]
			if exe_state.rd == decode_state.rs2 and exe_state.rd:
				return [True, 2]
		mem_state = states_to_check[-3]
		if mem_state.rd != -1 and decode_state.rs1 != -1:
			if mem_state.rd == decode_state.rs1 and mem_state.rd != 0:
				return [True, 1]
			if mem_state.rd == decode_state.rs2 and mem_state.rd != 0:
				return [True, 1]

		return [False, -1]

# Add decode part, When are we entering in BTB?, How handle jal and jalr?
# Returns...what required? Return states also
# Use variable arguments in fetch and decode
