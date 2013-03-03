opcodes   = {"ADD"   : "000",
             "AND"   : "001",
             "STORE" : "010",
             "LOAD"  : "011",
             "SLL"   : "100",
             "BEQ"   : "101",
             "HALT"  : "110",
             "TBD"   : "111"
             }

registers = {"$t1"         : "0000",
             "$t2"         : "0001",
             "$t3"         : "0010",
             "$t4"         : "0011",
             "$t5"         : "0100",
             "$t6"         : "0101",
             "$beq1"       : "0110",
             "$zero"       : "0111",
             "$beq2"       : "1000",
             "$one"        : "1001",
             "$negone"     : "1010",
             "$nine"       : "1011",
             "$sixteen"    : "1100",
             "$fortyeight" : "1101",
             "$load"       : "1110"
             }


def get_binary(progIn):
    progIn = open(progIn, "r+")
    progOut = open("compilerOut.txt", "w")

    count = 1
    labels = {}

    data = progIn.readlines()
    for x in range(len(data)):
        count += 1
        inputLine = data[x].split()

        if inputLine == []:
            count -= 1
        else:
            if inputLine[0].find(":") != -1:
                count -= 1
                # add {Labels# : count(base 2)} to the labels dictionary .  b's show up for some reason so i replace them
                num = bin(count)
                ind = num.find("b")
                num = num[ind+1:len(num)].zfill(5)
                labels[inputLine[0] + "\n"] = num

    count = 0
    print labels
    for line in data:

        if labels.has_key(line) or line == '\n':
            continue

        count += 1

        ind = line.find("#")
        if ind != -1:
            line = line[0:ind]

        inputLine = line.split()
        outputLine = []

#        print line
        for x in range(len(inputLine)):
            inputLine[x] = inputLine[x].replace(",", "")

            if x == 0:
                if not(opcodes.has_key(inputLine[x])):
                    print "Error on line", count, ":", "\n    unknown instruction ", inputLine[x]
                    return
                outputLine.append(opcodes.get(inputLine[x]))
# AND instruction
            if inputLine[0] == "HALT":
                if x == 0:
                    outputLine.append("0000000")

            if inputLine[0] == "AND":

                if x == 0:
                    if (len(inputLine) != 4):
                        print "Error on line", count, ":", "\n    wrong number of args for an AND instr"
                        return

                if x == 1:
                    if inputLine[x] != '0' and inputLine[x] != '1':
                        print "Error on line", count, ":", "\n    first arg of an AND instr must be a 1 or 0, got ", [inputLine[x]]
                        return
                    outputLine.append(inputLine[x])
                if x == 2:
                    if inputLine[x][1] != 't' and inputLine[x] != '$zero' and inputLine[x] != '$beq1':
                        print "Error on line", count, ":\n    second arg of an AND instr must be reg 1-8, got ", [inputLine[x]]
                        return

                    outputLine.append(registers.get(inputLine[x])[1:4])

                if x == 3:
                    if inputLine[x][1] != 't' and inputLine[x] != '$zero' and inputLine[x] != '$beq1':
                        print "Error on line", count, ":\n    third arg of an AND instr must be reg 1-8, got ", [inputLine[x]]
                        return
                    outputLine.append(registers.get(inputLine[x])[1:4])
