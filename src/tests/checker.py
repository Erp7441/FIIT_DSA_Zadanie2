# Evaluates given function that had truth values of each letter inserted into it
def evaluate_functions(functions: list):

    # Check if we have a list of functions
    if list is None or len(functions) == 0:
        return False

    # Holds the boolean value we have found
    is_true = True

    # For each function in the list
    for function in functions:
        # For each letter in the function
        for letter in function:
            # If the evaluated letter is '0'
            if letter == '0':
                is_true = False
                # TODO:: shouldn't we break here?

        if is_true:
            # If we have not found any '0' value return True
            return True
        else:
            # Else reset boolean value we have found and continue on the next function in the list
            is_true = True

    # If we haven't found any '1' value's in functions return False
    return False


# Check the expression boolean value according to the combination of '0' and '1'
def check(expression, order, combination):
    functions = []

    # Split the DNF expression into nodes
    nodes = expression.split('+')

    # For each node in the list of nodes
    for node in nodes:

        # Create a list of new nodes
        new_nodes = []

        # For each letter in order
        for index_o, order_enum in enumerate(order):

            # For each character in node
            for index_ch, character in enumerate(node):

                # If the character matches the letter in order
                # TODO:: Change "order[index_o]" to "order[index_o].lower() ?"
                if character.lower() == order[index_o]:

                    # If the character is upper case
                    if character.isupper():
                        # And the combination value is '0'
                        if combination[index_o] == '0':
                            # We append '1' to the new_nodes list
                            new_nodes.append("1")
                        else:
                            # Else we append '0' to the new_nodes list
                            new_nodes.append("0")
                    # Else the character is lowercase
                    # TODO:: Refactor to always just append "combination[index_o] to the new_nodes list
                    else:
                        # If the combination value is '0'
                        if combination[index_o] == '0':
                            # Append '0 to the new_nodes list
                            new_nodes.append("0")
                        else:
                            # Else we append '1' to the new_nodes list
                            new_nodes.append("1")
        # Finally we append the new_nodes list to the list to the list of functions
        functions.append(new_nodes)

    # We evaluate the boolean value of each function in function list
    return evaluate_functions(functions)