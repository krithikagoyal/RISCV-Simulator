# Functional Simulator for RISCV Processor
### *This project is developed as part of Computer Architecture class and is build in 3 phases.*

## PHASE: 1 (Single cycle execution)
*myRISCVSim.py* file will take .mc file as its argument and is executed as per the functional behaviour of the instructons.
Each instruction will go through the following steps:
1. Fetch
1. Decode
1. Execute
1. Memory access
1. Register update or Writeback

#### This program till now supports below 31 instructions:
* **R Format:** add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem.
* **I Format:** andi, addi, ori, lb, ld, lh, lw, jalr.
* **S Format:** sb, sw, sd, sh.
* **SB Format:** beq, bne, bge, blt.
* **U Format:** auipc, lui.
* **UJ Format:** jal.

#### How to build ?
Run the following commands on the terminal:
```
$ cd src
$ make
```

#### How to execute ?
Run the following command on terminal:
```
myRISCVSim.py test/simple_add.mc
```

#### Directory Structure
