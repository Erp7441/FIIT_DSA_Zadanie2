def remove_occurrences(array: list, letter):
    new_list = []
    for element in array:
        if letter not in element:
            new_list.append(element)
    return '+'.join(new_list)


def evaluate_letter(letter: str, replacement: str):
    if letter.islower():
        if replacement == '1':
            return '1'
        else:
            return '0'
    else:
        if replacement == '1':
            return '0'
        else:
            return '1'


def definitive_value(expression: str, control: str, replacement: str):
    expression = expression.split('+')
    values = []
    for node in expression:
        if len(node) == 1 and node.lower() == control.lower():
            values.append(evaluate_letter(node, replacement))

    if len(values) == 0:
        return None

    if '1' in values:
        return '1'
    return '0'


class Node:
    def __init__(self, expression: str, order: str):
        self.order = order
        self.left = None
        self.right = None
        self.expression = expression
        self.value = None
        if order is not None and len(order) != 0:
            self.value = order[0].upper()

    def expression_handler(self, letter: str, replacement: str):

        if self.expression is None:
            return None

        new_expression = None
        if replacement == '1':
            new_expression = remove_occurrences(self.expression.split('+'), letter.upper())
            new_expression = new_expression.replace(letter.lower(), '')

        elif replacement == '0':
            new_expression = remove_occurrences(self.expression.split('+'), letter.lower())
            new_expression = new_expression.replace(letter.upper(), '')

        if len(new_expression) == 0:
            return definitive_value(self.expression, letter, replacement)

        return new_expression

    def create_childs(self, letter: str, layer):

        if not self.check_create_childs():
            return

        # TODO:: Handle empty expression
        left_expression = self.expression_handler(letter, '0')
        right_expression = self.expression_handler(letter, '1')

        self.join_child(left_expression, '0', letter)
        self.join_child(right_expression, '1', letter)

        layer.append(self.left)
        layer.append(self.right)

    # Check ci existuje nejaka noda ktorej expression == tej ktoru chcem vytvorit. Ak ano tak napojim.
    def join_child(self, expression: str, side: str, letter: str):
        from src.bdd.BDD import BDD

        if expression == '0':
            if side == '1':
                self.right = BDD.get_node_zero()
            elif side == '0':
                self.left = BDD.get_node_zero()
        elif expression == '1':
            if side == '1':
                self.right = BDD.get_node_one()
            elif side == '0':
                self.left = BDD.get_node_one()
        else:
            if side == '1':
                self.right = Node(expression, self.order.replace(letter, ''))
            elif side == '0':
                self.left = Node(expression, self.order.replace(letter, ''))

    def __str__(self):
        if self.value is not None and len(self.value) != 0:
            return self.value + ' '
        else:
            return ""

    def check_create_childs(self):
        from src.bdd.BDD import BDD
        if self == BDD.get_node_one() or self == BDD.get_node_zero():
            return False
        return True
