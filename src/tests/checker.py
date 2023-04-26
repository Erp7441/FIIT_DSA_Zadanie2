from src.bdd.BDD import BDD
from src.utils.colors import boolean_c, CORRECT
from itertools import product
from time import sleep


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
        # If the node value is True then return True
        if get_node_value(node, combination, order):
            return True

    # All nodes are False. Return False.
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


def print_combination(combination, expression_value: bool, header_tracker: bool = False, order: str = "", slow_output: bool = False, slow_time: float = 0.0):
    if slow_output:
        sleep(slow_time)
    if header_tracker:
        print(order)
        for _ in range(len(order) + 7):
            print('-', end='')
        print('\n', end='')

    print((''.join(combination)) + ": " + boolean_c(expression_value) + " which is " + CORRECT)


def print_bad_combination(combination: str, bdd_value: bool, expression_value: bool, slow_output: bool = False, slow_time: float = 0.0):
        if slow_output:
            sleep(slow_time)
        print("Combination: %s" % ''.join(combination))
        print("Value of BDD: %s" % bdd_value)
        print("Value of expression: %s" % expression_value)


def check_bdd_solution(bdd: BDD, expression: str, order: str, verbose_all: bool = False,
                       verbose_bad: bool = True, verbose_good: bool = False, slow_time: float = None):
    # Iter tools product on 01010010101010
    # 1. Generate all possible combinations of 0's and 1's
    # 2. Check the value of "use()" method in BDD
    # 3. Check the value of expression using "check()" function
    # 4. If all possible combinations are equal then we have correct BDD solution

    printed_header = False
    slow_output = False
    order = order.lower()

    if slow_time is not None:
        slow_output = True

    for combination in product('01', repeat=len(order)):

        expression_value = check(expression, order, combination)
        bdd_value = get_diagram_value(bdd, combination)

        if bdd_value != expression_value:
            print_bad_combination(combination, bdd_value, expression_value, slow_output, slow_time)
            return boolean_c(False)
        elif verbose_all or verbose_good:
            if not printed_header:
                print_combination(combination, bdd_value, printed_header, order, slow_output, slow_time)
                printed_header = True
            else:
                print_combination(combination, bdd_value, slow_output=slow_output, slow_time=slow_time)

    return boolean_c(True)


def test_bdd(expression: str, order: str, verbose_all: bool = False, verbose_bad: bool = True,
             verbose_good: bool = False, slow_time = None):
    bdd = BDD().create(expression, order)
    return check_bdd_solution(bdd, expression, order, verbose_all, verbose_bad, verbose_good, slow_time)
