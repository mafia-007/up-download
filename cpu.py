__author__ = 'eamars'

import time

# The virtual cpu has 16 32-bit general propose registers, some
# status registers, one program counter and some memory
# Three and two address instructions are supported

MAX_UNSIGNED_INT = 2**32-1
MIN_UNSIGNED_INT = 0

# General propose registers
GPR = [None] * 16

# SRAM
SRAM = [None] * 1024

# Status Registers
REG_PC = 0
REG_Z = 0
REG_O = 0
REG_N = 0


# Instruction set

# Arithmetic
ADD = "ADD"
SUB = "SUB"
MUL = "MUL"

# Logical operators
ORR = "ORR"
EOR = "EOR"
AND = "AND"

# Comparisons
CMP = "CMP"     # O1 - O2

# Branch
BEQ = "BEQ"     # jump if REG_ZERO
B   = "B"       # unconditional jump

# Data management
MOV = "MOV"

# RESET
RESET = "RESET"


def add(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op3 = instruction[1]
    op1 = instruction[2]
    op2 = instruction[3]

    op1_value = 0
    if op1[0] == "#":     # Immediate number, eg, #12
        op1_value = int(op1[1:])
    else:                   # Register, eg, R1
        op1_value = GPR[int(op1[1:])]

    op2_value = 0
    if op2[0] == "#":     # Immediate number, eg, #12
        op2_value = int(op2[1:])
    else:                   # Register, eg, R1
        op2_value = GPR[int(op2[1:])]

    result = op1_value + op2_value

    if result > MAX_UNSIGNED_INT:
        result -= MAX_UNSIGNED_INT

    REG_O = 1

    GPR[int(op3[1:])] = result

    REG_PC += 1


def sub(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op3 = instruction[1]
    op1 = instruction[2]
    op2 = instruction[3]

    op1_value = 0
    if op1[0] == "#":     # Immediate number, eg, #12
        op1_value = int(op1[1:])
    else:                   # Register, eg, R1
        op1_value = GPR[int(op1[1:])]

    op2_value = 0
    if op2[0] == "#":     # Immediate number, eg, #12
        op2_value = int(op2[1:])
    else:                   # Register, eg, R1
        op2_value = GPR[int(op2[1:])]

    result = op1_value - op2_value

    if result < 0:
        result *= -1

    REG_N = 1

    GPR[int(op3[1:])] = result

    REG_PC += 1


def mul(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op3 = instruction[1]
    op1 = instruction[2]
    op2 = instruction[3]

    op1_value = 0
    if op1[0] == "#":     # Immediate number, eg, #12
        op1_value = int(op1[1:])
    else:                   # Register, eg, R1
        op1_value = GPR[int(op1[1:])]

    op2_value = 0
    if op2[0] == "#":     # Immediate number, eg, #12
        op2_value = int(op2[1:])
    else:                   # Register, eg, R1
        op2_value = GPR[int(op2[1:])]

    result = op1_value * op2_value

    if result > MAX_UNSIGNED_INT:
        result -= MAX_UNSIGNED_INT

    REG_O = 1

    GPR[int(op3[1:])] = result

    REG_PC += 1


def cmp(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op1 = instruction[1]
    op2 = instruction[2]

    op1_value = 0
    if op1[0] == "#":     # Immediate number, eg, #12
        op1_value = int(op1[1:])
    else:                   # Register, eg, R1
        op1_value = GPR[int(op1[1:])]

    op2_value = 0
    if op2[0] == "#":     # Immediate number, eg, #12
        op2_value = int(op2[1:])
    else:                   # Register, eg, R1
        op2_value = GPR[int(op2[1:])]

    result = op1_value - op2_value

    if result == 0:
        REG_Z = 1
    else:
        REG_Z = 0

    REG_PC += 1


def beq(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op1 = instruction[1]

    offset = 0
    if op1[0] == "#":     # Immediate number, eg, #12
        offset = int(op1[1:])
    else:                   # Register, eg, R1
        offset = GPR[int(op1[1:])]

    if REG_Z == 1:
        REG_Z = 0
        REG_PC = offset
    else:
        REG_PC += 1


def b(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op1 = instruction[1]

    offset = 0
    if op1[0] == "#":     # Immediate number, eg, #12
        offset = int(op1[1:])
    else:                   # Register, eg, R1
        offset = GPR[int(op1[1:])]

    REG_PC = offset


def mov(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    op1 = instruction[1]
    op2 = instruction[2]

    op2_value = 0
    if op2[0] == "#":     # Immediate number, eg, #12
        op2_value = int(op2[1:])
    else:                   # Register, eg, R1
        op2_value = GPR[int(op2[1:])]

    GPR[int(op1[1:])] = op2_value

    REG_PC += 1


def reset(instruction):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    init()
    for i in range(len(GPR)):
        GPR[i] = None

    REG_PC += 1


def cpu(program):
    global REG_PC
    global REG_Z
    global REG_O
    global REG_N

    while True:
        instruction = program[REG_PC].split()
        print(REG_PC, instruction)

        op = instruction[0]

        if op == ADD:
            add(instruction)
        elif op == SUB:
            sub(instruction)
        elif op == MUL:
            mul(instruction)
        elif op == ORR:
            pass
        elif op == EOR:
            pass
        elif op == AND:
            pass
        elif op == CMP:
            cmp(instruction)
        elif op == BEQ:
            beq(instruction)
        elif op == B:
            b(instruction)
        elif op == MOV:
            mov(instruction)
        elif op == RESET:
            reset(instruction)

        print(GPR)
        time.sleep(1)


def init():
    REG_PC = 0
    REG_Z = 0
    REG_O = 0
    REG_N = 0

if __name__ == "__main__":
    program = [
        "RESET",
        "MOV R0 #1",        # int a = 0;
        "MOV R1 #3",        # int b = 3;
        "ADD R2 R0 R1",     # int c = a + b;
        "MOV R3 #4",        # int d = 4;
        "CMP R3 R2",        # if (d == c)
        "BEQ #9",           #
        "MOV R15 #233",     # e = 233;
        "B #0",             #
        "MOV R14 #233",     # f = 233;
        "B #0"
    ]
    cpu(program)

