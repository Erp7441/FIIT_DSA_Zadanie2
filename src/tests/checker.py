from src.bdd.BDD import BDD


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


def get_combinations(characters: str, amount: int):
    from itertools import product
    from src.utils.converter import tuple_to_string
    combinations = []
    for combination in list(product(characters, repeat=amount)):
        combinations.append(tuple_to_string(combination))
    return combinations


def check_bdd_solution(bdd: BDD, expression: str, order: str, verbose: bool = True):
    from src.utils.colors import boolean_c

    # Iter tools product on 01010010101010
    # 1. Generate all possible combinations of 0's and 1's
    # 2. Check the value of "use()" method in BDD
    # 3. Check the value of expression using "check()" function
    # 4. If all possible combinations are equal then we have correct BDD solution

    combinations = get_combinations('01', len(order))
    printed_header = False

    for combination in combinations:

        last_node_of_combination = bdd.use(combination)
        boolean_value = None

        if last_node_of_combination is None:
            continue

        if last_node_of_combination.value == '1':
            boolean_value = True
        elif last_node_of_combination.value == '0':
            boolean_value = False
        else:
            return None

        if boolean_value != check(expression, order, combination):
            # TODO:: Remove
            print("Expression: %s" % expression)
            print("Order: %s" % order)
            print("Combination: %s" % combination)
            print("Last Expression: %s" % last_node_of_combination.expression)
            print("Last Order: %s" % last_node_of_combination.order)
            print("Boolean value of last node: %s" % boolean_value)
            return boolean_c(False)
        else:
            from src.utils.colors import boolean_values_c, c

            if not printed_header and verbose:
                print(order)
                for _ in range(len(order) + 7):
                    print('-', end='')
                print('\n', end='')
                printed_header = True

            if verbose:
                print(boolean_values_c(combination) + ": " + boolean_c(boolean_value) + " which is " + c("correct", "green"))

    return boolean_c(True)


def test_bdd(expression: str, order: str, verbose: bool = True):
    bdd = BDD().create(expression, order)
    return check_bdd_solution(bdd, expression, order, verbose)
