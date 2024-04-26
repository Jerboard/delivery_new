

# обрабатывает строку с числом, возвращает число, если строка содержит число, иначе возвращает 0
def hand_digit(values: str) -> int:
    if not values == '' or values == ' ':
        digit = 0
    else:
        chars = [' ', '\xa0']
        values = values.translate(str.maketrans('', '', ''.join(chars)))
        digit = int(values) if str(values).isdigit() else 0

    return digit
