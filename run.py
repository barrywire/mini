import mini
import time

file_name = 'ex.mini'

def runParser():
    text = ""
    with open(file_name, 'r') as file:
        text = file.read()

    if text.strip() == "":
        return
    result, error = mini.run(file_name, text)

    if error:
        print(error.as_string())
    else:
        print(result)


start_time = time.time()
runParser()

# Calculate Run Time
finish_time = time.time()
total_run_time = finish_time - start_time
print("\n", file_name, "runs in:", total_run_time, "seconds")
