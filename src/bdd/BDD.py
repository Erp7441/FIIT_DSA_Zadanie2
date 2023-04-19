from src.bdd.Node import Node


# Prva redukcia pri vytvarani diagramu
# 1. Pokial vytvaram deti na danom layeri
# 2. Checknem ci uz nemam dane dieta co vytvaram na layeri
# 3. Pokial ano tak len spojim rodica s najdenym nodom bez toho aby som vytvoril duplikat

# Druha redukcia vzdy pri vytvarani
# 1. Na konci 0 a 1 reprezentuju nody
# 2. Spravime si nody 0 a 1 a adekvatne ich ponapajame
# 3. Potom pokial noda ma left a right to iste tak je zbytocna
# 4. Zmazeme tu nodu a napojime ju bud na 0 alebo 1 (podla toho aku ma pravu resp. lavu stranu)

# Tretia redukcia po vytvorei
# 1. Ak sa vyraz definitivne rovna 1. Ak ano napojime ho do 1.
# 2. Ak sa vyraz definitivne rovna 0. Ak ano napojime ho do 0.

# 3. Ak mas vo vyraze '+'. Tak rozkladas podla Shannonovej dekompozicie a return.
# 4. Ak nemas vo vyraze '+'.
# Priklad A B C D
# Pokial je A = 1 tak mas B C D.
# Pokial je A = 0 tak mas 0.
# Priklad mas jedno pismeno napriklad X. Len ho dosadis

class BDD:
    node_one = Node('1', '1')
    node_zero = Node('0', '0')

    def __init__(self, order, expression):
        self.layers = []
        self.order = order
        self.layers.append([Node(order, expression)])

    # BDD_create
    def create(self):
        for letter in self.order:
            if letter == '+':
                continue
            self.layers.append([])
            for node in self.layers[-2]:
                if node.order is not None and len(node.order) != 0:
                    node.create_childs(node.order[0], self.layers[-1])
                    if node.left is not None and node.right is not None and node.left == node.right:
                        # Second reduction
                        self.replace_node(node, self.layers[-2], self.layers[-3], self.layers[-1])


    # BDD_create_with_best_order
    def create_with_best_order(self):
        # TODO:: Implement
        pass

    # BDD_use
    def use(self):
        # TODO:: Implement
        pass

    @staticmethod
    def get_node_one():
        return BDD.node_one

    @staticmethod
    def get_node_zero():
        return BDD.node_zero

    def __str__(self):
        string = str()
        for layer in self.layers:
            for node in layer:
                string += node.__str__()
            if layer is not None and len(layer) != 0:
                string += "---------\n"
        return string

    def replace_node(self, node, nodes_layer, parents_layer, childs_layer):

        if node is None or nodes_layer is None or parents_layer is None or childs_layer is None:
            return

        nodes_layer.remove(node)
        for parent in parents_layer:
            if parent.left == node:
                # TODO:: correct?
                parent.left = BDD.get_node_one()
            elif parent.right == node:
                parent.right = BDD.get_node_one()

        children_to_remove = []
        for child in childs_layer:
            if child == node.left or child == node.right:
                children_to_remove.append(child)

        for child in children_to_remove:
            childs_layer.remove(child)

        nodes_layer.append(BDD.get_node_one())
