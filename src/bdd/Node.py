
# Shannon's helper function that inserts a '0' or '1' value into the expression
def shannon_insert_value(expression, value, insertion_value):

    # 1. If the "replacement" is '0', replace each letter that equals "value" with "replacement" accordingly
    # 1.1 If there is a lowercase letter in the expression, set 0 if it is an uppercase letter, set 1
    # 2. If the "replacement" is '1', replace each letter that equals "value" with "replacement" accordingly
    # 2.1 If there is a lowercase letter in the expression, set 1 if it is an uppercase letter, set 0
    # RESULT = list of parts that have that letter replaced with corresponding values

    # Holds the new expression after inserting "insertion_value" instead of "value"
    new_expression = []

    # For each letter in expression
    for letter in expression:
        # If the letter is of same value as the one we are looking for
        if letter.lower() == value.lower():
            # If we are inserting '1'
            if insertion_value == '1':
                # If the letter is lowercase
                if letter.islower():
                    # Replace it with '1' in the new expression
                    new_expression.append('1')
                # Else if it is uppercase
                else:
                    # Replace it with '0' in the new expression
                    new_expression.append('0')
            # If we are inserting '0'
            elif insertion_value == '0':
                # If the letter is lowercase
                if letter.islower():
                    # Replace it with '0' in the new expression
                    new_expression.append('0')
                # Else if it is uppercase
                else:
                    # Replace it with '0' in the new expression
                    new_expression.append('1')
        # Else we append the letter to the new expression
        else:
            new_expression.append(letter)

    # Lastly we convert the new expression to a string and remove any leading or trailing '+' signs and then split it
    # To get a list out of the new expression
    return ''.join(new_expression).strip('+').split('+')


# Shannon's helper function that removes character '1' from a given expression
def shannon_extract_one(expression):

    # Holds a new expression without '1's in it
    new_expression = str()

    # For each letter in the expression
    for letter in expression:
        # If the letter is not '1'
        if letter != '1':
            # We add it to the new expression
            new_expression += letter

    # Return new expression with '1' characters removed
    return new_expression


# Checks if the Provided expression consists of one character
def check_expression_consists_of_same_letter(expression):
    # For each letter in expression
    for letter in expression:
        # If the letter is not the same as the first one in the expression
        if letter != expression[0]:
            # We return False as this means the expression does not consist of same letter
            return False

    # If we got through the loop that means the expression consists of same letter and we return True
    return True


# Evaluate letter value given a replacement value
def evaluate_letter(letter: str, replacement: str):

    # If the letter is digit, and it's value is 0 or 1. Then return the letter
    if letter.isdigit() and (int(letter) == 1 or int(letter) == 0):
        return letter
    # Else if it is a number other than 0 or 1 then exit this function
    elif letter.isdigit():
        return None

    # If it is lowercase letter we return the replacement value
    if letter.islower():
        return replacement
    # Else if it is an uppercase letter we return the opposite of replacement value
    else:
        if replacement == '1':
            return '0'
        else:
            return '1'


# Evaluates a definitive value of a expression
def definitive_value(expression: str, control: str, replacement: str):

    # We split the expression into '+' separated nodes
    expression = expression.split('+')

    # Holds the values of all nodes in the expression
    values = []

    # For each node in the expression
    for node in expression:

        # If the node is a single letter that matches the one we are looking for
        # Example 'b' ; Control = 'b'
        if len(node) == 1 and node.lower() == control.lower():
            # Append the evaluation of this letter to the list of values
            values.append(evaluate_letter(node, replacement))

        # If the node is consisting of multiple letters that are the same then we evaluate just the first letter and
        # ignore the rest of the node
        # Example 'bb' ; Control = 'b'
        elif len(node) > 1 and node[0].lower() == control.lower() and check_expression_consists_of_same_letter(node):
            values.append(evaluate_letter(node[0], replacement))
        # If the node is a single letter is not the one we are looking for
        # Example 'b'
        elif len(node) == 1:
            # We append it to the values without evaluation
            values.append(node)
        # If the node is longer then 1 letter and does not contain the letter we are looking for
        # Example 'Bc' or 'Bb'
        elif len(node) > 1:
            # First we check if the nod does not evaluate to '0'
            # 'Bb' case
            from src.bdd.BDD import check_true_times_false_case
            # If it evaluates to '0'
            if check_true_times_false_case(node):
                # We append '0' to the list of values
                values.append('0')
                # And continue to next iteration
                continue

            # 'Bc' case #
            # Holds the new node
            new_node = str()
            # For each letter in node
            for letter in node:
                # If the value of letter is not '1'
                if evaluate_letter(letter, replacement) != '1':
                    # We append it to the new node
                    new_node += letter
            # Then we append the new node to the list of values
            values.append(new_node)

    # If we don't have any values we have nothing
    if len(values) == 0:
        return None

    # If we have at least one '1' value that means that "<something>+1" in boolean algebra always equals '1'
    if '1' in values:
        return '1'

    # If we haven't found any '1' value. We look if each of the values is a '0'

    # For each value in values list
    for value in values:
        # If a value is not '0' that means that the expression does not have a definitive value
        if value != '0':
            # We return None
            return None

    # If we have reached the end of the for loop. That means each value in the values list is a '0'.
    return '0'


