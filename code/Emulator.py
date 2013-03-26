import copy
import time

logger = True
errors = False
logs = False
assertions = False
sleep = False
verboseLog = False

t1 = [None]
t2 = [None]
t3 = [None]
t4 = [None]
t5 = [None]
t6 = [None]
beq1 = [None]
zero = [0]
beq2 = [None]
one = [1]
negone = [-1]
nine = [9]
sixteen = [16]
fortyeight = [48]
load = [None]

#mem9 = [None]
#mem10 = [None]

# 9 and 10 are special...
mem = []
for i in range(200):
    mem.append("00000000")

mem[9] = "11111111" # what we are searching for... hardcoded for now...

#sample array to search in...
mem[96] = "01000000"
mem[97] = "11110011"
mem[98] = "11010100"
mem[99] = "00101001"
mem[100] = "11000110"
mem[101] = "10010010"
mem[102] = "00101001"
mem[103] = "11000110"
mem[104] = "10010010"
mem[105] = "01000000"
mem[106] = "11110011"
mem[107] = "11010100"
mem[108] = "00101001"
mem[109] = "11000110"
mem[110] = "10010010"
mem[111] = "00101001"
mem[112] = "11000110"
mem[113] = "10010010"
mem[114] = "01000000"
mem[115] = "11110011"
mem[116] = "11010100"
mem[117] = "00101001"
mem[118] = "11000110"
mem[119] = "10010010"
mem[120] = "00101001"
mem[121] = "11000110"
mem[122] = "10010010"
mem[123] = "01000000"
mem[124] = "11110011"
mem[125] = "11010100"
mem[126] = "00101001"
mem[127] = "11000110"
mem[128] = "10010010"
mem[129] = "00101001"
mem[130] = "11000110"
mem[131] = "10010010"
mem[132] = "11000110"
mem[133] = "10010010"
mem[134] = "11000110"
mem[135] = "10010010"
mem[136] = "11000110"
mem[137] = "11000110"
mem[138] = "11111111"


#convert to integers
for i in range(len(mem)):
    mem[i] = int(mem[i],2)
stack = []



def addInstr(arg1, arg2, arg3):
    log("l", "ADD")
    log("a", ((registers.get(arg1),registers.get(arg2),registers.get(arg3))))
    firstReg = registers.get(arg1)
    secondReg = registers.get("0" + arg2)
    secondReg[0] = secondReg[0] + firstReg[0]


def andInstr(arg1, arg2, arg3):
    log("l", "AND")
    firstReg = registers.get("0" + arg2)
    secondReg = registers.get("0" + arg3)

    if arg1 == '0':
        secondReg[0] = firstReg[0]
    elif arg1 == '1':
        beq2[0] = firstReg[0] & secondReg[0]
    else:
        message = "incorrect first argument in AND: ", arg1
        log("e", message)
        return


def storeInstr(arg1, arg2, arg3):
    log("l", "STORE")
    if arg1 == '0':     # implicit mem[10]
        reg = registers.get(arg2[2:6])
        message = "put "+str(reg[0])+"int mem[10]"
        log("a", message)
        mem[10] = reg[0]
    elif arg1 == '1':
        if arg2 == '0':  # beq1
            stack.append(arg3)
        elif arg2 == '1':  # t4
            stack.append(arg3)


def loadInstr(arg1, arg2, arg3):
    log("l", "LOAD")
    if arg1 == "1":  # load from the stack. arg2 ignored, arg3 is position
        secondReg = registers.get(arg3[1:5])
        message = "stack: "+str(stack)
        log("l", message)
        load[0] = stack.pop()
    elif arg1 == "0":  # loading from memory

        if arg2 == '1':  # load from middle
            #convert to binary string and format
            w1 = bin(mem[96+t2[0]])[2:].zfill(8)
            w2 = bin(mem[96+t2[0]+1])[2:].zfill(8)
            word = w1[4:]+w2[:4]
            log("a","loading from middle of word: '"+word+"'")
            #binary string only used for merging and display... back to integers...
            load[0] = int(word,2)

        elif arg2 == '0':  # load from start

             #special case, if arg3 is $negone, just load from mem[9]
            if arg3[1:] == "1010":
                log("a", "loading from mem[9]")
                load[0] = int(mem[9])
            else:
                log("a", str((arg1, arg2, arg3)))
                load[0] = mem[96+t2[0]]
                log("a","loading from start of word: '"+bin(load[0])[2:].zfill(8)+"'")


        else:
            message = "incorrect second argument in LOAD: ", arg1
            log("e", message)
            return
    else:
        message = "incorrect first argument in LOAD: ", arg1
        log("e", message)
        return


def shiftInstr(arg1, arg2, arg3):
    log("l", "SHIFT")
    firstReg = registers.get(arg1)  # shift amaount
    secondReg = registers.get("0" + arg2)
    secondReg[0] = secondReg[0] << firstReg[0]
    if secondReg[0] > 65536:
        # convert to binary, get rightmost 16 bits, convert back
        binaryNum = bin(secondReg[0])[2:][-16:]
        secondReg[0] = int(binaryNum, 2)    #convert back to integer before assigning
        log("l", "zeroed out register via shift")


