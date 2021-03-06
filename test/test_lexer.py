from poyais.lexer import lex


def test_empty_exp():
    empty = ""
    assert list(lex(empty)) == []


def test_lambda_exp():
    lambda_exp = "(lambda () nil)"
    assert list(lex(lambda_exp)) == ["(", "lambda", "(", ")", "nil", ")"]


def test_quoted_list():
    quoted_exp = "'()"
    assert list(lex(quoted_exp)) == ["'", "(", ")"]

    quasi_quoted_exp = "`()"
    assert list(lex(quasi_quoted_exp)) == ["`", "(", ")"]


def test_string():
    string_exp = '"Here\'s a semi hairy example"'
    assert list(lex(string_exp)) == [
        string_exp
    ]

    lambda_string_exp = "(lambda () '({}))".format(string_exp)
    assert list(lex(lambda_string_exp)) == [
        "(", "lambda", "(", ")", "'", "(", string_exp, ")", ")"]


def test_single_digits():
    digits_exp = "(define () 5)"
    assert list(lex(digits_exp)) == ["(", "define", "(", ")", "5", ")"]
