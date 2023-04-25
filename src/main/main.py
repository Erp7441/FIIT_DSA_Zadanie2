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

# TODO 's:
    # 1. How long everything took
    # 2. Comparison between BDD_Create and BDD_Create_with_best_order
    # 3. Random generate and test functions (minimum test 100 with 13 literals)

# Test expressions:
    # 1.
        # Expression: wxLwokUd+wXywolNkVdUd+XwOVD+wXYlwolkVdu+WXylnkvdU+wxylwolNkvUd+WxylONVd+wxywolNkVdud+WxyOlNkdud+wxYLwLNkVdu+wloNkVd+wxYlwolKDUD+wxyolnkvuD+wYwlnKVud+xyWolNKVud+xywoLNku+WxloNkd+wxlnkVdud+wxylwolNKVd+wyLwONkdUd+xylwonkd+WxyWOlvd+wXLoLvUd+xYlolnVdu+wxywOLnkdu+WlWOlnKdud+WxlWolvud+wXYwlNKvd+Ylwolnkvud+ylolNkdu+wxlwOlnKVDUD+xyOlNkvdu+WYlnKVdud+ylwolnd+wxlwlnkVDu+wlwlnKvdud+WYoLnKvDuD+wyLwoKvd+XylwolNvdUd+WYLWnvdud+WxlOlNkvud+wxlwolnvud+WNvDu+WxYLnKUd+wylwonku+wyoLNd+xlKUd+WlWlNkvd+wxyokvdud+wxylolNkVd+wolnkdu+wxylwOnkVdu+wLNKvDu+xYLonkDuD+ylwOlnKv+WxylnKVuD+XyOlNKvDuD+wXwOlnkvdu+WXWolkDu+wxYlwoNkVdUd+wXLnd+xylwnKvdud+XYlwoNvdu+wxYlwolvd+WXYLWnkvd+WxyoLNKDU+Xolnkvd+xYwOLkD+wXwolkvd+wXylOlndud+WnVd+wYwolNVdud+xYlolnkv+wYlwonVDUD+wXyLkVUD+wxYlwlnKud+wylwolnkvDu+Wxylnkdu+wylwnkVdud+YWolnKvdUd+XYLwnKVdud+wxlwonvDuD+wxYlolnvd+wxYwoLnkdUd+xwOlnKdud+wxlwnkvdu+XLwLNkvDu
        # Order: lnkvdwouxy
        # Combination: 0000001010
    # 2.
        # Expression: HADu+tfDs+lCDw+zpqn+xSNy+AyDj+wCXr+lvYc+Zvxq+pKSl+jkAf+XAqc+vlWu+raZH+NLtc+ZpnL+nzFh+lkjh+Vrjt+qfpd
        # Order: nvwlxaupjrdfhqzyktsc
def main():
    # NODES COUNT BEFORE REDUCTION: self.nodes_before_count = 2**(len(order)+1) - 1

    #bdd = BDD().create_with_best_order("aC+abc+Ab+Bc")
    #path = bdd.use("100")
    #print(bdd, end="\n")
    #print(path, end=

    expression = "HADu+tfDs+lCDw+zpqn+xSNy+AyDj+wCXr+lvYc+Zvxq+pKSl+jkAf+XAqc+vlWu+raZH+NLtc+ZpnL+nzFh+lkjh+Vrjt+qfpd"
    order = "nvwlxaupjrdfhqzyktsc"

    bdd = BDD().create(expression, order)

    pass


def generate_and_test_diagrams(diagram_count: int = 100, variable_count: int = 13, node_count: int = 200):
    from src.tests.checker import check_bdd_solution
    from src.tests.generator import generate_bdd_diagrams

    diagrams = generate_bdd_diagrams(diagram_count, variable_count, node_count)

    for diagram in diagrams:
        expression = diagram.layers[0][0].expression
        order = diagram.layers[0][0].order

        print("BDD is: " + check_bdd_solution(diagram, expression, order))
        print("-----------------------------------------------------------")


