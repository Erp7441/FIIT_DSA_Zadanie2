def check(expression, order, combination):
    functions = []
    splits = expression.split('+')

    for split in splits:
        new_splits = []
        for index_o, order_enum in enumerate(order):
            for index_ch, character in enumerate(split):
                if character.lower() == order[index_o]:
                    if character.isupper():
                        if combination[index_o] == '0':
                            new_splits.append("1")
                        else:
                            new_splits.append("0")
                    else:
                        if combination[index_o] == '0':
                            new_splits.append("0")
                        else:
                            new_splits.append("1")
        functions.append(new_splits)


    # Comment this nigger
    is_true = True
    for function in functions:
        for letter in function:
            if letter == '0':
                is_true = False
        if is_true:
            return True
        else:
            is_true = True

    return False