def beqInstr(arg1, arg2, arg3):

    if arg2 == "11":  # specialcase
        message = "t1 = ",t1
        log("l", message)
        reg = registers.get(arg3[0:4])  # shift amount
        message = "shamt "+str(reg[0])
        log("l", message)
        if reg[0] == 1:
            return 1
        else:
            return int(reg[0], 2)
    else:
        if arg1 == '0':
            firstArgument = zero[0]
        else:
            firstArgument = beq1[0]

        if arg2 == "00":
            secondArgument = zero[0]
        elif arg2 == "10":
            secondArgument = beq2[0]
        elif arg2 == "01":
            secondArgument = one[0]

        message = "BEQ: compare "+\
        str(firstArgument)+ " w/ "+\
        str(secondArgument)
        log("l", message)

        if firstArgument == secondArgument:
            if arg3.find("-") != -1:
                return -1-int(arg3[0:4], 2)
            else:
                return int(arg3[0:4], 2)-1
        else:
            return 0


def haltInstr(arg1, arg2, arg3):
    log("l", "HALTED")
    return


def tbdInstr(arg1, arg2, arg3):
    log("l", "TBD")










opcodes   = {"000": addInstr,
             "001": andInstr,
             "010": storeInstr,
             "011": loadInstr,
             "100": shiftInstr,
             "101": beqInstr,
             "110": haltInstr,
             "111": tbdInstr,
             }

registers = {"0000": t1,
             "0001": t2,
             "0010": t3,
             "0011": t4,
             "0100": t5,
             "0101": t6,
             "0110": beq1,
             "0111": zero,
             "1000": beq2,
             "1001": one,
             "1010": negone,
             "1011": nine,
             "1100": sixteen,
             "1101": fortyeight,
             "1110": load,
             }








def exe():
    prog = open("compilerOut.txt", "r")
    instructionCount = 0
    programCount = 1
    lines = prog.readlines()
    message = "lines "+str(lines)
    log("l", message)
    progLength = len(lines)

    while programCount <= progLength:
        instructionCount += 1
        log('l', "IC = "+str(instructionCount))

        if verboseLog:
            logAll()
        if sleep:
            time.sleep(0.5)

        message = "PC = "+str(programCount)
        log("l", message)
        line = lines[programCount-1]
        programCount += 1
        op = line[0:3]
        func = opcodes.get(op)

        arg1, arg2, arg3 = None, None, None
        if (opcodes.get(op) == addInstr) or (opcodes.get(op) == shiftInstr):
            arg1 = line[3:7]
            arg2 = line[7:10]

        elif (opcodes.get(op) == andInstr):
            arg1 = line[3]
            arg2 = line[4:7]
            arg3 = line[7:10]

        elif (opcodes.get(op) == storeInstr):
            arg1 = line[3]  # if zero goto mem
            if arg1 == '0':
                arg2 = line[4:10]
            else:
                arg2 = line[4]
                arg3 = line[5:10]

        elif (opcodes.get(op) == loadInstr):
            arg1 = line[3]
            arg2 = line[4]
            arg3 = line[5:10]

        elif (opcodes.get(op) == beqInstr):
            arg1 = line[3]
            arg2 = line[4:6]
            arg3 = line[6:len(line)]

        if func:
#            try:
            if func == beqInstr:
                if arg2 == "11":
                    programCount = func(arg1, arg2, arg3)
                else:
                    programCount += func(arg1, arg2, arg3)
            elif func == haltInstr:
                message = "DONE, t1 = ", t1
                log("a", message)
                log("l", message)
                return
            else:
                func(arg1, arg2, arg3)

        else:
            message = "Error on line ", programCount, " unknown function call: ", op
            log("e", message)
    pass

def log(type, arg):
    if logger:
        if type == "e" and errors:
            print "ERR: ",arg
        elif type == "a" and assertions:
            print ">>> ", arg
        elif type == "l" and logs:
             print  ">",arg

def logAll():
    print "REGISTERS:\n",\
    "t1 = ", registers.get("0000"),"\n",\
    "t2 = ", registers.get("0001"),"\n",\
    "t3 = ", registers.get("0010"),"\n",\
    "t4 = ", registers.get("0011"),"\n",\
    "t5 = ", registers.get("0100"),"\n",\
    "t6 = ", registers.get("0101"),"\n",\
    "beq1 = ", registers.get("0110"),"\n",\
    "zero = ", registers.get("0111"),"\n",\
    "beq2 = ", registers.get("1000"),"\n",\
    "one = ", registers.get("1001"),"\n",\
    "negone = ", registers.get("1010"),"\n",\
    "nine = ", registers.get("1011"),"\n",\
    "sixteen = ", registers.get("1100"),"\n",\
    "fortyeight = ", registers.get("1101"),"\n",\
    "load = ", registers.get("1110"),"\n"



if __name__ == '__main__':
    exe()

