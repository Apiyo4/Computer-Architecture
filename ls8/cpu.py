"""CPU functionality."""
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg =  [0] * 8
        self.pc = 0
        self.ram = [0]* 256
        self.running = True

    def load(self):
        """Load a program into memory."""
        try:
            address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
            with open(sys.argv[1]) as f:
                for line in f:
                    val = line.split("#")[0].strip()
                    if val == "":
                        continue
                    intVal = int(val, 2)
                    self.ram[address] = intVal
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found!")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, value, address):
        self.ram[address] = value
    def run(self):
        """Run the CPU."""
        
        while self.running:
            ir = self.ram[self.pc]
            instruction_length = ((ir >> 6) & 0b11) + 1
            reg_num1 = self.ram_read(self.pc + 1)
            reg_num2 = self.ram_read(self.pc + 2)
            if ir == HLT:
                self.running = False 
            elif ir == LDI:
                self.reg[reg_num1] = reg_num2
            elif ir == PRN:
                print(self.reg[reg_num1])
            elif ir == MUL:
                self.alu("MUL", reg_num1, reg_num2)
            self.pc += instruction_length