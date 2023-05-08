import mini
import time

file_name = 'ex.mini'


def run_lexer():
    text = ""
    with open(file_name, 'r') as file:
        text = file.read()

    if text.strip() == "":
        return
    result, error = mini.run_lexer(file_name, text)

    if error:
        print(error.as_string())
    else:
        print(result)


def run_parser():
    text = ""
    with open(file_name, 'r') as file:
        text = file.read()

    if text.strip() == "":
        return
    result, error = mini.run_parser(file_name, text)

    if error:
        print(error.as_string())
    else:
        print(result)


# def run_interpreter():
#     text = ""
#     with open(file_name, 'r') as file:
#         text = file.read()

#     if text.strip() == "":
#         return
#     result, error = mini.run(file_name, text)

#     if error:
#         print(error.as_string())
#     else:
#         print(result)


# Calculate Run Time
lexer_start_time = time.time()

run_lexer()

lexer_finish_time = time.time()

lexer_total_run_time = lexer_finish_time - lexer_start_time
print("=====================================================================")
print("\n", file_name, "Mini Lexer runs in:",
      lexer_total_run_time, "seconds\n\n")

parser_start_time = time.time()

run_parser()

parser_finish_time = time.time()

parser_total_run_time = parser_finish_time - parser_start_time
print("=====================================================================")
print("\n", file_name, "Mini Parser runs in:",
      parser_total_run_time, "seconds\n\n")

# interpreter_start_time = time.time()

# run_interpreter()

# interpreter_finish_time = time.time()
# interpreter_total_run_time = interpreter_finish_time - interpreter_start_time
# print("=====================================================================")
# print("\n", file_name, "Interpreter runs in:", interpreter_total_run_time, "seconds")
