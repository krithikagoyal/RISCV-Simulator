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
from myRISCVSim import State, ProcessingUnit, BTB # Change names if used different
# import from Hazard detection unit
import time

'''
1. For non-pipelined version, each of the five stages takes pipelining_enabled,
    and terminate as input. Implement it accordingly in myRISCVSim.py

2. State() of an instruction will also store from where to pick the data for a
    particular state, default will be buffer of previous stage of the instruction
    but can be changed due to, data_hazard.

3. x.evaluate() will evaluate the particular stage of the instruction,
    all the information needed for evaluation will be stored in the state.
    For this, the class will have a variable as self.stage = -1.
    This variable will increase in each stage.

    def evaluate(instruction, pipelining_enabled):
        terminate = false
        if instruction.stage == 1:
            fetch(instruction, pipelining_enabled, terminate) # even though terminate is not required
        ...
        return instruction

4. PC for a branch instruction, not present in BTB will be calculated in decode stage.

5. check_data_hazard in HDU returns if data_hazard is there or not

---Later---
1. If control_hazard returns true, and it will add a predicted instruction to the
    pipeline_instructions, else it will return false.

2. If forwarding is enabled, data_hazard will change the state of instruction
    by specifying from where it will pick data in a stage where hazard is occuring,
    else will add a dummy instruction.

3. Expected functions:
a) class: State(PC): # will take PC as an input
                  ins = 0
                  stage = -1
                  function evaluate(),
                  pc_update = value of the pc up_date depending on branch taken or not taken
                  branch_taken = False
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
------
'''

if __name__ == '__main__':

    # set .mc file
    prog_mc_file = take_input()

    # invoke the processing unit
    # invoke BTB
    # invoke HDU

    # Knobs
    pipelining_enabled = True                      # Knob1
    forwarding_enabled = False                     # Knob2
    print_registers_each_cycle = False             # Knob3
    print_pipeline_registers_and_cycle = False     # Knob4
    print_specific_pipeline_register = [False, -1] # Knob5

    '''
        # Various counts, Some might be already declared in myRISCVSim.py
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
    '''

    # Other signals
    PC = 0
    clock_cycles = 0
    terminate = False            # has the program terminated ?
    number_of_data_hazards = 0
    number_of_branch_mispredictions = 0
    number_of_stalls_due_to_control_hazards = 0
    number_of_control_hazards = 0
    number_of_stalls_due_to_data_hazards = 0

    if not pipelining_enabled:
        while True:
            instruction = State(PC)
            Processor.fetch(instruction, pipelining_enabled, terminate)
            Processor.decode(instruction, pipelining_enabled, terminate)
            if terminate:
                break
            Processor.execute(instruction, pipelining_enabled, terminate)
            if terminate:
                break
            Processor.memory(instruction, pipelining_enabled, terminate)
            Processor.write_back(instruction, pipelining_enabled, terminate)
            clock_cycles += 1

            if print_registers_each_cycle:
                # Print registers, also print cycle
                print("\n");

    else:
        pipeline_instructions = []   # instructions currently in the pipeline

        while True:
            if not forwarding_enabled:
                pipeline_instructions = [x.evaluate() for x in pipeline_instructions]

                for _ in pipeline_instructions:
                    if _.stage == 3 and _.pc_update and _.branch_taken != btb.get_Target[PC]
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

'''
---For later reference---
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

            # Check for control hazards
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
------
'''

# Print Messages

# display the data
# display()
