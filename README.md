# About

Poyais is the beginnings of a Scheme implementing [r7rs](r7rs.com) targeting the JVM written in Python.

# Why?

Why not?

# How?
Aim is to take an EBNF specification to a compiler. What is currently included is a relatively clean EBNF tokenizer and primitives to combine parsers.

What remains to be written is:
 - A routine to transform a set of tokenized rules derived from EBNF into a parser
 - A routine that transforms the output of a parser into an AST
 - A routine that transforms an AST into JVM bytecode
 
Here's an incomplete EBNF spec for scheme following ISO/EIC 14977
``` ebnf
letter = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" 
       | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v"
       | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R"
       | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
math symbol = "+" | "-" | "/" | "*" ;
whitespace = " " | "\t" | "\n" ;

character = letter | digit ;
symbol = ( letter | math symbol ) , { character } ;
sexp = "(" , [ whitespace ] , symbol , { whitespace , symbol }, [ whitespace ], ")" ;
quote = "'" ;
backquote = "`" ;
quoted_list = ( quote , "(" , ")" ) | ( quote, sexp ) ;
backquoted_list = ( backquote , "(" , ")" ) | ( backquote, sexp ) ;
```

Later on it might be necessary to define 'define' and 'syntax-rule' which would only require editing this spec. A scheme level reader macro seems unlikely, but it's definitely possible to extend syntax here as a substitute, provided the new definitions are handled in the AST generation code.

There is a choice to be made here of returning a flat stream of parsed symbols and mapping it an AST or outputting an AST defined by this recursive descent.

I think a flat stream is cleaner, but I'm not sure.

# A couple notes for future me

It's a little strange to see r7rs mention scheme as never destroying lisp objects but having mutation in the language. What does destroy really mean here?

