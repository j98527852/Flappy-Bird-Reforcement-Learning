import json

class Bot(object):


    def __init__(self):
        self.gameNo = 0
        self.DumpAfter = 25
        self.discount = 1
        self.r = {0: 10, 1: 1, 2: -1000}
        self.lr = 0.7
        self.loadQval()
        self.lastState = "-20_-240_4"
        self.lastAction = 0
        self.moves = []
        self.score = 0

#load privous trained data.
    def loadQval(self):
        self.Qval = {}
        fil = open('Qval.json', 'r')
        self.Qval = json.load(fil)
        fil.close()


#Decide whether to jump or not
    def act(self, difX, difY, vel):
        if difX > 140:
            difX = int(difX) - (int(difX) % 70)
        state = str(int(difX) - int(difX)%10) + '_' + str(int(difY) - int(difY)%10) + '_' + str(vel)  #%10 to reduce complexicity
        self.moves.append([self.lastState,self.lastAction,state])
        self.lastState = state


        try:
            ifDontFlap = self.Qval[state][0]
            ifFlaped = self.Qval[state][1]
        except :
            self.Qval.update({state : [0,0]})

        # if privous reward for "DoNotFlap" is higher than "Flap" then "DoNotFlap" in given state
        if self.Qval[state][0] >= self.Qval[state][1]:
            self.lastAction = 0
            return 0
        else:
            self.lastAction = 1
            return 1


#main function where q values are updated
    def update_scores(self):
        revMoves = list(reversed(self.moves))
        if int(revMoves[0][2].split('_')[1]) > 100:
            upperPipeCol = True
        else:
            upperPipeCol = False
        t=1
        for m in revMoves:
            state = m[0]
            act = m[1]
            res = m[2]
            if (state.split("_")[1]<120):
                self.Qval[state][act] = (1- self.lr) * (self.Qval[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.Qval[res]) )
            if t == 1 or t==2:
                self.Qval[state][act] = (1- self.lr) * (self.Qval[state][act]) + (self.lr) * ( self.r[2] + (self.discount)*max(self.Qval[res]) )
            elif upperPipeCol and act :
                self.Qval[state][act] = (1- self.lr) * (self.Qval[state][act]) + (self.lr) * ( self.r[2] + (self.discount)*max(self.Qval[res]) )
                upperPipeCol = False
            else:
                self.Qval[state][act] = (1- self.lr) * (self.Qval[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*max(self.Qval[res]) )
            t += 1
        self.gameNo += 1 #increase game count
        self.dump_Qval() # Dump q values (if game count % DumpAfter == 0)
        self.moves = []

    def dump_Qval(self):

        if self.gameNo % self.DumpAfter == 0:
            fil = open('Qval.json', 'w')
            json.dump(self.Qval, fil)
            fil.close()
            print('Q-values updated on local file.')

    def highScores(self,score):
        if self.score < score:
            self.score = score
        print(self.score)   #to check progress of learened game
        print(self.gameNo)
