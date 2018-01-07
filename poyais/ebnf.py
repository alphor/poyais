from collections import namedtuple

# LETTER = re.compile("[a-zA-Z]")
# DIGIT = re.compile("[0-9]")

Rule = namedtuple('Rule', ('lhs', 'rhs'))


def split_into_rules(ebnf_string):
    return dispatch_charwise(_split_assignments, ebnf_string)


def dispatch_charwise(dispatch, ebnf_string):
    # assigned is set when we've encountered an equal sign, but not a
    # terminator (semicolon). this lets us keep track of which side to
    # send characters to, and to expect an unquoted semicolon or an
    # unquoted equals
    state = {
        'assigned': False,
        'quoted': False,
        'lhs': [],
        'rhs': [],
    }
    linum, idx = 0, 0
    for line in ebnf_string.split("\n"):
        # we increment before so that we correctly handle end of file easily
        while idx < len(line):
            maybe_result = dispatch(line, linum, idx, state)
            if maybe_result:
                yield maybe_result
            idx += 1
        idx = 0
        linum += 1
    # problem here is that we silently ignore half written correct
    # rules at the end like:
    #   foo = 'a'
    # (missing semicolon)


# it's a little strange to mutate our inputs and also output rules.
# well... a lot of this is strange.
def _split_assignments(line, linum, idx, state):
    deref = line[idx]
    if state['quoted']:
        assert state['assigned'], errmsg('lhs_quote', linum, idx)

        state['rhs'].append(deref)

        if deref == state['quoted']:
            state['quoted'] = False
    elif state['assigned']:  # we're on rhs
        assert deref != "=", errmsg('rhs_unquoted_equals', linum, idx)

        if deref == ";":
            # completed rule
            lhs, rhs = (''.join(state['lhs']).strip(),
                        ''.join(state['rhs']).strip())
            state['lhs'], state['rhs'] = [], []
            state['assigned'] = False
            return Rule(lhs, rhs)
        state['rhs'].append(deref)
    elif deref == '=':
        state['assigned'] = True
    else:
        assert deref != ";", errmsg('lhs_semicolon', linum, idx)
        state['lhs'].append(deref)


def errmsg(why, linum, idx):
    return {
        'lhs_quote':           "Quote character on left hand side at",
        'lhs_semicolon':       "Semicolon on left hand side at",
        'rhs_unquoted_equals': "Unquoted '=' on right hand side at",
        'unmatched_text':      "Unmatched text beyond"
    }[why] + " {}: {}".format(linum, idx)