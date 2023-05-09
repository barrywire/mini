# MINI Language Compiler

Mini is a simple language extracted from the BASIC language developed in the 1960s by John George Kemeny and Thomas Eugene Kurtz at Dartmouth College.

## Mini Language - Grammar

The grammar of the Mini language is defined in the grammar.txt file. It is under continuous development.

## Mini Language - Lexer

Developed by [Barnabas Wire](https://github.com/barrywire)
The code for the lexer is found in its entirety in the basic.py file, specifically in the Lexer class. Errors are handled by the Error class in collaboration with the IllegalCharError and ExpectedCharError classes.

## Mini Language - Parser

Developed by [David Kilolo](https://github.com/dgkilolo), [Laurent Namasaka](https://github.com/laurentnamasaka), [Samson Rasugu](https://github.com/samrasugu) and [Barnabas Wire](https://github.com/barrywire).

## Mini Language - Intermediate Code Generator

Developed by [David Kilolo](https://github.com/dgkilolo), [Laurent Namasaka](https://github.com/laurentnamasaka), [Samson Rasugu](https://github.com/samrasugu) and [Barnabas Wire](https://github.com/barrywire).


## Running the code

1. Clone the repository
2. Run the shell.py file. It is the entry point of the compiler.

```bash
python3 run.py
```

3. Enter the code to be interpreted in the terminal
