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

# main.py
# Purpose of this file: This file controls the overall functioning of the Simulator.

from Gui import display, take_input
from myRISCVSim import State, Processor, BTB, HDU
import time

stats = [
	"Total number of cycles: ",
	"Total instructions executed: ",
	"CPI: ",
	"Number of data-transfer(load and store): ",
	"Number of ALU instructions executed: ",
	"Number of Control instructions: ",
	"Number of stalls/bubbles in the pipeline: ",
	"Number of data hazards: ",
	"Number of control hazards: ",
	"Number of branch mispredictions: ",
	"Number of stalls due to data hazards: ",
	"Number of stalls due to control hazards: "
]

s = [0]*12

l = []
l_dash = []
pc_tmp = []
data_hazard_pairs = []
control_hazard_signals = []
stage = {1: "fetch", 2: "decode", 3: "execute", 4: "memory", 5: "write_back"}

# Function for pipelined execution
def evaluate(processor, pipeline_ins):
	processor.write_back(pipeline_ins[0])
	processor.mem(pipeline_ins[1])
	processor.execute(pipeline_ins[2])
	control_hazard, control_pc, entering, color = processor.decode(pipeline_ins[3], btb)
	if entering:
		control_hazard_signals.append(2)
	elif pipeline_ins[2].is_dummy and color != 0 and len(control_hazard_signals) > 0 and control_hazard_signals[-1] == 2:
		control_hazard_signals.append(control_hazard_signals[-1])
	else:
		control_hazard_signals.append(color)
	processor.fetch(pipeline_ins[4], btb)
	pipeline_ins = [pipeline_ins[1], pipeline_ins[2], pipeline_ins[3], pipeline_ins[4]]
	return pipeline_ins, control_hazard, control_pc