#SHIFT and ADD
            elif inputLine[0] == "SLL" or inputLine[0] == "ADD":

                if x == 0:
                    if (len(inputLine) != 3):
                        print "Error on line", count, ":", "\n    wrong number of args for an SHIFT/ADD instr"
                        return

                if x == 1:
                    if not(registers.has_key(inputLine[x])):
                        print "Error on line", count, ":\n    second arg of an ADD/SHIFT instr must be a reg, got", [inputLine[x]]
                        return
                    outputLine.append(registers.get(inputLine[x]))

                if x == 2:
                    if inputLine[x][1] != 't' and inputLine[x] != '$zero' and inputLine[x] != '$beq1':
                        print "Error on line", count, ":\n    third arg of an ADD/SHIFT instr must be reg 1-8, got ", [inputLine[x]]
                        return
                    outputLine.append(registers.get(inputLine[x])[1:4])

            elif inputLine[0] == "LOAD":
                if x == 0:
                    if (len(inputLine) != 4):
                        print "Error on line", count, ":", "\n    wrong number of args for a LOAD instr"
                        return

                if x == 1:
                    if inputLine[x] != '0' and inputLine[x] != '1':
                        print "Error on line", count, ":", "\n    first arg of a LOAD instr must be a 1 or 0, got ", [inputLine[x]]
                        return
                    outputLine.append(inputLine[x])

                if x == 2:
                    if inputLine[x] != '0' and inputLine[x] != '1':
                        print "Error on line", count, ":", "\n    second arg of a LOAD instr must be a 1 or 0, got ", [inputLine[x]]
                        return
                    outputLine.append(inputLine[x])

                if x == 3:
                    if not(registers.has_key(inputLine[x])):
                        print "Error on line", count, ":\n    third arg of a LOAD instr must be a reg, got", [inputLine[x]]
                        return

                    outputLine.append('0' + registers.get(inputLine[x]))

            elif inputLine[0] == "STORE":
                if x == 0:
                    pass
                if x == 1:
                    if inputLine[x] != '0' and inputLine[x] != '1':
                        print "Error on line", count, ":", "\n    first arg of a STORE instr must be a 1 or 0, got ", [inputLine[x]]
                        return
                    outputLine.append(inputLine[x])

                if x == 2:
                    if inputLine[1] == '1':  # stack
                        if len(inputLine) != 4:
                            print "Error on line", count, ":", "\n    wrong number of args for a STORE to STACK instr"
                            return
                        if inputLine[x] != '0' and inputLine[x] != '1':
                            print "Error on line", count, ":", "\n    second arg of a STORE to STACK instr must be a 1 or 0, got ", [inputLine[x]]
                            return

                        outputLine.append(inputLine[x])

                    else:
                        if len(inputLine) != 3:
                            print "Error on line", count, ":", "\n    wrong number of args for a STORE to MEM instr"
                            return

                        if not(registers.has_key(inputLine[x])):
                            print "Error on line", count, ":\n    third arg of a LOAD instr must be a reg, got", [inputLine[x]]
                            return

                        outputLine.append('00' + registers.get(inputLine[x]))

                if x == 3:  # must be storing to stack
                    if inputLine[1] == '1':
                        if not(labels.has_key(inputLine[x]+'\n')):
                            print "Error on line", count, ":", "\n    unknown label to STORE to STACK, got ", [inputLine[x]]
                            return
                        print count
                        outputLine.append(labels.get(inputLine[x]+'\n'))

            elif inputLine[0] == "BEQ":
                if x == 0:
                    if (len(inputLine) != 4):
                        print "Error on line", count, ":", "\n    wrong number of args for a BEQ instr"
                        return

                if x == 1:
                    if inputLine[x] != '$beq1' and inputLine[x] != '$zero':
                            print "Error on line", count, ":", "\n    first arg of a BEQ instr must be $beq1 or $zero, got ", [inputLine[x]]
                            return

                    if inputLine[x] == "$beq1":
                        outputLine.append("1")
                    else:
                        outputLine.append("0")

                if x == 2:
                    if inputLine[x] != '$zero' and inputLine[x] != '$beq2' and inputLine[x] != '$one' and inputLine[x] != '11':
                            print "Error on line", count, ":", "\n    first arg of a BEQ instr must be $beq1 or $zero, got ", [inputLine[x]]
                            return

                    if inputLine[x] == "$zero":
                        outputLine.append("00")

                    elif inputLine[x] == "$one":
                        outputLine.append("01")

                    elif inputLine[x] == "$beq2":
                        outputLine.append("10")

                    else:
                        outputLine.append("11")

                if x == 3:
                    if inputLine[2] != "11":
                        num = abs(int(labels.get(inputLine[x] + '\n'), 2) - count)
                        num = bin(num).replace("b", "0").zfill(6)
                        num = num[2:len(num)]
                        if int(labels.get(inputLine[x] + '\n'), 2) < count:
                            num += "-"
                        if not(labels.has_key(inputLine[x]+'\n')):
                            print "Error on line", count, ":", "\n    unknown label for BEQ, got ", [inputLine[x]]
                            return
                        outputLine.append(num)
                    else:
                        if not(registers.has_key(inputLine[x])):
                            print "Error on line", count, ":\n    last arg of special case BEQ must be a reg, got", [inputLine[x]]
                            return
                        outputLine.append(registers.get(inputLine[x]))
#                    STORE [1 bit condition <memory[10] or stack>] [6 bits for offset] #mem
#        OR
#  STORE [1 bit condition <memory[10] or stack>] [1 bit to store $t4 or $beq1] [5 bits] # 5 bits for hardcoded offset (program conter)

        print inputLine, "input"
        print outputLine, " output"
        progOut.writelines(outputLine + ["\n"])

if __name__ == '__main__':
    get_binary("factorial.txt")
