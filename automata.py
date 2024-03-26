import copy


class NFA:
    def __init__(self, initial=0, final=1, states=2, transitions=None):
        # PyCharm did this
        if transitions is None:
            transitions = {}

        self.initial = initial
        self.final = final
        self.states = states
        self.transitions = transitions

    def __add__(self, other):
        new = self.copy()

        new.final = self.states + other.final
        new.states += other.states

        new.transitions.setdefault(self.final, {}).setdefault(0, []).append(self.states)

        for k1 in other.transitions.keys():
            for k2 in other.transitions[k1].keys():
                new.transitions.setdefault(k1 + self.states, {}).setdefault(k2, []).extend(
                    [v + self.states for v in other.transitions[k1][k2]])

        return new

    def __or__(self, other):
        new = self.copy()

        new.final = self.states + other.final
        new.states += other.states

        new.transitions.setdefault(self.initial, {}).setdefault(0, []).append(self.states)
        new.transitions.setdefault(self.final, {}).setdefault(0, []).append(new.final)

        for k1 in other.transitions.keys():
            for k2 in other.transitions[k1].keys():
                new.transitions.setdefault(k1 + self.states, {}).setdefault(k2, []).extend(
                    [v + self.states for v in other.transitions[k1][k2]])

        return new

    # def __invert__(self):
    #     new = self.copy()
    #     new.final = new.states
    #     new.states += 1
    #     for i in range(self.final):
    #         new.transitions.setdefault(i, {}).setdefault(0, []).append(new.final)
    #     return new

    def opt(self):
        new = self.copy()
        new.transitions.setdefault(new.initial, {}).setdefault(0, []).append(new.final)
        return new

    def star(self):
        new = self.opt()
        new.transitions.setdefault(new.final, {}).setdefault(0, []).append(new.initial)
        return new

    def copy(self):
        return copy.deepcopy(self)

    def e_closure(self, *states):
        closure = list(states)

        for state in closure:
            for k in self.transitions.setdefault(state, {}).keys():

                if not k:
                    for v in self.transitions[state][k]:

                        if v not in closure:
                            closure.append(v)

        return frozenset(closure)

    def powerset_construction(self):
        states = [self.e_closure(self.initial)]

        move = {}
        finals = set()

        i = 0
        while i < len(states):
            edges = {}

            for s in states[i]:
                for a in self.transitions[s].keys():

                    if a:  # skip epsilon transitions, e_closure will handle them
                        edges.setdefault(a, set()).update(self.transitions[s][a])

            for a in edges.keys():
                closure = self.e_closure(*edges[a])

                try:
                    k = states.index(closure)

                except ValueError:
                    k = len(states)
                    states.append(closure)

                move.setdefault(i, {})[a] = k

            if self.final in states[i]:
                finals.add(i)

            i += 1

        return move, finals, states


def char(code):
    new = NFA()
    new.transitions.setdefault(new.initial, {})[code] = [new.final]
    return new


def char_range(nfa_start, nfa_end):
    new = NFA()
    start = list(nfa_start.transitions[nfa_start.initial].keys())[0]
    end = list(nfa_end.transitions[nfa_end.initial].keys())[0]

    for code in range(ord(start), ord(end) + 1):
        new.transitions.setdefault(new.initial, {})[chr(code)] = [new.final]
    return new


def build_recognizer(nfa):
    move, finals, _ = nfa.powerset_construction()

    def match(string):
        state = 0
        index = 0

        while index < len(string):
            try:
                state = move[state][string[index]]
                index += 1
            except KeyError:
                break

        return state in finals, index

    return match
