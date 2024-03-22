import pydot
from utils import ContainerSet

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        temp = self.transitions[self.running]
        return temp[symbol][0]
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self.running = self.start
        for item in range(len(string)):
            self.running = self._move(string[item])
        print(self.running)
        print(self.finals)
        print(self.running in self.finals)
        
        return self.running in self.finals
    
def move(automaton, states, symbol):
    moves = set()
    for state in states:
        temp = automaton.transitions.get(state,-1)
        if temp != -1:
            if temp.get(symbol,-1) != -1:
                for element in temp[symbol]:    
                    moves.add(element)
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    while pending:
        state = pending.pop()
        closure.add(state)
        if automaton.transitions.get(state,-1) != -1:
            temp = automaton.transitions.get(state,-1)
            if temp.get("",-1) != -1:
                to_add= temp[""]
                for item in to_add:
                    if item not in pending and item not in closure:
                        pending.append(item)

                
    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]
    pending = [ start ]
    id = 1
    while pending:
        state = pending.pop()
        for symbol in automaton.vocabulary:
            temp = move(automaton,state,symbol)
            if len(temp)==0:
                continue
            temp = epsilon_closure(automaton,temp)
            exists = False
            for s in states:
                if temp.set == s.set:
                    transitions[state.id, symbol] = s.id
                    exists = True
            if exists: continue
                
            temp.id = id
            temp.is_final = any(s in automaton.finals for s in temp)
            id +=1
            states.append(temp)
            pending.append(temp)
            
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = temp.id
                pass
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[origin+d1,symbol]= [dest+d1 for dest in destinations] 
        
    for (origin, symbol), destinations in a2.map.items():
        transitions[origin+d2,symbol]= [dest+d2 for dest in destinations] 

    transitions[0,""]= [d1]
    transitions[0,""]= [d2]
    
    for st in a1.finals:
        transitions[st+d1,""]=[final]
    for st in a2.finals:
        transitions[st+d2,""]=[final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[origin+d1,symbol]= [dest+d1 for dest in destinations] 
        
    for (origin, symbol), destinations in a2.map.items():
        transitions[origin+d2,symbol]= [dest+d2 for dest in destinations] 

    
    for st in a1.finals:
        transitions[st+d1,""]=[d2]
        
    for st in a2.finals:
        transitions[st+d2,""]=[final]
            
    states = a1.states + a2.states + 1
    finals = { final }
    print(states,finals,transitions,start)
    return NFA(states, finals, transitions, start)
#el closure no me queda claro q este bien
def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[origin+d1,symbol]= [dest+d1 for dest in destinations] 
    
    transitions[0,""]= [d1]
    transitions[0,""]= [final]
    
    for st in a1.finals:
        transitions[st+d1,""]=[0]
        transitions[st+d1,""]=[final]
            
    states = a1.states +  2
    finals = { final }
    print(states,finals,transitions,start)
    return NFA(states, finals, transitions, start)