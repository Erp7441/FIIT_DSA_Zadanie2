from Node import Node


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
    node_one = Node(None, "1")
    node_zero = Node(None, "0")

    def __init__(self, order, expression):
        self.layers = []
        self.order = order
        self.layers.append([Node(order, expression)])

    def BDD_create(self):
        for letter in self.order:
            self.layers.append([])
            for node in self.layers[-2]:
                node.create_childs(letter, self.layers[-1])
                # Tu budem robit druhu redukciu :) Useless node

    def BDD_create_with_best_order(self):
        pass

    def BDD_use(self):
        pass
