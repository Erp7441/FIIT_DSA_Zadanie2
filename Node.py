class Node:
    def __init__(self, expression, order):
        self.order = order
        self.left = None
        self.right = None
        self.expression = expression

    def remove_occurrences(self, array: list, letter):
        new_list = []
        for element in array:
            if letter not in element:
                new_list.append(element)
        return '+'.join(new_list)

    def expression_handler(self, letter, replacement):
        letter = letter.lower()
        if replacement == '1':
            self.expression = self.remove_occurrences(self.expression.split('+'), letter.upper())
            self.expression = self.expression.replace(letter.lower(), '')
        elif replacement == '0':
            self.expression = self.remove_occurrences(self.expression.split('+'), letter.lower())
            self.expression = self.expression.replace(letter.upper(), '')
        return self.expression

    def create_childs(self, letter, layer):

        left_expression = self.expression_handler(letter, '0')
        right_expression = self.expression_handler(letter, '1')

        self.join_child(left_expression, '0', letter)
        self.join_child(right_expression, '1', letter)

        layer.append(self.left)
        layer.append(self.right)

    # Check ci existuje nejaka noda ktorej expression == tej ktoru chcem vytvorit. Ak ano tak napojim.
    def join_child(self, expression, side:str, letter:str):

        if expression == '0':
            # Napojim do nuly kokot
            if side == '1':
                self.right = Node(None, "0")
            elif side == '0':
                self.left = Node(None, "0")
        elif expression == '1':
            if side == '1':
                self.right = Node(None, "1")
            elif side == '0':
                self.left = Node(None, "1")
        else:
            if side == '1':
                self.right = Node(expression, letter)
            elif side == '0':
                self.left = Node(expression, letter)
