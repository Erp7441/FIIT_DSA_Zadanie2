colors = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m"
}

ZERO = colors.get('red') + '0' + "\033[0m"
ONE = colors.get('green') + '1' + "\033[0m"
FALSE = colors.get('red') + "False" + "\033[0m"
TRUE = colors.get('green') + "True" + "\033[0m"
CORRECT = colors.get('green') + "correct" + "\033[0m"
INCORRECT = colors.get('red') + "incorrect" + "\033[0m"


def c(string: str, color: str):

    if color is None or color.lower() not in colors.keys():
        return string

    return colors.get(color.lower()) + string + "\033[0m"


def boolean_values_c(string: list):

    new_string = []
    for letter in string:
        if letter == '0':
            new_string.append(ZERO)
        elif letter == '1':
            new_string.append(ONE)
        else:
            new_string.append(letter)

    return ''.join(new_string)


def boolean_c(boolean_value: bool):
    if boolean_value:
        return TRUE
    else:
        return FALSE
