from yat.model import *


class PrettyPrinter:

    def __init__(self):
        self.tab = 0

    def visit(self, tree):
        tree.accepted(self)
        print(';')

    def visit_number(self, number):
        print(number.value, end='')

    def visit_reference(self, reference):
        print(reference.name, end='')

    def visit_binary_operation(self, bin_op):
        print('(', end='')
        bin_op.lhs.accepted(self)
        print(' ' + bin_op.op, end=' ')
        bin_op.rhs.accepted(self)
        print(')', end='')

    def visit_unary_operation(self, un_op):
        print('(', end='')
        print(un_op.op, end=' ')
        un_op.expr.accepted(self)
        print(')', end='')

    def print_list(self, lst):
        if lst:
            self.tab += 4
            for operation in lst:
                print(' ' * self.tab, end='')
                self.visit(operation)
            self.tab -= 4

    def visit_conditional(self, conditional):
        print('if' + '(', end='')
        conditional.condition.accepted(self)
        print(')' + '{')
        self.print_list(conditional.if_true)
        print('}' + 'else' + '{')
        self.print_list(conditional.if_false)
        print('}', end='')

    def visit_print(self, write):
        print('print', end='(')
        write.expr.accepted(self)
        print(')', end='')

    def visit_read(self, read):
        print('read(' + read.name, end=')')

    def print_args(self, lst):
        print('(', end='')
        if lst:
            for arg in lst[:-1]:
                arg.accepted(self)
            print(', ', end='')
            lst[-1].accepted(self)
            print(')', end='')

    def visit_func_def(self, func_def):
        print(func_def.name, end='')
        print('(' + ', '.join(func_def.function.args), end=')')
        print('{')
        self.print_list(func_def.function.body)
        print('}', end='')

    def visit_func_call(self, func_call):
        func_call.fun_expr.accepted(self)
        self.print_args(func_call.args)


if __name__ == '__main__':
    printer = PrettyPrinter()
    printer.visit(FunctionCall(FunctionDefinition(
        'foo',
        Function([], [Read('n'),
                      Print(BinaryOperation(Reference('n'),
                                            '/',
                                            Reference('k')
                                            ))])), [], ))

    printer.visit(Conditional(BinaryOperation(
                       Number(2),
                       '<=',
                       Reference('s')
                    ), [Print(Number(1))],
                       [Print(Number(0))]))

    number = Number(42)
    conditional = Conditional(number, [], [])
    printer.visit(conditional)

    function = Function([], [])
    definition = FunctionDefinition('foo', function)
    printer.visit(definition)

    number = Number(42)
    write = Print(number)
    printer.visit(write)

    read = Read('x')
    printer.visit(read)

    ten = Number(10)
    printer = PrettyPrinter()
    printer.visit(ten)

    reference = Reference('x')
    printer = PrettyPrinter()
    printer.visit(reference)

    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer.visit(mul)

    reference = Reference('foo')
    call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
    printer.visit(call)

    function = Function(['x', 'y'], [])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)
