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
from myRISCVSim_check import State, Processor, BTB, HDU
import time

stats = [
	"Total number of cycles: ",
	"Total instructions executed: ",
	"CPI: ",
	"Number of data-transfer(load and store): ",
	"Number of ALU instructions executed: ",
	"Number of Control instructions: ",
	"Number of stalls/bubbles in the pipeline: ",
	"Stat8: Number of data hazards: ",
	"Number of control hazards: ",
	"Number of branch mispredictions: ",
	"Number of stalls due to data hazards: ",
	"Number of stalls due to control hazards: "
]

s = [0]*12

def evaluate(processor, pipeline_ins):
	processor.write_back(pipeline_ins[0])
	if(!pipeline_ins[0].is_dummy):
		s[1] += 1
	else:
		s[6] += 1
	processor.mem(pipeline_ins[1])
	processor.execute(pipeline_ins[2])
	control_hazard, control_pc, state3 = processor.decode(pipeline_ins[3], btb)
	processor.fetch(pipeline_ins[4], btb)
	pipeline_ins = [pipeline_ins[1], pipeline_ins[2], pipeline_ins[3], pipeline_ins[4]]
	return pipeline_ins, control_hazard, control_pc

if __name__ == '__main__':

	# set .mc file
	prog_mc_file = take_input()

	prog_mc_file = take_input()
	print(prog_mc_file)

	# invoke classes
	processor = Processor(prog_mc_file)
	hdu = HDU()
	btb = BTB()

	# Knobs
	pipelining_enabled = True                      # Knob1
	forwarding_enabled = False                      # Knob2
	print_registers_each_cycle = True              # Knob3
	print_pipeline_registers_and_cycle = False     # Knob4
	print_specific_pipeline_register = [False, -1] # Knob5

	# Signals
	PC = 0
	clock_cycles = 0
	prog_end = False

	# Various Counts
	number_of_control_hazards = 0
	number_of_stalls_due_to_control_hazards = 0
	number_of_data_hazards = 0
	number_of_stalls_due_to_data_hazards = 0
	total_number_of_stalls = 0
	number_of_branch_mispredictions = 0

	if not pipelining_enabled:
		processor.pipelining_enabled = False

		while True:
			instruction = State(PC)
			processor.fetch(instruction)
			processor.decode(instruction)
			if processor.terminate:
				prog_end = True
				break
			processor.execute(instruction)
			if processor.terminate:
				prog_end = True
				break
			processor.mem(instruction)
			processor.write_back(instruction)

			PC = processor.next_PC
			clock_cycles += 5

			if print_registers_each_cycle:
				for i in range(32):
					print(processor.R[i], end=" ")
				print("\n")

			print(clock_cycles)

	else:
		processor.pipelining_enabled = True

		pipeline_instructions = [State(0) for _ in range(5)]
		for i in range(4):
			pipeline_instructions[i].is_dummy = True

		while not prog_end:
			if not forwarding_enabled:
				data_hazard = hdu.data_hazard_stalling(pipeline_instructions)

				# for x in pipeline_instructions:
					# print("x.pcp = ", x.PC, x.is_dummy)

				old_states = pipeline_instructions
				pipeline_instructions, control_hazard, control_pc = evaluate(processor, pipeline_instructions)

				branch_taken = pipeline_instructions[3].branch_taken
				branch_pc = pipeline_instructions[3].next_pc

				PC += 4

				if branch_taken and not data_hazard[0]:
					PC = branch_pc
					# print("branch_pc", branch_pc)

				if control_hazard and not data_hazard[0]:
					number_of_control_hazards += 1
					number_of_stalls_due_to_control_hazards += 1
					PC = control_pc
					# print("control_pc = ", control_pc)
					pipeline_instructions.append(State(PC))
					pipeline_instructions[-2].is_dummy = True

				if data_hazard[0]:
					number_of_data_hazards += 1
					number_of_stalls_due_to_data_hazards += 1
					pipeline_instructions = pipeline_instructions[:2] + [State(0)] + old_states[3:]
					pipeline_instructions[2].is_dummy = True
					PC -= 4

				# print("lll ", control_hazard, data_hazard, PC)
				if not control_hazard and not data_hazard[0]:
					pipeline_instructions.append(State(PC))

				pipeline_instructions[-2].next_pc = PC
				# print("len ", len(pipeline_instructions))
				prog_end = True
				for i in range(4):
					x = pipeline_instructions[i]
					# print("X.pc ", x.PC)
					if not x.is_dummy:
						prog_end = False
						break

			else:
				data_hazard, if_stall, stall_position, pipeline_instructions = hdu.data_hazard_forwarding(pipeline_instructions)

				# for x in pipeline_instructions:
					# print("x.pcp = ", x.PC, x.is_dummy)

				old_states = pipeline_instructions
				pipeline_instructions, control_hazard, control_pc = evaluate(processor, pipeline_instructions)

				branch_taken = pipeline_instructions[3].branch_taken
				branch_pc = pipeline_instructions[3].next_pc

				PC += 4

				if branch_taken and not if_stall:
					PC = branch_pc
					# print("branch_pc", branch_pc)

				if control_hazard and not if_stall:
					number_of_control_hazards += 1
					number_of_stalls_due_to_control_hazards += 1
					PC = control_pc
					# print("control_pc = ", control_pc)
					pipeline_instructions.append(State(PC))
					pipeline_instructions[-2].is_dummy = True

				if if_stall:
					number_of_stalls_due_to_data_hazards += 1
					if stall_position == 1:
						pipeline_instructions = pipeline_instructions[:2] + [State(0)] + old_states[3:]
						pipeline_instructions[2].is_dummy = True
					elif stall_position == 2:
						pipeline_instructions = pipeline_instructions[:3] + [State(0)] + old_states[4:]
						pipeline_instructions[3].is_dummy = True
					PC -= 4

				number_of_data_hazards += data_hazard

				# print("lll ", control_hazard, data_hazard, PC)
				if not control_hazard and not if_stall:
					pipeline_instructions.append(State(PC))

				pipeline_instructions[-2].next_pc = PC

				for inst in pipeline_instructions:
					inst.decode_forwarding_op1 = False
					inst.decode_forwarding_op2 = False

				# print("len ", len(pipeline_instructions))
				prog_end = True
				for i in range(4):
					x = pipeline_instructions[i]
					# print("X.pc ", x.PC)
					if not x.is_dummy:
						prog_end = False
						break

			clock_cycles += 1

			# if print_registers_each_cycle:
			# 	for i in range(32):
			# 		print(processor.R[i], end=" ")
			# print("\n")

			# Print specific pipeline register
			# Shift this above among instructions or elsewhere
			# if print_specific_pipeline_register[0]:
			# 	pass

			# Print pipeline registers and cycle
			# if print_pipeline_registers_and_cycle:
			# 	pass

			# print(clock_cycles)

	# Print Messages
	s[0] = clock_cycles
	s[1] = s[1]
	s[2] = s[0]/s[1]
	s[6] = s[6]
	if prog_end:
		processor.write_data_memory()
		for i in range(12):
			stats[i] += str(s[i])
		statfile = open("stats.txt", "w")
		statfile.writelines(stats)
		statfile.close()
		display()


# Redundant stages and all dummy maybe
# use of second argument of data_hazard_stalling?
