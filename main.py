# The project is developed as part of Computer Architecture class
# Project Name: Functional Simulator for subset of RISCV Processor

# Developer's Name:
# Developer's Email id:
# Date: 


# main.py
# Purpose of this file: The file handles the input and output, and
# invokes the simulator


from myRISCVSim import *
import sys

if __name__ == '__main__':
    prog_mc_file = ''
    if len(sys.argv) < 2:
        print("Incorrect number of arguments. Please invoke the simulator \n\t./myRISCVSim <input mc file> \n")
        exit(1)
    
    #reset the processor
    reset_proc()

    #load the program memory
    load_program_memory(sys.argv[1])

    #run the simulator
    run_RISCVsim()