def test():
    from src.tests.checker import test_bdd

    #expression = "wxLwokUd+wXywolNkVdUd+XwOVD+wXYlwolkVdu+WXylnkvdU+wxylwolNkvUd+WxylONVd+wxywolNkVdud+WxyOlNkdud+wxYLwLNkVdu+wloNkVd+wxYlwolKDUD+wxyolnkvuD+wYwlnKVud+xyWolNKVud+xywoLNku+WxloNkd+wxlnkVdud+wxylwolNKVd+wyLwONkdUd+xylwonkd+WxyWOlvd+wXLoLvUd+xYlolnVdu+wxywOLnkdu+WlWOlnKdud+WxlWolvud+wXYwlNKvd+Ylwolnkvud+ylolNkdu+wxlwOlnKVDUD+xyOlNkvdu+WYlnKVdud+ylwolnd+wxlwlnkVDu+wlwlnKvdud+WYoLnKvDuD+wyLwoKvd+XylwolNvdUd+WYLWnvdud+WxlOlNkvud+wxlwolnvud+WNvDu+WxYLnKUd+wylwonku+wyoLNd+xlKUd+WlWlNkvd+wxyokvdud+wxylolNkVd+wolnkdu+wxylwOnkVdu+wLNKvDu+xYLonkDuD+ylwOlnKv+WxylnKVuD+XyOlNKvDuD+wXwOlnkvdu+WXWolkDu+wxYlwoNkVdUd+wXLnd+xylwnKvdud+XYlwoNvdu+wxYlwolvd+WXYLWnkvd+WxyoLNKDU+Xolnkvd+xYwOLkD+wXwolkvd+wXylOlndud+WnVd+wYwolNVdud+xYlolnkv+wYlwonVDUD+wXyLkVUD+wxYlwlnKud+wylwolnkvDu+Wxylnkdu+wylwnkVdud+YWolnKvdUd+XYLwnKVdud+wxlwonvDuD+wxYlolnvd+wxYwoLnkdUd+xwOlnKdud+wxlwnkvdu+XLwLNkvDu"
    #order = "lnkvdwouxy"

    #expression = "ABCDEFGHIJKLMNOPQRS"
    #order = "abcdefghijklmnopqrs"

    #expression = "HADu+tfDs+lCDw+zpqn+xSNy+AyDj+wCXr+lvYc+Zvxq+pKSl+jkAf+XAqc+vlWu+raZH+NLtc+ZpnL+nzFh+lkjh+Vrjt+qfpd"
    #order = "nvwlxaupjrdfhqzyktsc"

    #expression = "ZfyIx+bqIKq+irFbs+Kzibr+KQAFR+bAqhc+Ilzsz+xfbXK+XhlYK+rFhZb+KQzyA+lAAyl+zCSxi+Kyqzh"
    #order = "zfyixbqkrsahcl"

    #expression = "aC+abc+Ab+Bc"
    #order = "abc"

    expression = "PEthGeelNIdtnD+otlHUiHloMpihx+EbNluACDGwBdNn+hXjddDmMWntWbH+UaaDnJhndEXGFc+XjEJrIMiCLWNam+IDRLxwdRwdOPpx+LEDWjcffaHgNpL+LNNotlwgxbowxh+mThwXXlejnwdim+MFrfewoWACHfNJ+bbGmNDmmwubIiE+lcrjjlxhUaEuhR+mDJmiemwJtnOXo+RHcNjUeDpIpXoT+EWRcciXwxThRXX+aOCoNMxxTlAiPt+IdopemdWwhwnoG+BoLepfjXjLlggP+rRepejxuLuJUHF+FJrtutmUMrouwm+pgrgRDTpuFjpDe+wWWhbnfWFejeec+lgfCjibjdPIJRL+OLiOJiOLcWdcTw+RxAwbuMbDiBoFR+plueXIHjXfxAhD+MgdrHtxRfEiGPu+ofxUgUWuGRnAwF"
    order = "pethglnidoumxbacwjfr"

    from time import time
    start = time()
    print("BDD is: " + test_bdd(expression, order, verbose_all=False))
    end = time() - start
    print("BDD time: " + str(end))

    #generate_and_test_diagrams(2)
    pass



test()
#main()
