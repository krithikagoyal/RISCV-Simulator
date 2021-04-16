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

'''
1. If control_hazard returns true, it will add a predicted instruction to the
    pipeline_instructions, else it will return false.

2. If forwarding is enabled, data_hazard will change the state of instruction
    by specifying from where it will pick data in a stage where hazard is occuring,
    else will add a dummy instruction.

3. x.evaluate() will evaluate the particular stage of the instruction,
    all the information needed for evaluation will be stored in the state.

4. State() of an instruction will also store from where to pick the data for a
    particular state, default will be buffer of previous stage of the instruction
    but can be changed due to, data_hazard.

5. PC for a branch instruction, not present in BTB will be calculated in decode stage.

6. Expected functions:
a) class: State(PC): # will take PC as an input
                  ins = 0
                  function evaluate(),
                  pc_update = False
                  branch_taken = False
                  pc_val = PC
                  data_decode = [instruction_number, buffer_number]
                  data_execute = [instruction_number, buffer_number]
                  # stores from where we will pick the data for the execution of a particular instruction.

b) data_hazard(pipeline_instructions, new_instruction, pc, forwarding_enabled) # pass by reference
            if forwarding_enabled:
                check if new_instruction can be added or not
                if cannot be added:
                    then change the state of new_instruction to store, from where it will pick the data
                    add it to pipeline_instructions
                    update PC accordingly
            else:
                check if the new instruction can be added or not, else add a stall

            return was_there_hazard, new_pc

buffers = [5][5]
'''

if __name__ == '__main__':

    # set .mc file
    prog_mc_file = take_input()

    # reset the processor
    reset_proc()

    # load the program memory
    load_program_memory(prog_mc_file)

    # display the data
    # display()

    # Knobs
    pipelining_enabled = True                      # Knob1
    forwarding_enabled = False                     # Knob2
    print_register = False                         # Knob3
    print_pipeline_register_and_cycle = False      # Knob4
    print_specific_pipeline_register = [False, -1] # Knob5

    # Various counts
    number_of_cycles = 0
    total_instructions_executed = 0
    cpi = cycles / total_instructions_executed # should be calculated at the end, shift at the end
    data_transfer_instructions = 0 # Loads and stores
    alu_instructions = 0
    control_instructions = 0
    number_of_stalls = 0 # or bubbles in the pipeline
    number_of_data_hazards = 0
    number_of_control_hazard = 0
    number_of_branch_mispredictions = 0
    number_of_stalls_due_to_data_hazards = 0
    number_of_stalls_due_to_control_hazards = 0

    # Other signals
    PC = 0

    if not pipelining_enabled:
        print("Hello");

    else:
        pipeline_instructions = []   # instructions currently in the pipeline
        terminate = False            # has the program terminated ?
        branch_taken = {}

        while not terminate:
            pipeline_instructions = [x.evaluate() for x in pipeline_instructions]

            for _ in pipeline_instructions:                              # check if the pc has been updated because of a conditional branch
                if _.pc_update and _.branch_taken != branch_taken[_.pc]: # if it is not equal to the branch we predicted.
                    branch_taken.pop(_.pc)
                    pipeline_instructions.pop()                          # flushing 1 time assuming branch decision is calculated during decode stage
                    PC = _.pc_val                                        # updated PC

            if len(pipeline_instructions) == 5:
                pipeline_instructions = pipeline_instructions[1:]        # removing the first instruction since it has been executed

            new_instruction = State(PC)
            new_pc = PC

            # What all is this?
            ctrl_hazard, new_pc = control_hazard(pipeline_instructions, new_instruction, PC)

            # data_hazard will work according to whether forwarding is enabled or not.
            data_hazard, new_pc = data_hazard(pipeline_instructions, new_instruction, forwarding_enabled, PC)

            if ctrl_hazard and new_pc != PC + 4:
                branch_taken[PC] = True
            elif ctrl_hazard:
                branch_taken[PC] = False

            PC = new_pc
            if not ctrl_hazard and not data_hazard:
                pipeline_instructions.append(State(PC)) # State(PC) will return an object of a class State()
                PC += 4

            # How terminate?

# Print Messages
