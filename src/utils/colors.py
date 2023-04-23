def c(string: str, color: str):

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

    if color is None or color.lower() not in colors.keys():
        return string

    return colors.get(color.lower()) + string + "\033[0m"


def boolean_values_c(string: str):

    new_string = []
    for letter in string:
        if letter == '0':
            new_string.append(c(letter, "Red"))
        elif letter == '1':
            new_string.append(c(letter, "Green"))
        else:
            new_string.append(letter)
    return ''.join(new_string)


def boolean_c(boolean_value: bool):
    if boolean_value:
        return c(str(boolean_value), "Green")
    else:
        return c(str(boolean_value), "Red")
