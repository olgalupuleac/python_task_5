from yat.model import *
from yat.printer import *


class ConstantFolder:

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return number

    def visit_reference(self, reference):
        return reference

    def visit_bin_op(self, bin_op):
        folded_lhs = bin_op.lhs.accept(self)
        folded_rhs = bin_op.rhs.accept(self)
        if (isinstance(folded_lhs, Number) and
                isinstance(folded_rhs, Number)):
            return BinaryOperation(folded_lhs,
                                   bin_op.op,
                                   folded_rhs).evaluate(Scope())
        if bin_op.op == '*':
            if (isinstance(folded_lhs, Number) and
                isinstance(folded_rhs, Reference) and
                    folded_lhs.value == 0):
                return Number(0)
            if (isinstance(folded_rhs, Number) and
                isinstance(folded_lhs, Reference) and
                    folded_rhs.value == 0):
                return Number(0)
        if (isinstance(folded_lhs, Reference) and
            isinstance(folded_rhs, Reference) and
                bin_op.op == '-'):
            if folded_lhs.name == folded_rhs.name:
                return Number(0)
        return BinaryOperation(folded_lhs,
                               bin_op.op,
                               folded_rhs)

    def visit_un_op(self, un_op):
        folded_un_op = UnaryOperation(un_op.op, un_op.expr.accept(self))
        if isinstance(folded_un_op.expr, Number):
            return folded_un_op.evaluate(Scope())
        return folded_un_op

    def fold_list(self, lst):
        folded_lst = []
        if lst:
            for op in lst:
                folded_lst.append(op.accept(self))
        return folded_lst

    def visit_conditional(self, conditional):
        return Conditional(conditional.condition.accept(self),
                           self.fold_list(conditional.if_true),
                           self.fold_list(conditional.if_false))

    def visit_print(self, write):
        return Print(write.expr.accept(self))

    def visit_read(self, read):
        return read

    def visit_func(self, func):
        return Function(func.args, self.fold_list(func.body))

    def visit_func_def(self, func_def):
        return FunctionDefinition(func_def.name,
                                  Function(func_def.function.args,
                                           self.fold_list(
                                               func_def.function.body)))

    def visit_func_call(self, func_call):
        return FunctionCall(func_call.fun_expr.accept(self),
                            self.fold_list(func_call.args))


if __name__ == '__main__':
    folder = ConstantFolder()
    printer = PrettyPrinter()

    printer.visit(folder.visit(Number(9)))

    function = Function(['x', 'y', 'z'], [Print(Reference('x')),
                                          UnaryOperation('-', BinaryOperation(
                                              Number(2),
                                              '+',
                                              Reference('x'))),
                                          BinaryOperation(Reference('y'),
                                                          '-',
                                                          Reference('z'))])
    definition = FunctionDefinition('foo', function)
    conditional = Conditional(Number(1), [definition], [Print(Number(5))])
    printer.visit(folder.visit(conditional))

    printer.visit(folder.visit(Conditional(BinaryOperation(
                                              Number(2),
                                              '+',
                                              BinaryOperation(
                                                           Reference('n'),
                                                           '-',
                                                           Reference('n'))
                                             ), [Print(BinaryOperation(
                                                           Reference('n'),
                                                           '-',
                                                           Reference('n')))],
                                                [Print(BinaryOperation(
                                                           Reference('m'),
                                                           '*',
                                                           Number(0)))])))
