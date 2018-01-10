from poyais.combinator import make_tagged_matcher, and_parsers, or_parsers
from poyais.combinator import Node
from hypothesis.strategies import text
from hypothesis import given
import string


@given(text(alphabet=string.ascii_letters))
def test_make_parser_returns_fun(literal_reg):
    func = make_tagged_matcher('foo', literal_reg)

    tm = func(literal_reg)
    assert len(tm) == 1
    assert tm[0].match == literal_reg


@given(text(alphabet=string.ascii_letters),
       text(alphabet=string.ascii_letters))
def test_and_parsers_joins_parsers(reg1, reg2):
    p1 = make_tagged_matcher('foo', reg1)
    p2 = make_tagged_matcher('bar', reg2)

    func = and_parsers(p1, p2)
    tms = func(reg1 + reg2)
    assert tms[0].match == reg1
    assert tms[1].match == reg2


@given(text(alphabet=string.ascii_letters),
       text(alphabet=string.ascii_letters))
def test_or_parsers_acts_as_either(reg1, reg2):
    p1 = make_tagged_matcher('foo', reg1)
    p2 = make_tagged_matcher('bar', reg2)

    func = or_parsers(p1, p2)
    tm1 = func(reg1)
    assert len(tm1) == 1
    assert reg1.startswith(tm1[0].match)

    tm2 = func(reg2)
    assert len(tm2) == 1
    assert reg2.startswith(tm2[0].match)


def test_or_and_and_comb():
    # at this point I'm thinking it's probably a good idea
    # to write an anonymous parser. that'll make testing these
    # slightly less frictionless but more importantly
    # I could see their use in compound statements with arbitrary
    # syntax that we don't care about at the AST level
    p1 = make_tagged_matcher('flavor1', 'honey')
    p2 = make_tagged_matcher('flavor2', 'apple')
    p3 = make_tagged_matcher('end',     'pie')

    honeypie = and_parsers(p1, p3)
    applepie = and_parsers(p2, p3)
    anypie = or_parsers(honeypie, applepie)

    assert concat_tm_matches(honeypie('honeypie')) == 'honeypie'
    assert concat_tm_matches(applepie('applepie')) == 'applepie'

    assert concat_tm_matches(anypie('honeypie')) == 'honeypie'
    assert concat_tm_matches(anypie('applepie')) == 'applepie'


def test_and_or_or_comb():
    p1 = make_tagged_matcher('base', 'peach')
    p2 = make_tagged_matcher('avant_garde', 'broccoli')
    p3 = make_tagged_matcher('dessert', 'cobbler')
    p4 = make_tagged_matcher('plural', 'es')

    peach_or_broc = or_parsers(p1, p2)
    dessert_or_plural = or_parsers(p3, p4)

    yums = and_parsers(peach_or_broc, dessert_or_plural)

    for yummy in ('peachcobbler', 'broccolicobbler',
                  'peaches', 'broccolies'):
        assert concat_tm_matches(yums(yummy)) == yummy


def test_node_deep_iter():
    b = Node(3, Node(4, Node(5, Node(
            Node(1, Node(2, Node(3))), Node(10, Node(3))))))
    assert b.deep_iter() == (3, 4, 5, (1, 2, 3), 10, 3)


def concat_tm_matches(tms):
    return ''.join(x.match for x in tms)

