class Viterbi:
    # This is the constructor for this class, which takes as input a
    # given HMM with respect to which most likely sequences will be
    # computed.
    hmm = None
    def __init__(self, hmm):
        self.hmm = hmm
        self.states = hmm.states
        self.start_p = hmm.start_p
        self.trans_p = hmm.trans_p
        self.emit_p = hmm.emit_p

    def viterbi(self, obs):
        hmm = self.hmm
        states = self.hmm.states
        start_p = self.hmm.start_p
        trans_p = self.hmm.trans_p
        emit_p = self.hmm.emit_p

        V = [{}]
        path = {}
        for (state, i) in states.items():
            V[0][state] = hmm.getStartP(state) + hmm.getEmitP(state, obs[0])
            path[state] = [state]

        for t in range(1, len(obs)):
            V.append({})
            newpath = {}

            for (y, index) in states.items():
                maxList = []
                (prob, state) = max((V[t-1][y0] + hmm.getTransP(y0, y) + hmm.getEmitP(y, obs[t]), y0) for (y0,i) in states.items())
                
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            # Don't need to remember the old paths
            path = newpath
        n = 0           # if only one element is observed max is sought in the initialization values
        if len(obs) != 1:
            n = t
        (prob, state) = max((V[n][y], y) for y,i in states.items())
        return path[state]
