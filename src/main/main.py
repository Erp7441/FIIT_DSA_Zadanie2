from src.bdd.BDD import BDD

def main():
    bdd = BDD("aC+abc+Ab+Bc", "abc")
    bdd.create()
    print(bdd)
def test():
    from src.bdd.Node import definitive_value
    print(definitive_value("b+Bc", 'b', '1'))
    print(definitive_value("b+Cc", 'b', '1'))
    print(definitive_value("aC+abc+Ab+aBc+a", 'a', '1'))
    print(definitive_value("aC+abc+Ab+aBc+a", 'a', '0'))
    print(definitive_value("aC+abc+Ab+aBc+b", 'a', '1'))
    print(definitive_value("aC+abc+Ab+aBc+b", 'a', '0'))


# test()
main()
