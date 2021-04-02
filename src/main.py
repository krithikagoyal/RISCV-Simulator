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

from myRISVSim import reset_proc, load_program_memory, run_RISCVsim
import sys

if __name__ == '__main__':

    # check for correct number of arguments
    '''if len(sys.argv) < 2:
        print("Incorrect number of arguments. Please invoke the simulator \n\t./myRISCVSim <input mc file> \n")
        exit(1)
    

    # set .mc file
    prog_mc_file = sys.argv[1]'''
    prog_mc_file = 'input.mc'

    # reset the processor
    reset_proc()

    # load the program memory
    load_program_memory(prog_mc_file)

    # run the simulator
    run_RISCVsim()
