from src.bdd.BDD import BDD

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
# 1. Ak sa vyraz definitivne rovna 1. Ak ano napojime ho do 1 a return.
# 2. Ak sa vyraz definitivne rovna 0. Ak ano napojime ho do 0 a return.

# 3. Ak mas vo vyraze '+'. Tak rozkladas podla Shannonovej dekompozicie a return.
# 4. Ak nemas vo vyraze '+'.
# Priklad A B C D
# Pokial je A = 1 tak mas B C D.
# Pokial je A = 0 tak mas 0.
# Priklad mas jedno pismeno napriklad X. Len ho dosadis

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
