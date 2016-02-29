import math
import sys


class Hmm:
    # state is alway a string
    start_p = []
    trans_p = []
    emit_p = []
    states = {} # state:index
    numStates = 0
    alphabet = []

    def __init__(self, states):
        self.alphabet = states;
        self.createStates(states)
        self.numStates = len(self.states)

        self.start_p = [1.0]*self.numStates;

        # initialize matrices.
        for i in xrange(0, self.numStates):
            trans = list()
            for j in xrange(0, self.numStates):
                trans.append(1.0)
            self.trans_p.append(trans)

        self.createEmitP(states)


    def createStates(self, states):
        for i, state in enumerate(states):
            self.states[state] = i;

    def createEmitP(self, states):
        for s in states:
            self.emit_p.append({})
    

    def normalize(self):
        # normalize Initials
        s = sum(self.start_p)
        self.start_p = [math.log(i/s) for i in self.start_p]

        # normalize Transition matrix
        for i, line in enumerate(self.trans_p):
            s = sum(line)
            self.trans_p[i] = [math.log(x/s) for x in line]

        # normailzie output matrix
        for i, dic in enumerate(self.emit_p):
            s = sum(dic.values())
            for key, val in dic.iteritems():
                dic[key] = math.log(val/s)
            # to be able to represent situations not observed
            dic['low'] = math.log(1.0/s)   


    def updateStartP(self, state):
        self.start_p[self.states[state]] += 1

    def updateTransP(self, previous, state):
        row = self.states[previous]
        col = self.states[state]
        self.trans_p[row][col] += 1

    def updateEmitP(self, state, output):
        index = self.states[state]
        dic = self.emit_p[index]
        value  = dic.get(output)
        if value == None:
            dic[output] = 2.0 # start with two for Laplace smothening
        else:
            dic[output] = value + 1.0

    def getStartP(self, state):
        return self.start_p[self.states[state]]

    def getTransP(self, previous, state):
        row = self.states[previous]
        col = self.states[state]
        return self.trans_p[row][col]
        
    def getEmitP(self, state, output):
        row = self.states[state]
        dic = self.emit_p[row]
        value = dic.get(output)
        if not value:
            # if the probability hasn't been observed
            value = dic['low']
        return value

    #Returns the number of states in this HMM.
    def getNumStates(self):
        return self.numStates

    #Returns the number of output symbols for this HMM.
    def getNumOutputs(self):
        return self.numStates     



    def printStartP(self):
        print "\nStart probabilities"
        for i, elem in enumerate(self.start_p):
            print self.alphabet[i], elem

    def printTransP(self):
        print "\nTransition probabilities"
        print "The numbers are rounded in the print but not in the calculations"
        for i, l in enumerate(self.trans_p):
            sys.stdout.write(self.alphabet[i]+" =  ")
            for key, val in enumerate(l):
                sys.stdout.write(self.alphabet[key]+":%.3f  " % (val))
            sys.stdout.write("\n\n")


    def printEmitP(self):
        print "\nEmit probabilities"
        print "The numbers are rounded in the print but not in the calculations"
        for i, dic in enumerate(self.emit_p):
            sys.stdout.write(self.alphabet[i]+" =  ")
            for key, val in dic.iteritems():
                sys.stdout.write(key+":%.3f  " % (val))
            sys.stdout.write("\n\n")
        


