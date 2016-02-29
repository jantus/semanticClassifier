import sys
import time
import hmm
import viterbi
import getopt, sys
from sets import Set



def runRobot():
    states = ["1:2", "1:3", "2:1", "2:3", "2:4", "3:1", "3:2", "3:3", "3:4", "4:1", "4:2", "4:4"]
    
    HMM = hmm.Hmm(states)

    inputFile = open("Assignment5DataSets/robot_no_momemtum.data", 'r')
    state = inputFile.readline().split()
    HMM.updateStartP(state[0])
    HMM.updateEmitP(state[0], state[1])

    prev = state;
    # Building the HMM
    for line in inputFile:
        state = line.split()
        if state[0] == "..":
            # End of test data.
            break

        elif state[0] == '.': 
            # End of sequence, skip this iteration
            prev = state
            continue
        
        elif prev[0] == '.':
            #New sequence
            HMM.updateStartP(state[0])
            HMM.updateEmitP(state[0], state[1])
            prev = state
        else:
            HMM.updateTransP(prev[0], state[0])
            HMM.updateEmitP(state[0], state[1])
            prev = state


    HMM.normalize()



    print "HMM done, run viterbi"  

    vite = viterbi.Viterbi(HMM)
    word = []
    correctStates = []
    result = []

    # counter
    cStates = 0
    cErrors = 0

    cCorrect = 0

    for line in inputFile:
        
        line = line.split()
        if line[0] != '.': 
            cStates += 1
            # End of Sequence
            word.append(line[1]) 
            correctStates.append(line[0])  
        else:
            #word = word
            correctedWord =  vite.viterbi(word)
            for i in xrange(0, len(word)):
                if  correctStates[i] == correctedWord[i]:
                    cCorrect += 1
                else:
                    cErrors +=1

            correctStates = []
            result.append(correctedWord)
            word = []
    
    HMM.printStartP()
    HMM.printTransP()
    HMM.printEmitP()
    
    print "\nSequence: ".join([",".join(l) for l in result ])
    print
    print "States read:     ", cStates
    print "Correct guesses: ", cCorrect
    print "Wrong guesses:   ",  cErrors
    print "Correct guessing rate: ", round(float(cCorrect)/float(cStates)*100,2), "%"
    print "Wrong guessing rate:   ", round(float(cErrors)/float(cStates)*100,2), "%"



    return

def runTypos():
    states = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
              "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    
    HMM = hmm.Hmm(states)

    inputFile = open("Assignment5DataSets/typos10.data", 'r')
    state = inputFile.readline()
    HMM.updateStartP(state[0])
    HMM.updateEmitP(state[0], state[2])

    prev = state;
    # Build HMM
    for state in inputFile: 
        if state[0] == '..' or state[0] == '.':
            # End of test data.
            break

        elif state[0] == '_': 
            # End of word, skip this iteration
            prev = state
            continue
        
        elif prev[0] == '_':
            #New word
            HMM.updateStartP(state[0])
            HMM.updateEmitP(state[0], state[2])
            prev = state
        else:
            HMM.updateTransP(prev[0], state[0])
            HMM.updateEmitP(state[0], state[2])
            prev = state

    HMM.normalize()

    print "HMM done, run viterbi"  
    vite = viterbi.Viterbi(HMM)


    word = []
    correctWord = []
    result = []

    # counter
    cStates = 0
    cErrors = 0

    cCorrect = 0

    for line in inputFile:
        if line[0] != '_': 
            cStates += 1
            word.append(line[2]) 
            correctWord.append(line[0])

            if line[0] != line[2]:
                cErrors += 1;  
        else:
            correctedWord =  vite.viterbi(word)
            
            for i in xrange(0, len(correctWord)):
                if correctWord[i] == correctedWord[i]:
                    cCorrect += 1

            correctWord = []
            result.append("".join(correctedWord))


            word = []

    HMM.printStartP()
    HMM.printTransP()
    HMM.printEmitP()
    print
    print " ".join(result)
    print
    print "Letters read:   ",  cStates
    print "Initial errors: ",  cErrors
    print "Initial error rate: \t", round(float(cErrors)/float(cStates)*100,2), "%"
    print "Corrected Letters: \t", cErrors - (cStates - cCorrect)
    print "Correction rate: \t", round(float(cErrors + cCorrect - cStates) / float(cErrors)*100,2), "%"
    print "Final error rate: \t", round(float(cStates - cCorrect) / float(cStates)*100,2), "%"
    
    
    return

def runTopics():
    states = ["baseball", "cars", "guns", "medicine", "religion", "windows"]

    HMM = hmm.Hmm(states)

    inputFile = open("Assignment5DataSets/topics.data", 'r')
    line = inputFile.readline().split()
    state = line[0]

    HMM.updateStartP(state)

    for word in line[1:]:
        HMM.updateEmitP(state, word)

    prev = state;
    # Build HMM
    for line in inputFile:
        line = line.split()
        state = line[0]
        if state == "..":
            # End of test data.
            break

        else:
            HMM.updateTransP(prev, state)

            for word in line[1:]:
                 HMM.updateEmitP(state, word)

            prev = state


    HMM.normalize()

    print "HMM done, run viterbi"  

    vite = viterbi.Viterbi(HMM)
    word = []
    result = []

    # counter
    cStates = 0
    cErrors = 0

    cCorrect = 0

    for line in inputFile:
        # each line is a new state
        line = line.split()
        if line[0] == '': 
            # End of Stream
            break
        else:
            cStates += 1
            #word = word
            states =  vite.viterbi(line[1:])
            # Most common state
            state = max(set(states), key=states.count)
            if state == line[0]:
                cCorrect += 1
            else:
                cErrors += 1

            result.append(state)
            word = []

    HMM.printStartP()
    HMM.printTransP()
    HMM.printEmitP()
    print
    print "".join(["article"+str(i)+"="+e+", " for i, e in enumerate(result)])
    print
    print "Articles:\t",    cStates
    print "Correct predictions:\t",  cCorrect
    print "Wrong predictions:\t",  cErrors
    print "Correct prediction rate: ", round(float(cCorrect)/float(cStates)*100,2), "%"
    print "Wrong prediction rate:   ", round(float(cErrors)/float(cStates)*100,2), "%"


    return
    

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:o:')
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)


    if len(opts) != 2:
        print "Wrong number of argumetns"

    for opt in opts:
        if opt[0] == '-p':
            problem = int(opt[1])
        else:
            order = int(opt[1])



    if order == 1:
        if problem == 1:
            #Toy robot
            print "Toy robot"
            runRobot()
        elif problem == 2:
            #Typo
            print "Typo correction"
            runTypos()
        elif problem == 3: 
            print "Topic change"
            runTopics()
        else:
            print "Not a valid problem option, must be either 1, 2 or 3"
    elif order == 2:
        print "Funcionality not implemented"
    else:
        print "Not a valid HMM order, must be either 1 or 2"
  


if __name__ == "__main__":
	main()