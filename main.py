import sys
from functools import reduce
from typing import List, Tuple, Set, Dict
from queue import Queue 

State = int
Word = str
Configuration = Tuple[State, Word]
Transition = Tuple[State, Word, List[State]]
EPSILON = ""

class NFA: #nfa-l
    def __init__(self, numberOfStates: int, alphabet: Set[chr], finalStates: Set[State],
                 delta: Dict[Tuple[State, chr], Set[State]]):
        self.numberOfStates = numberOfStates
        self.states = set(range(self.numberOfStates))
        self.alphabet = alphabet
        self.initialState = 0
        self.finalStates = finalStates
        self.delta = delta

class DFA: #dfa-l
    def __init__(self, numberOfStates: int, alphabet: Set[chr], finalStates: Set[State],
                 delta: Dict[Tuple[State, chr], State]):
        self.numberOfStates = numberOfStates
        self.states = set(range(self.numberOfStates))
        self.alphabet = alphabet
        self.initialState = 0
        self.finalStates = finalStates
        self.delta = delta

def epsilon(states, numberOfStates, delta):
    res = set(states) #rezultatul
    eps = Queue()
    visited = [0] * numberOfStates #stare vizitata sau nu
    eps.put(states)
    while (not eps.empty()):    
        for state in eps.get(): #fiecare stare
            visited[state] = 1 #devine vizitata
            try: #daca exista tranzitii pe epsilon
                ekey = delta[state, EPSILON]
            except KeyError:
                continue
            res.update(ekey) #adaug la rezultat
            for k in ekey:
                if (visited[k] == 0):
                    eps.put({k}) #pun in coada noile elemente
    
    return res

def searchState(numberOfStates, mapStates, state):
    for k in range(0, numberOfStates):
        r = mapStates[k]
        if (r == state):
            return k
    return -1

def setfinalStates(numberOfStates, mapStates, nfaFinalStates):
    finalStates = set()
    for i in range(0, numberOfStates):
        for k in mapStates[i]:
            if (k in nfaFinalStates):
                finalStates.add(i)
    return finalStates

def NFA_to_DFA(nfa):
    
    q = Queue() #coada de parcurgere a starilor
    mapStates = dict() #starile automatului
    numberOfStates = 1
    delta = dict()
    #calculez starea initiala cu inchiderea epsilon
    q0 = epsilon({0}, nfa.numberOfStates, nfa.delta)
    q.put([q0, 0])
    mapStates[0] = q0
    #print(nfa.alphabet)
    while (not q.empty()): #cat mai am stari
        [states, newstate] = q.get() #extrag starea
        for ch in nfa.alphabet: #pentru fiecare caracter din alfabet
            temp = set()
            for s in states: #fiecare stare din set
                try:
                    temp.update(nfa.delta[s, ch]) #stare pentru tranzitia pe ch
                except KeyError:
                    continue
            #adaug starile + incluziunile pe epsilon      
            temp.update(epsilon(temp, nfa.numberOfStates, nfa.delta)) 
            #adaug tranzitia pe o stare existenta sau noua
            ifState = searchState(numberOfStates, mapStates, temp)
            if (ifState == -1): #daca nu exista creez o noua stare
                mapStates[numberOfStates] = temp
                delta[newstate, ch] = numberOfStates
                q.put([temp, numberOfStates])
                numberOfStates = numberOfStates + 1
            else: delta[newstate, ch] = ifState #asignez tranzitia    
    #creez starile finale
    finalStates = setfinalStates(numberOfStates, mapStates, nfa.finalStates)
    #creez dfa-l dupa modificarea starilor si deltei
    dfa = DFA(numberOfStates = numberOfStates, alphabet = nfa.alphabet,
                    finalStates = finalStates, delta = delta)
    
    return dfa


def read(inFile):
    with open(inFile) as file:
        numberOfStates = int(file.readline().rstrip()) #nr de stari
        finalStates = set(map(int, file.readline().rstrip().split(" "))) 
        delta = dict()
        alphabet = set()
        while True: #construiesc delta si alfabetul citind din fisier
            transition = file.readline().rstrip().split(" ")
            if transition == ['']:
                break
            if transition[1] == "eps":
                transition[1] = EPSILON
            else :
                alphabet.add(transition[1])
            delta[(int(transition[0]), transition[1])] = set(map(int, transition[2:]))
    
    return [numberOfStates, finalStates, delta, alphabet]


def write(outFile, dfa):
    file = open(outFile, "w")
    file.write(str(dfa.numberOfStates) + "\n") #nr-l de stari

    q = set(dfa.finalStates)
    while (len(q)): #starile finale
        file.write(str(q.pop()))
        if (len(q)):
            file.write(" ")
    
    file.write("\n")
    for i in range(0, dfa.numberOfStates): #penrtu fiecare stare
        for j in  dfa.alphabet: #trazitia pe caracterele din aflabet
            file.write(str(i) + " " + j + " " + str(dfa.delta[i, j]) + "\n")


def main(inFile, outFile):

    [numberOfStates, finalStates, delta, alphabet] = read(inFile) #citesc 
    nfa = NFA(numberOfStates = numberOfStates, alphabet = alphabet, #creez nfa
                    finalStates = finalStates, delta = delta)
    dfa = NFA_to_DFA(nfa) #creez dfa
    write(outFile, dfa) #scriu dfa-l


if (len(sys.argv) < 3): #daca nu exista argumentele
    print("Use python3 main.py inputFile outputFile")
else: main(sys.argv[1], sys.argv[2]) #apelez main
