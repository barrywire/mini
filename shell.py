import mini

while True:
    text = input('Mini > ')
    result, error = mini.run_intermediate_code_generator('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        print(result)
