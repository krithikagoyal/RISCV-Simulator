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
# Purpose of this file: This file handles the input and output, and invokes the simulator.

from Gui import display, take_input
from myRISCVSim import run_RISCVsim, reset_proc, load_program_memory
import time

# if control_hazard returns true, it will add a predicted instruction to the pipeline_instructions
# else it will return false
# if forwarding is enabled data_hazard will chnage the state of instruction by specifying from where it will pick data in a stage where hazard is occuring
# else will add a dummy instruction
# x.evaluate() will evaluate the particular stage of the instruction, all the information 
# needed for evaluation will be stored in the state.
# State() of an instruction will also store from where to pick the data for a particular
# state, default will be buffer of previous stage of the instruction but can be changed due to,
# data_hazard.

if __name__ == '__main__':
    # set .mc file
    prog_mc_file = take_input()
    # reset the processor
    reset_proc()
    # load the program memory
    load_program_memory(prog_mc_file)
    # display the data
    # display()
    pipeline_instructions = []   # instructions currently in the pipeline
    terminate = False            # has the program terminated ? 
    forwarding_enabled = False
    while len(pipeline_instructions) != 5:   # initialising by adding starting 5 states
        new_instruction = State(PC)
        ctrl_hazard = control_hazard(pipeline_instructions, new_instruction) # will add the predicted instruction
        data_hazard = data_hazard(pipeline_instructions, new_instruction, forwarding_enabled)
        if not ctrl_hazard and not data_hazard:
            pipeline_instructions.append(State(PC)) # State(PC) will return an object of a class State() 
            PC += 4
    while not terminate:
        x = [x.evaluate() for x in pipeline_instructions]
        x = [1:]
        new_instruction = State(PC)
        ctrl_hazard = control_hazard(pipeline_instructions, new_instruction)
        data_hazard = data_hazard(pipeline_instructions, new_instruction, forwarding_enabled)
        if not ctrl_hazard and not data_hazard:
            pipeline_instructions.append(State(PC)) # State(PC) will return an object of a class State() 
            PC += 4
