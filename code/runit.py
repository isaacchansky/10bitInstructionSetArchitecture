import Emulator
import Compiler
import sys

params = sys.argv

# set flags


if(len(params) > 4):
    print "you're doing it wrong"
else:

    # set flags
    if(len(params) > 3):
        flags = params[3]
        if('a' in flags):
            Emulator.assertions = True
        if('e' in flags):
            Emulator.errors = True
        if('l' in flags):
            Emulator.logs = True
        if('s' in flags):
            Emulator.sleep = True

    #factorial testing...

    if(params[1] == "factorial"):
        print "Factorial Test"
        number = int(params[2])
        inputFile = open("factorialtemplate.txt", "r+")
        outputFile = open("factorialtest.txt", "w")
        addInstr = "ADD $one, $t1\n"
        initInstr = "AND 0 $zero, $t1\n"

        lines = inputFile.readlines()
        lines.reverse()
        for i in range(number):
            lines.append(addInstr)
        lines.append(initInstr)
        lines.reverse()

        for line in lines:
            outputFile.write(line)
        outputFile.close()

        Compiler.get_binary("factorialtest.txt")

        Emulator.exe()
        print "result = ", Emulator.t1[0]


    #search testing...

    elif(params[1] == "search"):
        print "Search Test"
        #inputFile = open("search.txt", "r+")
        Compiler.get_binary("search.txt")
        Emulator.exe()
        print "result = ", Emulator.mem[10]

    else:
        print "you're doing it wrong"

    