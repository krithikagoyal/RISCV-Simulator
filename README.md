# Functional Simulator for RISC-V Processor
### *This project is developed as part of Computer Architecture class and is build in 3 phases.*

## PHASE: 1 (Single cycle execution)
*myRISCVSim.py* file will take .mc file as its argument and is executed as per the functional behaviour of the instructons.
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

#### How to run ?
Run the following commands on the terminal:
```
$ python test/bubble_sort.mc
```

#### Directory Structure
```
RISCV-Simulator
  |
  |- doc
      |
      |- design-doc.docx
  |- include
      |
      |- utility.py
  |- src
      |
      |- Instruction_Set_List.csv
      |- main.py
      |- myRISCVSim.py
  |- test
      |
      |- bubble_sort.mc
      |- factorial.mc
      |- fibonacci.mc
      |- Readme.md
      |- TC_1_Fibonacci_Assembly.s
      |- TC_2_Factorial_Assembly.s
      |- TC_1_BubbleSort_Assembly.s
  |
  |- Project-statement.txt
  |- Readme
```

#### Contributors
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
