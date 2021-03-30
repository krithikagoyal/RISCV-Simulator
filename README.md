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

CS204-Project
* bin
  * myRISCVSim
* doc
  * design-doc.docx
* include
  * myRISCVSim.h
* src
  * main.c
  * Makefile
  * myRISCVSim.h
* test
  * simple_add.mc
  * fib.mc
  * array_add.mc
  * fact.mc
  * bubble.mc
