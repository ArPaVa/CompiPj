import sys


class AttributeGrammar:

    def __init__(self, terminals, production_rules, eof_symbol=0):
        self.terminals = terminals
        self.production_rules = production_rules

        non_terminals = [rule[0] for rule in production_rules]
        self.start_symbol = non_terminals[0]
        self.non_terminals = set(non_terminals)

        self.epsilon = sys.intern('<epsilon>')
        self.eof_symbol = eof_symbol

        self.firsts = self.gen_firsts()
        self.follows = self.gen_follows()

    def gen_firsts(self):
        firsts = {}

        change = True
        while change:
            change = False

            for rule in self.production_rules:
                left = rule[0]
                right = rule[1]

                left_first = firsts.setdefault(left, set())
                first_len = len(left_first)

                if not len(right):
                    left_first.add(self.epsilon)
                else:
                    left_first.update(self.first(right, firsts))

                change = change or len(left_first) != first_len

        return firsts

    def gen_follows(self):
        follows = {self.start_symbol: {self.eof_symbol}}

        change = True
        while change:
            change = False

            for rule in self.production_rules:
                change = change or self.update_follows(rule, follows)

        return follows

    def first(self, sentence, firsts=None):
        local = set()

        if not firsts:
            firsts = self.firsts

        for s in sentence:
            s_first = firsts.setdefault(s, {s} if s in self.terminals else set())
            local.update(s_first)

            if self.epsilon not in s_first:
                if self.epsilon in local:
                    local.remove(self.epsilon)
                break

        return local

    def update_follows(self, rule, follows):
        change = False
        left = rule[0]
        right = rule[1]

        for i in range(len(right)):
            if right[i] in self.non_terminals:

                s_follow = follows.setdefault(right[i], set())
                follow_len = len(s_follow)

                tail_first = self.first(right[i + 1:])

                if not len(tail_first) or self.epsilon in tail_first:
                    left_follow = follows.setdefault(left, set())
                    s_follow.update(left_follow)

                s_follow.update(tail_first)

                if self.epsilon in s_follow:
                    s_follow.remove(self.epsilon)

                change = change or len(s_follow) != follow_len

        return change

    def lr0_closure(self, item):
        closure = {item}

        change = True
        while change:

            closure_len = len(closure)
            for rule, dot in closure.copy():
                right = self.production_rules[rule][1]

                if len(right) == dot:
                    continue

                if right[dot] in self.non_terminals:
                    for k in range(len(self.production_rules)):

                        if right[dot] == self.production_rules[k][0]:
                            closure.add((k, 0))

            change = closure_len != len(closure)

        return closure

    def lr0_goto(self, closure, symbol):
        new_closure = set()

        for rule, dot in closure:
            right = self.production_rules[rule][1]

            if len(right) == dot:
                continue

            if right[dot] == symbol:
                new_closure.update(self.lr0_closure((rule, dot + 1)))

        return new_closure

    def build_slr_parsing_table(self):
        canonical = [0, self.lr0_closure((0, 0))]

        action = {}
        goto = {}

        i = 1
        while i < len(canonical):

            for s in self.terminals:
                closure = self.lr0_goto(canonical[i], s)

                if len(closure):
                    try:
                        k = canonical.index(closure)

                    except ValueError:
                        k = len(canonical)
                        canonical.append(closure)

                    action.setdefault(i, {})[s] = k

            for s in self.non_terminals:
                closure = self.lr0_goto(canonical[i], s)

                if len(closure):
                    try:
                        k = canonical.index(closure)

                    except ValueError:
                        k = len(canonical)
                        canonical.append(closure)

                    goto.setdefault(i, {})[s] = k

            for k, dot in canonical[i]:
                rule = self.production_rules[k]

                left = rule[0]
                right = rule[1]

                if len(right) == dot:
                    if not k:
                        action.setdefault(i, {})[self.eof_symbol] = 0
                    else:
                        for s in self.follows[left]:
                            action.setdefault(i, {})[s] = -k

            i += 1

        return action, goto, canonical


# noinspection PyPep8Naming
def build_slr_parser(G):
    action, goto, _ = G.build_slr_parsing_table()

    def parse(buf):
        i = 0
        s = [1]
        r = []

        while True:
            try:
                k = action[s[-1]][buf[i]]

            except KeyError as err:
                correct = list(action[s[-1]].keys())
                raise SyntaxError(f"unexpected token {buf[i]}, expecting {correct}?") from err

            if not k:
                return r[0]

            if k > 0:
                s.append(k)
                r.append(buf[i])
                i += 1

            else:
                left, right, reduce = G.production_rules[-k]

                s_len = len(s) - len(right)
                s[s_len:] = []

                args = r[s_len - 1:]
                r[s_len - 1:] = []

                r.append(reduce(args))
                s.append(goto[s[-1]][left])

    return parse
