import mini

while True:
    text = input('Mini > ')
    result, error = mini.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        print(result)
