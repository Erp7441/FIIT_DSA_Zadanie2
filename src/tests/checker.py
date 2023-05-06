from src.bdd.BDD import BDD
from src.utils.colors import boolean_c, CORRECT
from itertools import product
from time import sleep
from timeit import default_timer


def time_ms():
    return default_timer() * 1000


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


def print_combination(
        combination,
        expression_value: bool,
        header_tracker: bool = False,
        order: str = "",
        slow_output: bool = False,
        slow_time: float = 0.0
):
    if slow_output:
        sleep(slow_time)
    if header_tracker:
        print(order)
        for _ in range(len(order) + 7):
            print('-', end='')
        print('\n', end='')

    print((''.join(combination)) + ": " + boolean_c(expression_value) + " which is " + CORRECT)


def print_bad_combination(
        combination: str,
        bdd_value: bool,
        expression_value: bool,
        slow_output: bool = False,
        slow_time: float = 0.0
):
    if slow_output:
        sleep(slow_time)
    print("Combination: %s" % ''.join(combination))
    print("Value of BDD: %s" % bdd_value)
    print("Value of expression: %s" % expression_value)


def check_bdd_solution(
        bdd: BDD,
        expression: str,
        order: str,
        verbose_all: bool = False,
        verbose_bad: bool = True,
        verbose_good: bool = False,
        slow_time: float = None
):
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

    # Case if the expression has been completely reduced to single True or False
    if len(expression) == 1:
        if expression == "1":
            return boolean_c(True)
        return boolean_c(False)

    for combination in product('01', repeat=len(order)):

        expression_value = check(expression, order, combination)
        bdd_value = get_diagram_value(bdd, combination)

        if bdd_value != expression_value:
            if verbose_bad:
                print_bad_combination(combination, bdd_value, expression_value, slow_output, slow_time)
            return boolean_c(False)
        elif verbose_all or verbose_good:
            if not printed_header:
                print_combination(combination, bdd_value, printed_header, order, slow_output, slow_time)
                printed_header = True
            else:
                print_combination(combination, bdd_value, slow_output=slow_output, slow_time=slow_time)

    return boolean_c(True)


def calculate_reduction(bdd: BDD):
    count_before_reduction = 2 ** (len(bdd.layers[0][0].order) + 1) - 1
    count_after_reduction = bdd.get_node_count()
    return (1 - (count_after_reduction / count_before_reduction)) * 100, count_before_reduction, count_after_reduction

def test_bdd_actual_vs_best_order(bdd_actual: BDD, expression: str, best_order_combination_count: int = None):
    bdd_best = BDD()

    if best_order_combination_count is None:
        bdd_best.create_with_best_order(expression)
    else:
        bdd_best.create_with_best_order(expression, best_order_combination_count)

    actual_node_count = bdd_actual.get_node_count()
    best_node_count = bdd_best.get_node_count()

    print("BDD with actual order nodes count: " + str(actual_node_count))
    print("BDD with best order nodes count: " + str(best_node_count))

    if best_node_count < actual_node_count:
        diff = actual_node_count - best_node_count

        print("BDD with best order has " + str(diff) + " less ", end="")
        if diff == 1:
            print("node")
        else:
            print("nodes")

    # Reduction percentage
    actual_reduction_pe = calculate_reduction(bdd_actual)[0]
    print("BDD with actual order reduction percentage: " + str(round(actual_reduction_pe, 13)) + " %")
    best_reduction_pe = calculate_reduction(bdd_best)[0]
    print("BDD with best order reduction percentage: " + str(round(best_reduction_pe, 13)) + " %")

    if best_reduction_pe > actual_reduction_pe:
        print("BDD with best order is " + str(round(best_reduction_pe - actual_reduction_pe, 13)) + " % more reduced")


def generate_and_run_tests(
        diagram_count: int = 100,
        variable_count: int = 13,
        node_count: int = 7,
        best_order_combination_count: int = 5
):
    from src.tests.generator import generate_expression_and_order

    for expression, order in generate_expression_and_order(diagram_count, variable_count, node_count):
        run_tests(expression, order, best_order_combination_count=best_order_combination_count)
        print("-------------------------------------------------------------------------------------------------------")


def generate_and_test_diagrams_correctness(
        diagram_count: int = 100,
        variable_count: int = 13,
        node_count: int = 7,
):
    from src.tests.generator import generate_bdd_diagrams

    diagrams = generate_bdd_diagrams(diagram_count, variable_count, node_count)

    for diagram in diagrams:
        expression = diagram.layers[0][0].expression
        order = diagram.layers[0][0].order

        check_bdd_solution(diagram, expression, order)
        print("-------------------------------------------------------------------------------------------------------")
    return diagrams


def run_tests(
        expression: str,
        order: str,
        verbose_all: bool = False,
        verbose_bad: bool = True,
        verbose_good: bool = False,
        slow_time: float = None,
        best_order_combination_count: int = None
):
    print("\n---------------------------------------------------------------------------------------------------------")

    print("Test parameters:")
    print("\tExpression: " + expression)
    print("\tOrder: " + order)
    print("\tBest order max combinations count: " + str(best_order_combination_count))
    print("\tVerbose all: " + str(verbose_all))
    if not verbose_all:
        print("\tVerbose bad: " + str(verbose_bad))
        print("\tVerbose good: " + str(verbose_good))
    print("\tSlow time: " + str(slow_time))

    print("-----------------------------------------------------------------------------------------------------------")

    start = time_ms()

    # Create BDD with actual order entered in arguments
    bdd_actual = BDD().create(expression, order)

    end = time_ms() - start
    print("BDD creation took: " + str(end) + " milliseconds")

    print("-----------------------------------------------------------------------------------------------------------")

    start = time_ms()

    # Check BDD correctness
    print("BDD correctness: "
          + check_bdd_solution(bdd_actual, expression, order, verbose_all, verbose_bad, verbose_good, slow_time)
          )

    end = time_ms() - start

    #TODO :: Remove this debug if
    if end < 0:
        pass

    print("BDD correctness check took: " + str(end) + " milliseconds")

    print("-----------------------------------------------------------------------------------------------------------")

    start = time_ms()

    # Best order test
    test_bdd_actual_vs_best_order(bdd_actual, expression, best_order_combination_count)

    end = time_ms() - start
    print("BDD best order vs actual order test took: " + str(end) + " milliseconds")

    print("-----------------------------------------------------------------------------------------------------------")

    reduction_percentage, nodes_count_before_reduction, nodes_count_after_reduction = calculate_reduction(bdd_actual)
    reduction_nodes_diff_count = nodes_count_before_reduction - nodes_count_after_reduction

    # Reduction percentage
    print("BDD reduction: " + str(round(reduction_percentage, 13)) + " %")
    print("BDD nodes count before reduction: " + str(nodes_count_before_reduction))
    print("BDD nodes count after reduction: " + str(nodes_count_after_reduction))
    print("BDD nodes difference before reduction and after reduction: " + str(reduction_nodes_diff_count))
