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
from myRISCVSim_check import State, Processor, BTB, HDU # Also, import Hazard detection unit
import time

def evaluate(processor, pipeline_ins):
	processor.write_back(pipeline_ins[0])
	processor.mem(pipeline_ins[1])
	processor.execute(pipeline_ins[2])
	control_hazard, control_pc, state3 = processor.decode(pipeline_ins[3], btb)
	processor.fetch(pipeline_ins[4], btb)
	pipeline_ins = [pipeline_ins[1], pipeline_ins[2], pipeline_ins[3], pipeline_ins[4]]
	return pipeline_ins, control_hazard, control_pc

if __name__ == '__main__':

	# set .mc file
	prog_mc_file = take_input()

	processor = Processor(prog_mc_file)
	hdu = HDU()
	btb = BTB()
	# invoke BTB
	# invoke HDU

	# Knobs
	pipelining_enabled = True                     # Knob1
	forwarding_enabled = False                     # Knob2
	print_registers_each_cycle = False             # Knob3
	print_pipeline_registers_and_cycle = False     # Knob4
	print_specific_pipeline_register = [False, -1] # Knob5

	# Other signals
	PC = 0
	clock_cycles = 0
	prog_end = False
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
			clock_cycles += 1
			if print_registers_each_cycle:
				for i in range(32):
					print(processor.R[i], end=" ")
				print("\n")
			print(clock_cycles)

		processor.write_data_memory()

	else:
		# add dummy instructions at the beginning
		processor.pipelining_enabled = True
		terminate = False
		pipeline_instructions = [State(0) for _ in range(5)]   # instructions currently in the pipeline
		for i in range(4):
			pipeline_instructions[i].is_dummy = True

		while not prog_end:
			if not forwarding_enabled:
				data_hazard = hdu.data_hazard_stalling(pipeline_instructions)

				for x in pipeline_instructions:
					print("x.pcp = ", x.PC)

				old_states = pipeline_instructions
				pipeline_instructions, control_hazard, control_pc = evaluate(processor, pipeline_instructions)

				branch_taken = pipeline_instructions[3].branch_taken
				branch_pc = pipeline_instructions[3].next_pc

				PC += 4

				if branch_taken and not data_hazard[0]:
					PC = branch_pc

				if control_hazard and not data_hazard[0]:
					number_of_control_hazards += 1
					number_of_stalls_due_to_control_hazards += 1
					PC = control_pc
					pipeline_instructions.append(State(0))
					pipeline_instructions[-1].is_dummy = True

				if data_hazard[0]:
					number_of_data_hazards += 1
					number_of_stalls_due_to_data_hazards += 1
					pipeline_instructions = pipeline_instructions[:2] + [State(0)] + old_states[3:]
					pipeline_instructions[2].is_dummy = True
					PC -= 4

				print("lll ", control_hazard, data_hazard, PC)
				if not control_hazard and not data_hazard[0]:
					pipeline_instructions.append(State(PC))

				pipeline_instructions[-2].next_pc = PC
				print("len ", len(pipeline_instructions))
				prog_end = True
				for x in pipeline_instructions:
					print("X.pc ", x.PC)
					if not x.is_dummy:
						prog_end = False
						break

			clock_cycles += 1
			print("clock_cycles = ", clock_cycles)

			if print_registers_each_cycle:
				# Print registers
				print("\n")

			# Shift this above among instructions or elsewhere
			if print_specific_pipeline_register[0]:
				# Print specific pipeline register
				print("\n")

			if print_pipeline_registers_and_cycle:
				# Print pipeline registers and cycle
				print("\n")

	if prog_end:
		display()
			# How terminate? One possible solution is to add a dummy instruction in fetch after program instructions.
			# The program then can be terminated if all the instructions are dummy instructions
