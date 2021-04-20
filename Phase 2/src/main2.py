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

    processor = Processor(prog_mc_file)
    hdu = HDU()
    btb = BTB()
    # invoke BTB
    # invoke HDU

    # Knobs
    pipelining_enabled = False                     # Knob1
    forwarding_enabled = False                     # Knob2
    print_registers_each_cycle = False             # Knob3
    print_pipeline_registers_and_cycle = False     # Knob4
    print_specific_pipeline_register = [False, -1] # Knob5

    # Other signals
    PC = 0
    clock_cycles = 0
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
            instruction = processor.fetch(instruction)
            instruction = processor.decode(instruction)
            if processor.terminate:
                break
            instruction = processor.execute(instruction)
            if processor.terminate:
                break
            instruction = processor.mem(instruction)
            instruction = processor.write_back(instruction)
            PC = processor.next_PC
            clock_cycles += 1
            if print_registers_each_cycle:
                for i in range(32):
                    print(processor.R[i], end=" ")
            print("\n")

        processor.write_data_memory()

    else:
        # add dummy instructions at the beginning
        terminate = False
        pipeline_instructions = [State(0) for _ in range(5)]   # instructions currently in the pipeline
        for i in range(5):
            pipeline_instrcions[i].is_dummy = True

        while not terminate:
            if not forwarding_enabled:
                data_hazard = data_hazard_stalling(pipeline_instructions)
                pipeline_instructions, branch_taken, branch_pc, control_hazard, control_pc = evaluate(processor, pipeline_instructions)
                
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
                    number_of_data_hazards = 0
                    number_of_stalls_due_to_data_hazards = 0
                    pc_update = True

                if not pc_update:
                    PC += 4

                pipeline_instructions.append(State(PC))

                terminate = True
                for x in pipeline_instructions:
                    if not x.is_dummy:
                        terminate = False
                        break


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

            if terminate:
                display()
                break

            # How terminate? One possible solution is to add a dummy instruction in fetch after program instructions.
            # The program then can be terminated if all the instructions are dummy instructions
