from src.bdd.BDD import BDD

#print(check("abc+ABC", "abc", "111"))
#print(check("aAbcde+Eb+bcD+cd+a", "abcde", "01011"))


#node = Node("aC+abc+Ab+Bc", "111")

#node.expression_handler('a', '0')
#node.expression_handler('b', '1')

#print(node.expression)

#bdd = BDD("aC+abc+Ab+Bc", "abc")
bdd = BDD("abc+ABC", "abc")
bdd.BDD_create()

print(bdd)