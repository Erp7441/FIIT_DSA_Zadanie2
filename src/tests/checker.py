from src.bdd.BDD import BDD
from src.utils.colors import boolean_c, CORRECT
from itertools import product
from time import sleep


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
                break

        if is_true:
            # If we have not found any '0' value return True
            return True
        else:
            # Else reset boolean value we have found and continue on the next function in the list
            is_true = True

    # If we haven't found any '1' value's in functions return False
    return False


# Check the expression boolean value according to the combination of '0' and '1'
def get_letter_value(letter: str, value: str):
    # If the character is upper case
    if letter.isupper():
        # We return the opposite value
        if value == '0':
            return '1'
        else:
            return '0'

    # Else we just return
    return value


# Evaluates total node boolean value
def get_node_value(node: str, combination: str, order: str):

    # For each letter in order
    for order_index, order_letter in enumerate(order):
        # For each letter in node
        for node_letter in node:
            # If the character matches the letter in order
            if node_letter.lower() == order_letter:
                if get_letter_value(node_letter, combination[order_index]) == '0':
                    return False
    return True


def check(expression: str, order: str, combination: str):

    # For each node in the list of nodes
    for node in expression.split('+'):
        if get_node_value(node, combination, order):
            return True

    # We evaluate the boolean value of each function in function list
    return False


def get_diagram_value(bdd, combination):
    last_node_of_combination = bdd.use(combination)

    if last_node_of_combination is None:
        return None

    if last_node_of_combination.value == '1':
        return True
    elif last_node_of_combination.value == '0':
        return False

    return None


def print_combination(combination, expression_value: bool, header_tracker: bool = False, order: str = ""):
    if header_tracker:
        print(order)
        for _ in range(len(order) + 7):
            print('-', end='')
        print('\n', end='')

    print((''.join(combination)) + ": " + boolean_c(expression_value) + " which is " + CORRECT)


def check_bdd_solution(bdd: BDD, expression: str, order: str, verbose_all: bool = False,
                       verbose_bad: bool = True, verbose_good: bool = False, slow_time: float = None):
    # Iter tools product on 01010010101010
    # 1. Generate all possible combinations of 0's and 1's
    # 2. Check the value of "use()" method in BDD
    # 3. Check the value of expression using "check()" function
    # 4. If all possible combinations are equal then we have correct BDD solution

    printed_header = False
    slow = False
    order = order.lower()

    if slow_time is not None:
        slow = True

    for combination in product('01', repeat=len(order)):

        boolean_value = get_diagram_value(bdd, combination)
        expression_value = check(expression, order, combination)

        if boolean_value != expression_value:
            if verbose_all or verbose_bad:
                if slow:
                    sleep(slow_time)
                print("Combination: %s" % ''.join(combination))
                print("Value of BDD: %s" % boolean_value)
                print("Value of expression: %s" % expression_value)

            return boolean_c(False)
        elif verbose_all or verbose_good:
            if slow:
                sleep(slow_time)
            if not printed_header:
                print_combination(combination, boolean_value, printed_header, order)
                printed_header = True
            else:
                print_combination(combination, boolean_value)

    return boolean_c(True)


def test_bdd(expression: str, order: str, verbose_all: bool = False, verbose_bad: bool = True,
             verbose_good: bool = False, slow_time = None):
    bdd = BDD().create(expression, order)
    return check_bdd_solution(bdd, expression, order, verbose_all, verbose_bad, verbose_good, slow_time)