# Checks if the node provided is either a '1' or a '0'
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

    # Decomposes the expression according to the Shannon's rules of decomposition
    def shannon_decomposition(self, letter: str, replacement: str):

        # Check prerequisites for Shannon's decomposition
        if self.expression is None or letter is None or replacement is None:
            return None

        # If expression has a definitive value. We return the value.
        definitive = definitive_value(self.expression, letter, replacement)
        if definitive == '1' or definitive == '0':
            return definitive

        # We insert the replacement inside the expression
        parts = shannon_insert_value(self.expression, letter, replacement)

        # Holds new expression after Shannon's reduction
        new_expression = []

        # For each part of the expression that has gone through the replacement process
        for part in parts:
            # If the part has '1' in it, we append it to the new expression without that '1'
            if '1' in part:
                new_expression.append(shannon_extract_one(part))
            # If the part has '0' in it, we ignore it
            # Else if the par has anything else in it except '0' or '1' we simply add it to the new expression
            elif '0' not in part:
                new_expression.append(part)

        # If the new expression is empty and definitive values are not '1' or '0'
        # We return '0'
        if len(new_expression) == 0 and (definitive != '1' or definitive != '0'):
            return '0'

        # Join the separated expression with '+' and strip any leading or trailing '+' signs
        return '+'.join(new_expression).strip('+')

    # Creates children for this node given a specific letter
    def create_children(self, letter: str, layer):

        # Check if this is not '0' or '1' node
        if not self.check_create_children():
            return

        # Decomposes the expression according to Shannon's rules of decomposition for both left and right child
        left_expression = self.shannon_decomposition(letter, '0')
        right_expression = self.shannon_decomposition(letter, '1')

        # Connect the newly created children to their appropriate sides
        self.join_child(left_expression, '0', letter)
        self.join_child(right_expression, '1', letter)

        # Check duplicates
        if self.left == self.right:
            self.left = self.right

        # We look for duplicates inside the layers
        found_duplicate_l = False
        found_duplicate_r = False

        # For each child in the layer
        for child in layer:
            # If a child with the same parameters as our left child already exists inside the layer
            if child == self.left:
                # We connect it as our left child
                self.left = child
                # Save that we found a duplicate of left child
                found_duplicate_l = True

                if found_duplicate_r:
                    break

            # If a child with the same parameters as our right child already exists inside the layer
            if child == self.right:
                # We connect it as our right child
                self.right = child
                # Save that we found a duplicate of right child
                found_duplicate_r = True

                if found_duplicate_l:
                    break

        # If we have not found any duplicates, and we are not '0' or '1' node then append our children to the layer
        if not found_duplicate_l and not check_for_terminator(self.left):
            layer.append(self.left)
        if not found_duplicate_r and not check_for_terminator(self.right) and self.left != self.right:
            layer.append(self.right)

    # Creates a child based on expression and join's it to the appropriate side
    def join_child(self, expression: str, side: str, letter: str):
        from src.bdd.BDD import BDD

        # If the expression is '0'
        if expression == '0':
            # We set '0' node to the right or left side based on the value of "side" attribute
            if side == '1':
                self.right = BDD.get_node_zero()
            elif side == '0':
                self.left = BDD.get_node_zero()
        # If the expression is '0'
        elif expression == '1':
            # We set '1' node to the right or left side based on the value of "side" attribute
            if side == '1':
                self.right = BDD.get_node_one()
            elif side == '0':
                self.left = BDD.get_node_one()
        else:
            # We create a new node with "expression" provided and
            # set it to the right or left side based on the value of "side" attribute
            if side == '1':
                self.right = Node(expression, self.order.replace(letter, ''))
            elif side == '0':
                self.left = Node(expression, self.order.replace(letter, ''))

    # Converts this node to string
    def __str__(self):

        # Holds string representation of the node of binary decision diagram
        string = str()

        # If we have a value append it to the string
        if self.value is not None and len(self.value) != 0:
            string += self.value + ': '
        # Else we have nothing to convert to string
        else:
            return ""
        # If we have a left child convert its value to string and append it to the string representation of node
        if self.left is not None and self.left.value is not None and len(self.left.value) != 0:
            string += self.left.value + ', '
        # Else append representation of empty node
        else:
            string += 'x, '
        # If we have a right child convert its value to string and append it to the string representation of node
        if self.right is not None and self.right.value is not None and len(self.right.value) != 0:
            string += self.right.value + '\n'
        # Else append representation of empty node
        else:
            string += 'x\n'

        # Return the string representation of the node of binary decision diagram
        return string

    # Compares the equality of two nodes
    def __eq__(self, other):
        # If the other node does not exist then return False
        if other is None:
            return False
        # Else return the comparison of the equality of both their values and expressions
        return self.expression == other.expression

    # Checks if this node is not equal to '1' or '0' node
    def check_create_children(self):
        from src.bdd.BDD import BDD
        return not (self == BDD.get_node_one() or self == BDD.get_node_zero())
