import random
import string
from random import randint
from src.bdd.BDD import BDD, get_combinations, get_expression_alphabet
from src.utils.constants import get_c_diagram_count, get_c_variable_count, get_c_node_count

def generate_dnf_expression(variable_count, node_count):

    alphabet = [random.choice(string.ascii_lowercase) for _ in range(variable_count)]
    nodes = []

    for _ in range(node_count):
        literals = []

        for i in range(variable_count):
            if random.random() < 0.5:
                literals.append(alphabet[i])

            elif random.random() < 0.5:
                literals.append(alphabet[i].upper())

        nodes.append(''.join(literals))

    return '+'.join(nodes).strip('+')


def generate_dnf_expressions(expression_count, variable_count, node_count):
    expressions = []
    for _ in range(expression_count):
        expressions.append(generate_dnf_expression(variable_count, node_count))
    return expressions


def generate_bdd_diagrams(
        diagram_count: int = get_c_diagram_count(),
        variable_count: int = get_c_variable_count(),
        node_count: int = get_c_node_count()
):
    expressions = generate_dnf_expressions(diagram_count, variable_count, node_count)
    diagrams = []
    for i in range(diagram_count):
        diagrams.append(BDD().create_with_best_order(expressions[i]))
    return diagrams


def generate_expression_and_order(
        diagram_count: int = get_c_diagram_count(),
        variable_count: int = get_c_variable_count(),
        node_count: int = get_c_node_count(),
        max_combinations: int = None,
):
    expressions = generate_dnf_expressions(diagram_count, variable_count, node_count)
    expressions_orders = []

    b_no_max_comb = max_combinations is None

    for expression in expressions:

        # Get string containing all letters in the expression
        alphabet = "".join(get_expression_alphabet(expression))

        if b_no_max_comb:
            max_combinations = min(len(alphabet), 5)

        # Get combinations of all letters in the expression
        combinations = get_combinations(alphabet, max_combinations)
        expressions_orders.append((expression, combinations[randint(0, max_combinations-1)]))

    return expressions_orders
