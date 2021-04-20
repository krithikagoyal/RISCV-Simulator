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

def evaluate(processor, pipeline_instructions, btb):
    for idx in range(5):
        if idx == 0:
            processor.write_back(pipeline_instructions[idx])
        elif idx == 1:
            state1 = processor.mem(pipeline_instructions[idx])
        elif idx == 2:
            state2 = processor.execute(pipeline_instructions[idx])
        elif idx == 3:
            state3 = processor.decode(pipeline_instructions[idx], btb)
            control_hazard = pipeline_instructions[idx].control_hazard
            control_pc = pipeline_instructions[idx].control_pc
        elif idx == 4:
            state4 = processor.fetch(pipeline_instructions[idx], btb)
            branch_taken = pipeline_instructions[idx].branch_taken
            branch_pc = pipeline_instructions[idx].branch_pc

    pipeline_instructions = [state1, state2, state3, state4]
    return pipeline_instructions, branch_taken, branch_pc, control_hazard, control_pc

if __name__ == '__main__':

    # set .mc file
    prog_mc_file = take_input()

    # invoke classes
    processor = Processor(prog_mc_file)
    hdu = HDU()
    btb = BTB()

    # Knobs
    pipelining_enabled = True                      # Knob1
    forwarding_enabled = False                     # Knob2
    print_registers_each_cycle = True              # Knob3
    print_pipeline_registers_and_cycle = False     # Knob4
    print_specific_pipeline_register = [False, -1] # Knob5

    # Signals
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
        processor.pipelining_enabled = True

        pipeline_instructions = [State(0) for _ in range(5)]
        for i in range(4):
            pipeline_instructions[i].is_dummy = True

        while True:
            print(PC)

            if not forwarding_enabled:
                data_hazard = hdu.data_hazard_stalling(pipeline_instructions)
                pipeline_instructions, branch_taken, branch_pc, control_hazard, control_pc = evaluate(processor, pipeline_instructions, btb)

                pc_update = False
                if branch_taken and not data_hazard[0]:
                    pc_update = True
                    PC = branch_pc

                if control_hazard:
                    pipeline_instructions[3].is_dummy = True
                    pc_update = True
                    PC = control_pc
                    number_of_control_hazards += 1
                    number_of_stalls_due_to_control_hazards += 1

                if not control_hazard and data_hazard[0]:
                    pipeline_instructions[3].is_dummy = True
                    pc_update = True
                    number_of_data_hazards += 1
                    number_of_stalls_due_to_data_hazards += 1

                if not pc_update:
                    PC += 4

                pipeline_instructions.append(State(PC))

                terminate = True
                for x in pipeline_instructions:
                    if not x.is_dummy:
                        terminate = False
                        break

                if terminate:
                    break

            else:
                pass

            clock_cycles += 1

            if print_registers_each_cycle:
                for i in range(32):
                    print(processor.R[i], end=" ")
            print("\n")

            # Print specific pipeline register
            # Shift this above among instructions or elsewhere
            if print_specific_pipeline_register[0]:
                pass

            # Print pipeline registers and cycle
            if print_pipeline_registers_and_cycle:
                pass

# Print Messages

# display the data
display()

# all_dummy and stage
# use of second argument of data_hazard_stalling
