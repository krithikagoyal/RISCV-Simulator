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

def evaluate(processor, pipeline_instructions):
    for idx, x in pipeline_instructions:
        if idx == 0:
            processor.write_back(x)
        elif idx == 1:
            state1 = processor.mem(x)
        elif idx == 2:
            state2 = processor.execute(x)
        elif idx == 3:
            control_hazard, control_pc, state3 = processor.decode(x)
        elif idx == 4:
            branch_taken, branch_pc, state4 = processor.fetch(x)

    pipeline_instructions = [state1, state2, stage3, stage4]
    return pipeline_instructions, branch_taken, branch_pc, control_hazard, control_pc

if __name__ == '__main__':

    # set .mc file
    prog_mc_file = take_input()

    # invoke classes
    processor = Processor(prog_mc_file)
    btb = BTB()
    hdu = HDU()

    # Knobs
    pipelining_enabled = False                     # Knob1
    forwarding_enabled = False                     # Knob2
    print_registers_each_cycle = False             # Knob3
    print_pipeline_registers_and_cycle = False     # Knob4
    print_specific_pipeline_register = [False, -1] # Knob5

    # Other signals
    PC = 0
    clock_cycles = 0

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
                break
            processor.execute(instruction)
            if processor.terminate:
                break
            processor.mem(instruction)
            processor.write_back(instruction)
            PC = processor.next_PC
            clock_cycles += 1

            if print_registers_each_cycle:
                for i in range(32):
                    print(processor.R[i], end=" ")
            print("\n")

        processor.write_data_memory()

    else:
        pipeline_instructions = []   # instructions currently in the pipeline

        while True:
            if not forwarding_enabled:
                pipeline_instructions = [x.evaluate() for x in pipeline_instructions]

                for _ in pipeline_instructions:
                    if _.stage == 3 and _.pc_update and _.branch_taken != btb.getTarget(PC):
                        pipeline_instructions.pop() # Flush
                        # Add a dummy instruction
                        number_of_branch_mispredictions += 1
                        number_of_stalls_due_to_control_hazards += 1
                        PC = _.pc_val

                if len(pipeline_instructions) == 5:
                        pipeline_instructions = pipeline_instructions[1:]

                data_hazard = hdu.check_data_hazard(pipeline_instructions) # check if data hazard is there or not

                if not data_hazard:
                    new_instruction = State(PC)
                    pipeline_instructions.append(State(PC))
                    PC += 4
                else:
                    last_inst = pipeline_instructions[-1]
                    pipeline_instructions.pop()
                    # Add a dummy instruction
                    pipeline_instructions.append(last_inst)
                    number_of_data_hazards += 1
                    number_of_stalls_due_to_data_hazards += 1

            else:
                pipeline_instructions = [x.evaluate() for x in pipeline_instructions]
                if len(pipeline_instructions) == 5:
                    pipeline_instructions = pipeline_instructions[1:]

                control_hazard = False
                for _ in pipeline_instructions:
                    if _.control_hazard and _.pc_update != _.pc_next:
                        control_hazard = True
                        number_of_control_hazards += 1
                        pipeline_instructions.pop()
                        pipeline_instructions.append(State(_.pc_update))
                        PC = _.pc_update + 4
                        break

                if not control_hazard:
                    new_instruction = State(PC)
                    pipeline_instructions.append(new_instruction) # if data_hazard is there, then execute will itself pick the data required form the buffer.

            clock_cycles += 1

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

            # How terminate? One possible solution is to add a dummy instruction in fetch after program instructions.
            # The program then can be terminated if all the instructions are dummy instructions

# Print Messages

# display the data
display()
