from src.bdd.Node import Node


# First reduction when creating the diagram
# 1. If I create children on a given layer
# 2. Check if I don't already have the child I'm creating on the layer
# 3. If yes, I just connect the parent to the found node without creating a duplicate

# Second reduction always when creating
# 1. At the end 0 and 1 represent nodes
# 2. Let's take nodes 0 and 1 and connect them appropriately
# 3. Then, if the left and right node are the same, it is useless.
# 4. Delete the node and connect it to either 0 or 1 (depending on which side is right or left)

# Third reduction after creation
# 1. If the expression is definitely equal to 1. If so, connect it to 1.
# 2. If the expression definitely equals 0. If yes, let's connect it to 0.

# 3. If you have a '+' in the expression. Then you decompose according to Shannon's decomposition and return.
# 4. If you don't have a '+' in the expression.
# Example A B C D
# If A = 1 then you have B C D.
# If A = 0, you have 0.
# Example you have one letter for example X. You just add it


# Checks if we need to perform a second reduction of a node in expression
def check_second_reduction(node):
    # If the left and right child of a node are the same, but are not '0' or '1' then return True
    return node.left is not None and node.right is not None \
        and (node.left != BDD.get_node_one() or node.left != BDD.get_node_zero()) \
        and (node.right != BDD.get_node_one() or node.right != BDD.get_node_zero()) \
        and node.left == node.right


# Remove all duplicate letters from a expression node
def remove_duplicate_letters_from_node(node):
    # Check if we can remove duplicates
    if node is None or len(node) < 2:
        return node

    # New expression after reduction
    new_expression = []
    # Last letter that was processed in the loop
    last_letter = str()

    # For each letter in node (a part of DNF expression that does not have a '+' sign.)
    for letter in node:
        # If we the last letter we processed is the same as current one we skip iteration
        if last_letter == letter:
            continue

        # Append current letter to new expression
        new_expression.append(letter)

        # Save current letter as last processed letter
        last_letter = letter

    # Convert the expression from list to string
    return ''.join(new_expression)


# Remove all duplicate letter from a expression
def remove_duplicate_letters_from_expression(expression):
    # Example would be "a+bb+C" which would result in "a+b+C"

    # We split the expression into '+' separated nodes
    expression = expression.split('+')

    # Holds the new expression after removing duplicates
    new_expression = []

    # For each node in separated expression
    for node in expression:
        # We remove duplicate letters from node and add it to the new expression
        new_expression.append(remove_duplicate_letters_from_node(node))

    # Lastly we convert the new expression to a string and remove any leading or trailing '+' signs
    return '+'.join(new_expression).strip('+')


# Checks if an expression contains a node that has a positive and negative letter multiplying
def check_true_times_false_case(expression):
    # Holds all letters present in expression
    alphabet = []

    # For each letter in the expression
    for letter in expression:

        # If the letter is not present in the alphabet
        if letter not in alphabet:
            # We add it (once due to the condition above)
            alphabet.append(letter)

    # For each letter in alphabet
    for letter in alphabet:
        # If we find that the alphabet contains both uppercase and lowercase letter of same value then the expression
        # has for example "aA" which results in '0' so we return True
        if letter.lower() in alphabet and letter.upper() in alphabet:
            return True

    # If we have not found any letter that has both uppercase and lowercase version in alphabet then we return False
    return False


# Removes all nodes from the expression that has a positive and negative letter multiplying
def remove_zero_nodes_from_expression(expression):
    # We split the expression into '+' separated nodes
    expression = expression.split('+')

    # Holds the new expression after removing zero nodes
    new_expression = []

    # For each node in the separated expression
    for node in expression:
        # If we do not have a True times False case. For example (abA or aA)
        if not check_true_times_false_case(node):
            # We add the node to the new expression
            new_expression.append(node)

    # Lastly we convert the new expression to a string and remove any leading or trailing '+' signs
    return '+'.join(new_expression).strip('+')


# Runs both minimization algorithms on a given expression
def minimize_expression(expression):
    # Minimize the  expression by removing duplicates and zero statements
    return remove_zero_nodes_from_expression(remove_duplicate_letters_from_expression(expression))


def check_for_terminator(node):
    return node == BDD.get_node_one() or node == BDD.get_node_zero()


# Generates all combinations of order
def get_combinations(s, count: int = None):
    from itertools import permutations
    perms = permutations(s)
    combinations = []
    for p in perms:
        if set(p) == set(s):
            combinations.append(''.join(p))
            if count is not None and len(combinations) == count:
                break
    return combinations


def replace_root(root):
    if root.left == root.right:
        return root.left
    return None


def get_expression_alphabet(expression: str):
    # Holds all letters present in expression
    alphabet = []

    # For each letter in the expression
    for letter in expression:
        if letter == '+':
            continue
        # If the letter is not present in the alphabet
        if letter.lower() not in alphabet:
            # We add it (once due to the condition above)
            alphabet.append(letter.lower())

    return alphabet


