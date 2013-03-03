import copy

t1          = [None]
t2          = [None]
t3          = [None]
t4          = [None]
t5          = [None]
t6          = [None]
beq1        = [None]
zero        = [0]
beq2        = [None]
one         = [1]
negone      = [-1]
nine        = [9]
sixteen     = [16]
fortyeight  = [48]
load        = [None]

mem10       = [None]

stack       = [1234, 123212]


def addInstr(arg1, arg2, arg3):
    print "Add"
    firstReg = registers.get(arg1)
    secondReg = registers.get("0" + arg2)
    secondReg[0] = secondReg[0] + firstReg[0]
    

def andInstr(arg1, arg2, arg3):
    print "AND"
    firstReg = registers.get("0" + arg2)
    secondReg = registers.get("0" + arg3)
    if arg1 == '0':        
        print "here"
        secondReg[0] = firstReg[0]
    elif arg1 == '1':
        beq2[0] = firstReg[0] & secondReg[0]
    else:
        print "error, incorrect first argument in AND: ", arg1; return
        

def storeInstr(arg1, arg2, arg3):
    print "STORE"
    if arg1 == '0': #implicit mem[10]        
        reg = registers.get(arg2[2:6])
        mem10[0] = reg[0]
    elif arg1 == '1':
        if arg2 == '0': #beq1
            stack.append(arg3)
        elif arg2 == '1': #t4
            stack.append(arg3)

def loadInstr(arg1, arg2, arg3):
    print "LOAD"
    if arg1 == "1": #load from the stack. arg2 ignored, arg3 is position
        secondReg = registers.get(arg3[1:5])
        load[0] = stack.pop()        
        print load, " = load"
    elif arg1 == "0": #loading from memory
        if arg2 == '1': #load from middle
            pass
        elif arg2 == '0': #load from start
            pass
        else:
            print "error, incorrect second argument in LOAD: ", arg1; return
    else:
        print "error, incorrect first argument in LOAD: ", arg1; return
        
def shiftInstr(arg1, arg2, arg3):
    print "shift"
    firstReg = registers.get(arg1) #shift amaount
    secondReg = registers.get("0" + arg2)
    secondReg[0] = secondReg[0]  << firstReg[0]    
    if secondReg[0] > 65536:
        secondReg[0] = 0

def beqInstr(arg1, arg2, arg3):
    print "BEQ"
    print [arg3]
    if arg2 == "11": #specialcase
        print "ASFDGASDFASDFASDF"
        reg = registers.get(arg3[0:4]) #shift amaount
        print reg, "reg"
        
        return reg[0]
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
            
#        print firstArgument, secondArgument
        
        if firstArgument == secondArgument:
            if arg3.find("-") != -1:
#                print "returned", -1-int(arg3[0:4], 2)
                return -1-int(arg3[0:4], 2)
            else:
#                print "returned", int(arg3[0:4], 2)
                return int(arg3[0:4], 2)
        else:
#            print 0
            return 0
            
            

def haltInstr(arg1, arg2, arg3):
    print "halted"
    return

def tbdInstr(arg1, arg2, arg3):
    print "tbd"

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

import time
def exe():
    prog = open("compilerOut.txt", "r")
    
    programCount = 0
    lines = prog.readlines()
    print lines
    progLength =  len(lines)
    
    while programCount <= progLength:
#        time.sleep(.1)
        line = lines[programCount-1]
        programCount += 1
        
        op = line[0:3]
        func = opcodes.get(op)
        
        arg1, arg2, arg3 = None, None, None     
        if (opcodes.get(op) == addInstr) or (opcodes.get(op) == shiftInstr):
            arg1 = line[3:7]
            arg2 = line[7:10]
        
        elif   (opcodes.get(op) == andInstr):
            arg1 = line[3]
            arg2 = line[4:7]
            arg3 = line[7:10]
        
        elif (opcodes.get(op) == storeInstr):
            arg1 = line[3] #if zero goto mem
            if arg1 == '0':
                arg2 = line[4:10]
            else:
                arg2 = line[4]
                arg3 = line[5:10]     
            
        
        elif   (opcodes.get(op) == loadInstr):
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
            else:
                func(arg1, arg2, arg3)
#            except Exception as inst:
#                print "Error executing ", func.__name__, " on line", programCount," :", inst
#                return
        else:
            print "Error on line ", programCount, " unknown function call: ", op
        
    pass
if __name__ == '__main__':
    exe()
    print t1