if __name__ == '__main__':

	# set .mc file and input knobs
	prog_mc_file, pipelining_enabled, forwarding_enabled, print_registers_each_cycle, print_pipeline_registers, print_specific_pipeline_registers = take_input()

	# Knobs
	# pipelining_enabled = True                       # Knob1
	# forwarding_enabled = False                      # Knob2
	# print_registers_each_cycle = False              # Knob3
	# print_pipeline_registers = False    			  # Knob4
	# print_specific_pipeline_registers = [False, 10] # Knob5

	# invoke classes
	processor = Processor(prog_mc_file)
	hdu = HDU()
	btb = BTB()

	# Signals
	PC = 0
	clock_cycles = 0
	prog_end = False

	# Various Counts
	number_of_stalls_due_to_control_hazards = 0
	number_of_data_hazards = 0
	number_of_stalls_due_to_data_hazards = 0
	total_number_of_stalls = 0


	if not pipelining_enabled:
		# Multi-cycle
		processor.pipelining_enabled = False

		while True:
			instruction = State(PC)

			processor.fetch(instruction)
			clock_cycles += 1
			if print_registers_each_cycle:
				print("CLOCK CYCLE:", clock_cycles)
				print("Register Data:-")
				for i in range(32):
					print("R" + str(i) + ":", processor.R[i], end=" ")
				print("\n")
			pc_tmp.append([-1, -1, -1, -1, instruction.PC])
			data_hazard_pairs.append({'who': -1, 'from_whom': -1})

			processor.decode(instruction)
			pc_tmp.append([-1, -1, -1, instruction.PC, -1])
			data_hazard_pairs.append({'who': -1, 'from_whom': -1})
			clock_cycles += 1
			if print_registers_each_cycle:
				print("CLOCK CYCLE:", clock_cycles)
				print("Register Data:-")
				for i in range(32):
					print("R" + str(i) + ":", processor.R[i], end=" ")
				print("\n")
			if processor.terminate:
				prog_end = True
				break

			processor.execute(instruction)
			pc_tmp.append([-1, -1, instruction.PC, -1, -1])
			data_hazard_pairs.append({'who': -1, 'from_whom': -1})
			clock_cycles += 1
			if print_registers_each_cycle:
				print("CLOCK CYCLE:", clock_cycles)
				print("Register Data:-")
				for i in range(32):
					print("R" + str(i) + ":", processor.R[i], end=" ")
				print("\n")

			processor.mem(instruction)
			pc_tmp.append([-1, instruction.PC, -1, -1, -1])
			data_hazard_pairs.append({'who': -1, 'from_whom': -1})
			clock_cycles += 1
			if print_registers_each_cycle:
				print("CLOCK CYCLE:", clock_cycles)
				print("Register Data:-")
				for i in range(32):
					print("R" + str(i) + ":", processor.R[i], end=" ")
				print("\n")

			processor.write_back(instruction)
			pc_tmp.append([instruction.PC, -1, -1, -1, -1])
			data_hazard_pairs.append({'who': -1, 'from_whom': -1})
			control_hazard_signals += [0,0,0,0,0]
			clock_cycles += 1
			if print_registers_each_cycle:
				print("CLOCK CYCLE:", clock_cycles)
				print("Register Data:-")
				for i in range(32):
					print("R" + str(i) + ":", processor.R[i], end=" ")
				print("\n")

			PC = processor.next_PC

	else:
		processor.pipelining_enabled = True
		pipeline_instructions = [State(0) for _ in range(5)]
		for i in range(4):
			pipeline_instructions[i].is_dummy = True

		while not prog_end:
			if not forwarding_enabled:
				data_hazard = hdu.data_hazard_stalling(pipeline_instructions)

				old_states = pipeline_instructions
				pipeline_instructions, control_hazard, control_pc = evaluate(processor, pipeline_instructions)

				tmp = []
				for i in range(5):
					if(old_states[i].is_dummy):
						tmp.append("bubble")
					else:
						tmp.append(old_states[i].PC)
				pc_tmp.append(tmp)
				data_hazard_pairs.append(data_hazard[2])

				branch_taken = pipeline_instructions[3].branch_taken
				branch_pc = pipeline_instructions[3].next_pc

				PC += 4

				if branch_taken and not data_hazard[0]:
					PC = branch_pc

				if control_hazard and not data_hazard[0]:
					number_of_stalls_due_to_control_hazards += 1
					PC = control_pc
					pipeline_instructions.append(State(PC))
					pipeline_instructions[-2].is_dummy = True

				if data_hazard[0]:
					number_of_data_hazards += data_hazard[1]
					number_of_stalls_due_to_data_hazards += 1
					pipeline_instructions = pipeline_instructions[:2] + [State(0)] + old_states[3:]
					pipeline_instructions[2].is_dummy = True
					PC -= 4

				if not control_hazard and not data_hazard[0]:
					pipeline_instructions.append(State(PC))

				pipeline_instructions[-2].next_pc = PC

				prog_end = True
				for i in range(4):
					x = pipeline_instructions[i]
					if not x.is_dummy:
						prog_end = False
						break

			else:
				data_hazard, if_stall, stall_position, pipeline_instructions, gui_pair = hdu.data_hazard_forwarding(pipeline_instructions)

				old_states = pipeline_instructions
				pipeline_instructions, control_hazard, control_pc = evaluate(processor, pipeline_instructions)

				tmp = []
				for i in range(5):
					if(old_states[i].is_dummy):
						tmp.append("bubble")
					else:
						tmp.append(old_states[i].PC)
				pc_tmp.append(tmp)
				data_hazard_pairs.append(gui_pair)

				branch_taken = pipeline_instructions[3].branch_taken
				branch_pc = pipeline_instructions[3].next_pc

				PC += 4

				if branch_taken and not if_stall:
					PC = branch_pc

				if control_hazard and not if_stall:
					number_of_stalls_due_to_control_hazards += 1
					PC = control_pc
					pipeline_instructions.append(State(PC))
					pipeline_instructions[-2].is_dummy = True

				if if_stall:
					number_of_stalls_due_to_data_hazards += 1

					if stall_position == 0:
						pipeline_instructions = pipeline_instructions[:1] + [State(0)] + old_states[2:]
						pipeline_instructions[1].is_dummy = True
						PC -= 4

					elif stall_position == 1:
						pipeline_instructions = pipeline_instructions[:2] + [State(0)] + old_states[3:]
						pipeline_instructions[2].is_dummy = True
						PC -= 4

				number_of_data_hazards += data_hazard

				if not control_hazard and not if_stall:
					pipeline_instructions.append(State(PC))

				pipeline_instructions[-2].next_pc = PC

				for inst in pipeline_instructions:
					inst.decode_forwarding_op1 = False
					inst.decode_forwarding_op2 = False

				prog_end = True
				for i in range(4):
					x = pipeline_instructions[i]
					if not x.is_dummy:
						prog_end = False
						break

			clock_cycles += 1
			if print_registers_each_cycle:
				print("CLOCK CYCLE:", clock_cycles)
				print("Register Data:-")
				for i in range(32):
					print("R" + str(i) + ":", processor.R[i], end=" ")
				print("\n")

			# Print specific pipeline register
			if print_specific_pipeline_registers[0]:
				for inst in pipeline_instructions:
					if inst.PC/4 == print_specific_pipeline_registers[1]:
						if not print_registers_each_cycle:
							print("CLOCK CYCLE:", clock_cycles)
						print("Pipeline Registers:-")
						print("Fetch # Decode =>", "Instruction:", pipeline_instructions[3].instruction_word)
						print("Decode # Execute => ", "Operand1: ", pipeline_instructions[2].operand1, ", Operand2: ", pipeline_instructions[2].operand2, sep="")
						print("Execute # Memory => ", "Data: ", pipeline_instructions[1].register_data, sep="")
						print("Memory # WriteBack => ", "Data: ", pipeline_instructions[0].register_data, sep="")
						print("\n")

			# Print pipeline registers
			elif print_pipeline_registers:
				if not print_registers_each_cycle:
					print("CLOCK CYCLE:", clock_cycles)
				print("Pipeline Registers:-")
				print("Fetch # Decode =>", "Instruction:", pipeline_instructions[3].instruction_word)
				print("Decode # Execute => ", "Operand1: ", pipeline_instructions[2].operand1, ", Operand2: ", pipeline_instructions[2].operand2, sep="")
				print("Execute # Memory => ", "Data: ", pipeline_instructions[1].register_data, sep="")
				print("Memory # WriteBack => ", "Data: ", pipeline_instructions[0].register_data, sep="")
				print("\n")


	# Print Statistics
	s[0] = clock_cycles
	s[1] = processor.count_total_inst
	s[2] = s[0]/s[1]
	s[3] = processor.count_mem_inst
	s[4] = processor.count_alu_inst
	s[5] = processor.count_control_inst
	s[7] = number_of_data_hazards
	if pipelining_enabled:
		s[8] = s[5]
	s[9] = processor.count_branch_mispredictions
	s[10] = number_of_stalls_due_to_data_hazards
	s[11] = number_of_stalls_due_to_control_hazards
	s[6] = s[10] + s[11]

	if prog_end:
		processor.write_data_memory()
		for i in range(12):
			stats[i] += str(s[i]) + '\n'
		statfile = open("stats.txt", "w")
		statfile.writelines(stats)
		statfile.close()
		for i in range(len(pc_tmp)):
			tmp = [str(processor.get_code[x]) for x in pc_tmp[i]]
			l.append(tmp)
			tmp = []
			for j in range(5):
				if forwarding_enabled and pipelining_enabled:
					if data_hazard_pairs[i]['from'][j] != '':
						tmp.append(str(processor.get_code[pc_tmp[i][j]]) + "\n" + data_hazard_pairs[i]['from'][j])
					else:
						tmp.append(str(processor.get_code[pc_tmp[i][j]]))
				else:
					tmp.append(str(processor.get_code[pc_tmp[i][j]]))
			l_dash.append(tmp + [data_hazard_pairs[i]])

		# resolvong control + data hazard case
		for i in range(len(l)):
			if data_hazard_pairs[i]['who'] == 3:
				control_hazard_signals[i] = 0

		# control_hazard_signals is a list on integers 0=> nothing; 1=> red ; 2 => yellow; 3=> green
		display(l, control_hazard_signals, l_dash )
