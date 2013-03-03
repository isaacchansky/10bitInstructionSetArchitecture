import Emulator
import Compiler
import sys

params = sys.argv

print params[0], params[1],params[2]

if(len(params) > 3):
    print "you're doing it wrong"
else:

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

    #search testing...

    elif(params[1] == "search"):
        print "Search Test"
        inputFile = open("search.txt", "r+")
        #Compiler.get_binary("search.txt")

    else:
        print "you're doing it wrong"

    Emulator.exe()
    print "result = ", Emulator.t1[0]
