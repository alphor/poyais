from collections import namedtuple
import re


# the fundamental parser unit is constructed from a tag
# and a regex identifying the tag.

# it is just a function that takes a string and returns
# a generator that yields a number of tagged matches:

Tagged_Match = namedtuple('Tagged_Match', ('tag', 'match'))


# to solve grouping, perhaps anonymous rules associated with a group
# built right before parser build time.

# to solve an optional, a parser can be or'd with the empty parser
# ie something that always returns the empty string:
#    this idea I like less, but it certainly is simple, because if the
#    optional fails then the syntax is satisfied but doesn't actually
#    move through the token stream

# what about repeats?
# one idea is to take a list of parsers, and them, and continually
# apply the parser until there is no more output. One of the issues is
# nonzero repetition. How does EBNF handle a fixed number of rhs
# elements? I guess that's just a bunch of ands.

# I think the trick behind MetaII is just reification of the parser
# into source code.  If this could be done then this'd be a way to
# generate compiler front ends, for any target language, provided it
# can be expressed in EBNF.




def make_tagged_matcher(tag, regex_string):
    # build the regex, then return a function that takes a string,
    # applies the reg to the string, if it succeeds
    # return a tagged match with the tag and the string that matched.
    reg = re.compile(regex_string)

    def parser(string):
        match = reg.match(string)
        if match:
            return (Tagged_Match(tag, match.group()),)
    return parser


def and_parsers(*parsers):
    def parser(string):
        out = []
        idx = 0
        for p in parsers:
            maybe = p(string[idx:])
            if maybe:
                for tagged_match in maybe:
                    out.append(tagged_match)
                    idx += len(tagged_match.match)
            else:
                # one of the parsers failed. Stop parsing,
                # fail the whole parser.
                return ()
        return tuple(out)
    return parser


def or_parsers(*parsers):
    def parser(string):
        for p in parsers:
            maybe = p(string)
            if maybe:
                return maybe
        else:
            return ()
    return parser
