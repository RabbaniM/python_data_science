from random import randint

#how big a number should we guess? 
max_number = 7
first_line = "Guess a number between 1 and %d" % max_number
print(first_line)

number = randint(1, max_number)

not_solved = True

#keep looping unil we guess correctly
while not_solved:
    answer = int(input('?'))
    you_said = "You typed %d" % answer
    print (you_said)
    if answer > number:
        print ("The number is lower")
    elif answer < number:
       print ("The number is higher")
    else:
        print ("You got it right")
        not_solved = False
