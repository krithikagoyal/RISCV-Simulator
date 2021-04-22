# Functional Simulator for RISC-V Processor
### *This project is developed as part of Computer Architecture class and is build in 3 phases.*

## Table of Contents
1. [Contributors](https://github.com/Harshiitrpr/RISCV-Simulator#contributors)
2. [Directory Structure](https://github.com/Harshiitrpr/RISCV-Simulator#directory-structure-of-each-phase)
3. [Requirements](https://github.com/Harshiitrpr/RISCV-Simulator#requirements)
4. [Phase 1 (Single Cycle Execution)](https://github.com/Harshiitrpr/RISCV-Simulator#phase-1-single-cycle-execution)
5. [Phase 2 (Pipelined Implementation)](https://github.com/Harshiitrpr/RISCV-Simulator#phase-2-pipelined-implementationn)
6. [How to run ?](https://github.com/Harshiitrpr/RISCV-Simulator#how-to-run-)

## Contributors
```
-------------------------------------------------
| Developer's Name   | Developer's Email ID     |
|-----------------------------------------------|
| Akhil Arya         | 2019csb1066@iitrpr.ac.in |
| Harshwardhan Kumar | 2019csb1089@iitrpr.ac.in |
| Krithika Goyal     | 2019csb1094@iitrpr.ac.in |
| Rhythm Jain        | 2019csb1111@iitrpr.ac.in |
| Tarun Singla       | 2019csb1126@iitrpr.ac.in |
-------------------------------------------------
```

## Directory Structure of each phase
```
RISCV-Simulator
  |
  |- doc
      |
      |- design-doc.docx
  |- src
      |
      |- Gui.py
      |- Instruction_Set_List.csv
      |- main.py
      |- myRISCVSim.py
  |- test
      |
      |- bubble_sort.mc
      |- factorial.mc
      |- fibonacci.mc
      |- TC_1_Fibonacci_Assembly.s
      |- TC_2_Factorial_Assembly.s
      |- TC_1_BubbleSort_Assembly.s
      |- Test.md
  |
  |- Project-statement.txt
  |- README
```

## Requirements
This simulator is built using Python.
The user must install python3 and all libraries stated in requirements.txt.

Run the following command in the terminal in the main directory to install all
the requirements of the project after installing python.
```
pip install -r requirements.txt
```

## PHASE 1 (Single Cycle Execution)
*myRISCVSim.py* file will take .mc file as its argument and is executed as per the functional behaviour of the instructions.
Each instruction will go through the following steps:
1. Fetch
1. Decode
1. Execute
1. Memory access
1. Register update or Writeback

#### The simulator supports below 29 instructions:
* **R Format:** add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem.
* **I Format:** andi, addi, ori, lb, lh, lw, jalr.
* **S Format:** sb, sw, sh.
* **SB Format:** beq, bne, bge, blt.
* **U Format:** auipc, lui.
* **UJ Format:** jal.

As an output, the simulator writes the updated memory contents in a "data_out.mc"
file. A "reg_out.mc" file is also produced containing the contents of the
registers. Additionally, the simulator also prints messages for each stage about
what it is doing in that stage and the number of clock cycles after each cycle.

## PHASE 2 (Pipelined Implementation)
The simulator now supports pipelined implementation also. Various knobs can be set by
the user to enable/disable pipelining, forwarding, printing register file, and printing
pipeline registers for all or a specific instruction.

At the end of the execution, the simulator prints various insightful statistics.

## How to run ?
For any phase,
1. Place your input .mc file(new ones if any) in the test directory.
2. Run the following command on the terminal in the src directory:
```
$ python main.py
```

A GUI window opens. Select the input file in the GUI. The program runs and the
GUI window opens again to show the updated memory and register contents.
