import cPickle as pickle
from sets import Set
import time
import random
from operator import itemgetter
from pprint import pprint

MAX_VAL=2
MIN_VAL=0
PERFORMING=False

'''
Prior Audience Sample, to compare levels
0 = Weak
1 = Medium
2 = Strongest
'''
def _getSample():
    return random.randrange(MIN_VAL,MAX_VAL + 1)


prior = 1 #initiliaze the richard 
jokesAndResponses = {} #set of told jokes, and their response
jokesTold = 0
heuristics = Set()
'''
Main Function Here
'''

class heuristic(object):
    def __init__(self,t):
	self.type = t
	self.fails = 0 
	self.prob = 99 #out of a hundred percent
    def getInfo(self):
	    return [self.type,self.fails,self.prob]

    def getType(self):
	    return self.type

    def failSelf(self):
	    self.fails = self.fails + 1
	    self.prob = self.prob/ (2**self.fails)

 

class performance(object):
    def __init__(self,h):
        self.allH = Set()
        for elm in h:
            self.allH.add(heuristic(elm))

    def getInfo(self):
        print "Printing the set of heuristics:\n"

	tempList=[]
        for elm in self.allH:
            tempList.append(elm.getInfo())

	tempList=list(sorted(tempList,key=itemgetter(2)))
	pprint(tempList)


    def reportFailure(self,tempH):
        for h in self.allH:
            if h.getType() in tempH:
                print "HERE IS A FAILING HEURISTIC: ", h.getType()
                h.failSelf()

    def getSuccessProb(self,tempH):
        for h in self.allH:
            if h.getType() in tempH:
                print "Here, collect and average the probabilities for the heuristics in tempH"
	

if __name__=="__main__":
    random.seed()

    #this is the sim for getting audience input for jokes
    allJokes = pickle.load(open("smallerObjects.p","rb"))

    print "This is all of our jokes:"
    #create set for heuristics
    for joke in allJokes:
	    print joke
	    heuristics.add(joke[1])
	    heuristics.add(joke[2])
	    heuristics.add(joke[3])

       
    p = performance(heuristics)
    p.getInfo() 
    for joke in allJokes:
        #Current Joke Heuristics
        tempH = []
        tempH.append(joke[1])
        tempH.append(joke[2])
        tempH.append(joke[3])
  
        #joke = [ Name,	Category, Version,  Length ]
        print "*"*20
        print "\n\nTELLING THIS JOKE: ",joke[0] 

        #Gets Reponse after telling a joke
        jokeResp = _getSample()
        jokesTold = jokesTold + 1

        print "PRIOR (PRYOR): ", prior
        print "SIMULATED RESPONSE VAL: ", jokeResp       
        
        print "ROBOT RESPONSE:"
        if jokeResp < prior:
            print "Whoops!"
            binaryResponse = "BAD"
            p.reportFailure(tempH)
        else:
	    print "Good!"
            binaryResponse = "GOOD"

        jokesAndResponses.update({joke[0]:binaryResponse})
        p.getInfo()

print "DONE WITH PERFORMANCE"
    
