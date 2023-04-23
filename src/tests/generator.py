import random
import string
from src.bdd.BDD import BDD


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


def generate_bdd_diagrams(diagram_count: int = 100, variable_count: int = 13, node_count: int = 200):
    expressions = generate_dnf_expressions(diagram_count, variable_count, node_count)
    diagrams = []
    for i in range(diagram_count):
        diagrams.append(BDD().create_with_best_order(expressions[i]))
    return diagrams