class BDD:
    node_one = Node('1', '1')
    node_one.value = '1'
    node_zero = Node('0', '0')
    node_zero.value = '0'

    def __init__(self):
        self.count = None
        self.layers = None
        self.order = None
        self.variable_count = None

    def initialize(self, expression: str, order: str = None):
        # Initialize layers list
        self.layers = []
        self.count = 0
        self.variable_count = 0

        # If order is not None we can set it as order of root node in this BDD
        if order is not None:
            self.order = order.lower()

        # If we have no expression connect  root to '0'
        if expression is None or len(expression) == 0:
            self.layers.append([BDD.get_node_zero()])
        else:
            # We minimize the initial expression
            node = Node(minimize_expression(expression), order)

            # If by minimizing we have an empty expression connect to '0'
            if len(node.expression) == 0:
                self.layers.append([BDD.get_node_zero()])

            # Else append the minimized expression to the root
            else:
                self.layers.append([node])

    # BDD_create
    def create(self, expression: str, order: str):

        # Initializes expression which we will be creating BDD from
        self.initialize(expression, order)

        # For each letter in order
        for _ in self.order:
            # Create new layer of nodes
            self.layers.append([])

            # For each node in layer above the new one
            for node in self.layers[-2]:
                # Create children of given order
                if node.order is not None and len(node.order) != 0:
                    node.create_children(node.order[0], self.layers[-1])

            self.s_reduction()

            # If did not create any children, remove the empty layer
            if self.layers[-1] is not None and len(self.layers[-1]) == 0:
                self.layers.remove(self.layers[-1])

        # Counts nodes of the reduced expression represented by the BDD
        self.get_node_count()
        self.get_variable_count()
        return self

    # BDD_create_with_best_order
    def create_with_best_order(self, expression: str, max_combinations: int = None):

        # Get string containing all letters in the expression
        alphabet = "".join(get_expression_alphabet(expression))

        if max_combinations is None or max_combinations <= 0:
            max_combinations = len(alphabet)

        # Get combinations of all letters in the expression
        combinations = get_combinations(alphabet, max_combinations)

        # Holds the best order of reduction
        best_order = ""

        # Holds smallest number of nodes
        smallest_count = float('inf')

        # For each letter of the expression's alphabet
        for combination in combinations:
            # Create a new BDD
            self.create(expression, combination)
            # Track current count of nodes
            current_count = self.get_node_count()
            # If the current count is smaller than the smallest tracked count
            if current_count < smallest_count:
                # Set current count as the smallest tracked count
                smallest_count = current_count
                # Save current order as the best one possible
                best_order = combination

        # Return BDD with the best order
        return self.create(expression, best_order)

    # Gets count of nodes in layers
    def get_node_count(self):
        # Holds count of nodes in layers
        self.count = 0
        # For each layer
        for layer in self.layers:
            # Add its length to the counter
            self.count += len(layer)
        # Return the count
        return self.count

    def get_variable_count(self):
        self.variable_count = len(get_expression_alphabet(self.layers[0][0].expression))
        return self.variable_count

    # BDD_use
    def use(self, combination: str):
        # Holds current position in BDD
        current_node = self.layers[0][0]

        # For each value in combination we received
        for index, value in enumerate(combination):

            if check_for_terminator(current_node):
                return current_node

            # If order's letter doesn't match the current node label then we skip it
            if current_node.value != self.order[index]:
                continue

            # If we got a '0' value we move left
            if value == '0':
                # We set current_node to it's left child
                current_node = current_node.left
            # Else if we got a '1' value we move left
            elif value == '1':
                # We set current_node to it's right child
                current_node = current_node.right

        # If we arrived at the end of the combination we return the last node of the combination
        return current_node

    @staticmethod
    def get_node_one():
        return BDD.node_one

    @staticmethod
    def get_node_zero():
        return BDD.node_zero

    def is_root(self, node):
        if self.layers is not None and len(self.layers) > 0:
            return node == self.layers[0][0]
        else:
            return False

    def __str__(self):

        # Holds string representation of the binary decision diagram
        string = str()

        # Creating separator for first layer
        if self.layers is not None and len(self.layers) != 0:
            print("--------")

        # For each layer
        for layer in self.layers:
            # Append all layer nodes to a string
            for node in layer:
                string += node.__str__()

            # Then append a layer separator
            if layer is not None and len(layer) != 0:
                string += "--------"

                # Lastly if we are not at the end of layer's list
                # Append new line character
                if layer is not self.layers[-1]:
                    string += '\n'

        # Return a string representation of the binary decision diagram
        return string

    def s_reduction(self):
        reversed_layers = list(reversed(self.layers))
        b_repeat = True

        while b_repeat:
            b_repeat = False
            for layer in reversed_layers:
                for node in layer:
                    # Second (duplicates) reduction

                    if check_second_reduction(node):
                        if self.is_root(node):
                            new_root = node.left
                            self.second_reduction(node, self.layers[0])
                            self.layers = [[new_root]]
                        else:
                            self.second_reduction(node, layer)
                            b_repeat = True

    def lookup_parent(self, node):
        for layer in self.layers:
            for parent in layer:
                if parent.left == node or parent.right == node:
                    return parent
        return None

    # Performs second reduction
    def second_reduction(self, node, nodes_layer):

        parent = self.lookup_parent(node)

        if parent is not None and parent.left == node:
            parent.left = node.left
        if parent is not None and parent.right == node:
            parent.right = node.right

        nodes_layer.remove(node)
