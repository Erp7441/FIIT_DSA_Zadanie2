def shannon_insert_value(expression, value, insertion_value):

    # 1. Ak je replacement '0' dosadime na kazdy letter 0
    # 1.1 Ak je vo vyraze male pismeno dosadime 0 ak je velke tak 1
    # 2. Ak je replacement '1' dosadime na kazdy letter 1
    # 2.1 Ak je vo vyraze male pismeno tak 1 ak je velke tak 0
    # VYSLEDOK = list casti ktore maju to pismeno nahradeny korespondujucimi hodnotami

    new_expression = []
    for letter in expression:
        if letter.lower() == value.lower():
            if insertion_value == '1':
                if letter.islower():
                    new_expression.append('1')
                else:
                    new_expression.append('0')
            elif insertion_value == '0':
                if letter.islower():
                    new_expression.append('0')
                else:
                    new_expression.append('1')
        else:
            new_expression.append(letter)
    return ''.join(new_expression).strip('+').split('+')


def shannon_extract_one(part):
    new_expression = str()
    for letter in part:
        if letter != '1':
            new_expression += letter
    return new_expression


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
        # Example 'b' ; Control = 'b' #
        if len(node) == 1 and node.lower() == control.lower():
            values.append(evaluate_letter(node, replacement))
        # Example 'bb' ; Control = 'b' #
        elif len(node) > 1 and node[0].lower() == control.lower() and check_expression_consists_of_same_letter(node):
            values.append(evaluate_letter(node[0], replacement))
        # Example 'b' #
        elif len(node) == 1:
            values.append(node)
        # Example 'Bc' or 'Bb' #
        elif len(node) > 1:
            # 'Bb' case #
            from BDD import check_true_times_false_case
            if check_true_times_false_case(node):
                values.append('0')
                continue
            # 'Bc' case #
            new_node = str()
            for letter in node:
                if evaluate_letter(letter, replacement) != '1':
                    new_node += letter
            values.append(new_node)

    if len(values) == 0:
        return None

    if '1' in values:
        return '1'

    for value in values:
        if value != '0':
            return None

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
    def shannons_decomposition(self, letter: str, replacement: str):

        if self.expression is None or letter is None or replacement is None:
            return None

        if self.expression == "b+Bc":
            print(end="")

        definitive = definitive_value(self.expression, letter, replacement)
        if definitive == '1' or definitive == '0':
            return definitive

        parts = shannon_insert_value(expression=self.expression, value=letter, insertion_value=replacement)
        new_expression = [] # 3. Vytvorime si novy list (vyrazu)

        # 4. Prechadzame kazdu jednu cast listu casti
        for part in parts:
            # 4.2 Ak v casti listu bude '1' vybereme z danej casti listu '1' a pridame ju do noveho listu
            if '1' in part:
                new_expression.append(shannon_extract_one(part))
            # 4.1 Ak v casti listu bude '0' ignorujeme tu cast
            # 4.3 Ak v casti listu nebude '0' ani '1' pridavame ju do noveho listu
            elif '0' not in part:
                new_expression.append(part)

        if len(new_expression) == 0 and (definitive != '1' or definitive != '0'):
            return evaluate_letter(letter, replacement)

        return '+'.join(new_expression).strip('+')

    def create_childs(self, letter: str, layer):

        if not self.check_create_childs():
            return

        left_expression = self.shannons_decomposition(letter, '0')
        right_expression = self.shannons_decomposition(letter, '1')

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
