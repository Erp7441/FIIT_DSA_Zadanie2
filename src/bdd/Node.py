def remove_occurrences(array: list, letter):
    new_list = []
    for element in array:
        if letter not in element:
            new_list.append(element)
    return '+'.join(new_list)

def replace_occurence(array: list, letter, replacement):
    new_list = []
    for element in array:
        if letter not in element:
            new_list.append(replacement)
    return '+'.join(new_list)

def replace_expression_nodes(expression, letter):
    new_expression = expression.replace(letter, '')
    new_list = new_expression.split('+')
    '+'.join(new_list)


def check_expression_consists_of_same_letter(expression):
    b_same_letter = True
    for letter in expression:
        if letter != expression[0]:
            b_same_letter = False
            break
    return b_same_letter


def evaluate_letter(letter: str, replacement: str):
    if letter.isdigit() and (int(letter) == 1 or int(letter) == 0):
        return letter
    elif letter.isdigit():
        return None

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
        elif len(node) > 1 and node.lower() == control.lower() and check_expression_consists_of_same_letter(node):
            values.append(evaluate_letter(node[0], replacement))

    if len(values) == 0:
        return None

    if '1' in values:
        return '1'
    return '0'


def check_for_terminator(node):
    from src.bdd.BDD import BDD
    return node == BDD.get_node_one() or node == BDD.get_node_zero()


class Node:
    def __init__(self, expression: str, order: str):
        self.order = order
        self.left = None
        self.right = None
        self.expression = expression
        self.value = None
        if order is not None and len(order) != 0:
            self.value = order[0].upper()

    # Sano
    def expression_handler(self, letter: str, replacement: str):

        if self.expression is None:
            return None

        # 1. Ak je replacement '0' dosadime na kazdy letter 0
            # 1.1 Ak je vo vyraze male pismeno dosadime 0 ak je velke tak 1
        # 2. Ak je replacement '1' dosadime na kazdy letter 1
            # 2.1 Ak je vo vyraze male pismeno tak 1 ak je velke tak 0
        # VYSLEDOK = list casti ktore maju to pismeno nahradeny korespondujucimi hodnotami
        # 3. Vytvorime si novy list (vyrazu)
        # 4. Prechadzame kazdu jednu cast listu casti
            # 4.1 Ak v casti listu bude '0' ignorujeme tu cast
            # 4.2 Ak v casti listu bude '1' vybereme z danej casti listu '1' a pridame ju do noveho listu
            # 4.3 Ak v casti listu nebude '0' ani '1' pridavame ju do noveho listu

        return new_expression

    def create_childs(self, letter: str, layer):

        if not self.check_create_childs():
            return

        left_expression = self.expression_handler(letter, '0')
        right_expression = self.expression_handler(letter, '1')

        self.join_child(left_expression, '0', letter)
        self.join_child(right_expression, '1', letter)

        # Prva redukcia
        found_duplicate_l = False
        found_duplicate_r = False
        for child in layer:
            if child == self.left:
                self.left = child
                found_duplicate_l = True
            elif child == self.right:
                self.right = child
                found_duplicate_r = True

        if not found_duplicate_l and not check_for_terminator(self.left):
            layer.append(self.left)
        if not found_duplicate_r and not check_for_terminator(self.right):
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
        string = str()
        if self.value is not None and len(self.value) != 0:
            string += self.value + ': '
        else:
            return ""
        if self.left is not None and self.left.value is not None and len(self.left.value) != 0:
            string += self.left.value + ', '
        else:
            string += 'x, '
        if self.right is not None and self.right.value is not None and len(self.right.value) != 0:
            string += self.right.value + '\n'
        else:
            string += 'x\n'
        return string

    def __eq__(self, other):
        if other is None: return False
        return self.value == other.value and self.expression == other.expression

    def check_create_childs(self):
        from src.bdd.BDD import BDD
        if self == BDD.get_node_one() or self == BDD.get_node_zero():
            return False
        return True
