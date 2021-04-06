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

if __name__ == '__main__':
    # set .mc file
    prog_mc_file = take_input()

    # reset the processor
    reset_proc()

    # load the program memory
    load_program_memory(prog_mc_file)

    # run the simulator
    run_RISCVsim()

    # display the data
    display()