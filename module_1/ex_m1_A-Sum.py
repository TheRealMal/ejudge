from string import digits

sum = 0

while True:
    try:
        inp = input()
    except EOFError:
        break
    digitMode, flagNegative = False, False
    startIndex = 0
    for i in range(len(inp)):
        if inp[i] in digits:
            if not digitMode: # Remember first digit index
                if flagNegative:
                    startIndex = i - 1
                else:
                    startIndex = i
                digitMode = True
        elif inp[i] == "-":
            if digitMode: # Add number to sum 
                sum += int(inp[startIndex:i])
                digitMode = False
            flagNegative = True # Next number will be negative
        elif digitMode: # Number end; Add to sum
            sum += int(inp[startIndex:i])
            digitMode, flagNegative = False, False
        else: 
            digitMode, flagNegative = False, False
    if digitMode: # Adds to sum if last symbol is digit
        sum += int(inp[startIndex:])

print(sum)