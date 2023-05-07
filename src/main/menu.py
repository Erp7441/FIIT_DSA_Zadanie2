from src.tests.checker import generate_and_run_tests, run_tests
from src.tests.generator import generate_bdd_diagrams
from src.bdd.BDD import BDD
from src.utils.constants import get_c_diagram_count, get_c_variable_count, get_c_node_count


def exit_menu():
    exit_confirm = input("Are you sure you want to exit? (y/n): ")
    if exit_confirm.lower() == "y":
        from sys import exit as exit_program
        exit_program(0)


class Menu:
    def __init__(self):
        self.options = [
            ("Enter expression and order", self.input_exp_and_ord),
            ("Print BDD's", self.print_bdds),
            ("Create BDD", self.create_bdd),
            ("Create BDD with best order", self.create_with_best_order),
            ("Create specific cases", self.create_specific_cases),
            ("Run tests", self.run_tests),
            ("Generate BDD's", self.generate_bdds),
            ("Generate BDD's and run tests", self.generate_bdds_and_test),
            ("Clear BDD's list", self.clear_bdds),
            ("Clear BDD expression", self.clear_expression),
            ("Clear BDD order", self.clear_order),
            ("Exit menu", exit_menu)
        ]
        self.expression = None
        self.order = None
        self.bdds = []

    def start(self):
        while True:
            print("\n----------------------------------")
            print("Current expression: " + str(self.expression))
            print("Current order: " + str(self.order))
            print("----------------------------------")

            for index, option in enumerate(self.options):
                print(str(index+1) + ": " + option[0])

            print("----------------------------------")
            self.get_user_selection()

    def create_bdd(self):
        if self.expression is None or self.order is None:
            print("No expression or order specified")
            return

        bdd = BDD().create(self.expression, self.order)
        self.bdds.append(bdd)

        print("Expression: " + self.expression)
        print("Reduced expression: " + bdd.layers[0][0].expression)
        print("Order: " + bdd.order)
        print("Node count: " + str(bdd.count))
        print("Variable count: " + str(bdd.variable_count))

    def create_with_best_order(self):
        if self.expression is None or self.order is None:
            print("No expression")
            return

        change_params = input("Do you wish to change default parameters? (y/n): ")

        bdd = None
        if change_params.lower() != "y":
            bdd = BDD().create_with_best_order(self.expression)
        else:
            try:
                best_order_combination_count = input("Enter maximum combination count (leave blank for default): ")
                best_order_combination_count = int(best_order_combination_count) if best_order_combination_count.strip() == "" else None
            except ValueError:
                print("Invalid input")
                return
            bdd = BDD().create_with_best_order(self.expression, best_order_combination_count)

        self.bdds.append(bdd)
        print("\nExpression: " + self.expression)
        print("Reduced expression: " + bdd.layers[0][0].expression)
        print("Order: " + bdd.order)
        print("Node count: " + str(bdd.count))
        print("Variable count: " + str(bdd.variable_count))

    def create_specific_cases(self):

        from src.utils.constants import get_c_test_expressions

        old_expression = self.expression
        old_order = self.order

        print("----------------------------------")
        for index, expression in enumerate(get_c_test_expressions()):
            self.expression = expression[0]
            self.order = expression[1]
            self.create_bdd()
            print("----------------------------------")

        self.expression = old_expression
        self.order = old_order

    def run_tests(self):
        if self.bdds is None or len(self.bdds) == 0:
            print("No BDD's were created")
            return

        change_params = input("Do you wish to change default parameters? (y/n): ")

        if change_params.lower() != "y":
            for bdd in self.bdds:
                run_tests(bdd.layers[0][0].expression, bdd.order)
            return

        verbose_all = input("Verbose all events? (y/n) (leave blank for default): ")
        verbose_bad = input("Verbose bad events? (y/n) (leave blank for default): ")
        verbose_good = input("Verbose good events? (y/n) (leave blank for default): ")
        slow_time = input("Enter slow time (leave blank for default): ")
        best_order_combination_count = input("Enter maximum combination count (leave blank for default): ")

        try:
            verbose_all = True if verbose_all.lower() == "y" else False
            verbose_bad = True if verbose_bad.lower() == "y" else False
            verbose_good = True if verbose_good.lower() == "y" else False
            slow_time = None if slow_time.strip() == "" else float(slow_time)
            best_order_combination_count = None if best_order_combination_count.strip() == "" else int(best_order_combination_count)
        except ValueError:
            print("Invalid input")
            return

        for bdd in self.bdds:
            run_tests(bdd.layers[0][0].expression, bdd.order, verbose_all, verbose_bad, verbose_good, slow_time, best_order_combination_count)

    def generate_bdds(self):
        diagrams = []
        diagram_count = get_c_diagram_count()
        variable_count = get_c_variable_count()
        node_count = get_c_node_count()

        change_params = input("Do you wish to change default parameters? (y/n): ")

        if change_params.lower() != "y":
            diagrams = generate_bdd_diagrams()
        else:
            diagram_count = input("Enter diagram count (leave blank for default): ")
            variable_count = input("Enter variable count (leave blank for default): ")
            node_count = input("Enter node count (leave blank for default): ")

            try:
                diagram_count = get_c_diagram_count() if diagram_count.strip() == "" else int(diagram_count)
                variable_count = get_c_variable_count() if variable_count.strip() == "" else int(variable_count)
                node_count = get_c_node_count() if node_count.strip() == "" else int(node_count)
            except ValueError:
                print("\nInvalid input!")
                return

            diagrams = generate_bdd_diagrams(diagram_count, variable_count, node_count)

        for bdd in diagrams:
            self.bdds.append(bdd)

        print("\nSuccessfully generated " + str(diagram_count) + " diagrams with " + str(variable_count) + " variables and " + str(node_count) + " nodes")

    def generate_bdds_and_test(self):
        change_params = input("Do you wish to change default parameters? (y/n): ")

        if change_params.lower() != "y":
            generate_and_run_tests()
            return

        diagram_count = input("Enter diagram count (leave blank for default): ")
        variable_count = input("Enter variable count (leave blank for default): ")
        node_count = input("Enter node count (leave blank for default): ")
        best_order_combination_count = input("Enter maximum combination count (leave blank for default): ")

        try:
            diagram_count = get_c_diagram_count() if diagram_count.strip() == "" else int(diagram_count)
            variable_count = get_c_variable_count() if variable_count.strip() == "" else int(variable_count)
            node_count = get_c_node_count() if node_count.strip() == "" else int(node_count)
            best_order_combination_count = int(best_order_combination_count) if best_order_combination_count.strip() != "" else None
        except ValueError:
            print("\nInvalid input!")
            return

        generate_and_run_tests(diagram_count, variable_count, node_count, best_order_combination_count)

    def print_bdds(self):
        if len(self.bdds) == 0:
            print("No BDD's were found!")
            return

        print_tree = False if input("Print tree of BDD's? (y/n): ").lower() != "y" else True

        print()
        for index, bdd in enumerate(self.bdds):
            if print_tree:
                print("BDD #" + str(index + 1) + " (" + bdd.layers[0][0].expression + ")")
                print(bdd)
            else:
                print("BDD #" + str(index + 1) + " (" + bdd.layers[0][0].expression + ")")
                print("----------------------------------")
            if index + 1 < len(self.bdds):
                print()

    def get_user_selection(self):
        selection = int(input("Enter selection: "))

        print("----------------------------------\n")
        if selection <= 0 or selection > len(self.options):
            print("Invalid selection!")

        self.options[selection-1][1]()

    def input_exp_and_ord(self):
        self.expression = input("Enter expression: ")
        if self.expression == "":
            self.expression = None

        self.order = input("Enter order: ").lower()
        if self.order == "":
            self.order = None

    def clear_bdds(self):
        self.bdds = []
        print("BDD's list has been cleared")

    def clear_expression(self):
        self.expression = None
        print("Expression has been cleared")

    def clear_order(self):
        self.order = None
        print("Order has been cleared")