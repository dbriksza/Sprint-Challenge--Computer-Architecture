"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
E=0
L=0
G=0


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = [0] * 8
        self.branchtable = {}
        self.branchtable[LDI] = self.do_LDI
        self.branchtable[PRN] = self.do_PRN
        self.branchtable[HLT] = self.do_HLT
        self.branchtable[CMP] = self.do_CMP
        self.branchtable[JEQ] = self.do_JEQ
        self.branchtable[JNE] = self.do_JNE
        self.branchtable[JMP] = self.do_JMP

    def ram_read(self, location):
        if location <= 256:
            return self.ram[location]

    def ram_write(self, location, information):
        if location <= 256:
            self.ram[location] = information

    def load(self, path):
        """Load a program into memory."""
        

        address = 0


        with open(path) as file:
            for line in file:
                if line[0] != "#" and line !='\n':
                    self.ram[address] = int(line[:8], 2)
                    address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def do_LDI(self):
        reg = self.ram_read(self.pc + 1)
        num = self.ram_read(self.pc + 2)
        self.reg[reg] = num
        self.pc += 3

    def do_PRN(self):
        reg = self.ram_read(self.pc + 1)
        num = self.reg[reg]
        print(num)
        self.pc += 2

    def do_HLT(self):
        sys.exit(1)

    def do_CMP(self):
        if self.reg[self.ram_read(self.pc+1)] == self.reg[self.ram_read(self.pc+2)]:
            E=1
            L=0
            G=0
            self.fl = 0b00000001
        else:
            E=0
            L=0
            G=0
            self.fl = 0b00000000
        self.pc += 3

    def do_JEQ(self):
        if self.fl == 0b00000001:
            reg = self.ram_read(self.pc + 1)
            self.pc = self.reg[reg]
        else:
            self.pc+=2

    def do_JNE(self):
        if self.fl == 0b00000000:
            reg = self.ram_read(self.pc + 1)
            self.pc = self.reg[reg]
        else:
            self.pc+=2

    def do_JMP(self):
        reg = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg]


    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram[self.pc]
            self.branchtable[IR]()

                
