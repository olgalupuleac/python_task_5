from yat.model import *
from printer import *


class ConstantFolder:

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return number

    def visit_reference(self, reference):
        return reference

    def visit_bin_op(self, bin_op):
        if isinstance(bin_op.lhs, Number) and isinstance(bin_op.rhs,
                                                         Number):
            scope = Scope()
            return bin_op.evaluate(scope)
        if bin_op.op == '*':
            if isinstance(bin_op.lhs, Number) and bin_op.lhs.value == 0:
                return Number(0)
            if isinstance(bin_op.rhs, Number) and bin_op.rhs.value == 0:
                return Number(0)
        if isinstance(bin_op.lhs, Reference) and isinstance(bin_op.rhs,
                                                            Reference):
            if bin_op.op == '-' and bin_op.lhs.name == bin_op.rhs.name:
                return Number(0)
        return bin_op

    def visit_un_op(self, un_op):
        if isinstance(un_op.expr, Number):
            scope = Scope()
            return un_op.evaluate(scope)
        return un_op

    def accept_list(self, lst):
        folded_lst = []
        if lst:
            for op in lst:
                folded_lst.append(op.accept(self))
        return folded_lst

    def visit_conditional(self, conditional):
        return Conditional(conditional.condition.accept(self),
                           self.accept_list(conditional.if_true),
                           self.accept_list(conditional.if_false))

    def visit_print(self, write):
        return Print(write.expr.accept(self))

    def visit_read(self, read):
        return read

    def visit_func(self, func):
        return Function(func.args, self.accept_list(func.body))

    def visit_func_def(self, func_def):
        return FunctionDefinition(func_def.name,
                                  Function(func_def.function.args,
                                           self.accept_list(
                                               func_def.function.body)))

    def visit_func_call(self, func_call):
        return FunctionCall(func_call.fun_expr.accept(self),
                            self.accept_list(func_call.args))


if __name__ == '__main__':
    folder = ConstantFolder()
    printer = PrettyPrinter()

    printer.visit(folder.visit(Number(9)))

    function = Function(['x', 'y', 'z'], [Print(Reference('x')),
                                          UnaryOperation('-', Number(10)),
                                          BinaryOperation(Reference('y'),
                                                          '-',
                                                          Reference('z'))])
    definition = FunctionDefinition('foo', function)
    conditional = Conditional(Number(1), [definition], [Print(Number(5))])
    printer.visit(conditional)

    printer.visit(folder.visit(Conditional(BinaryOperation(
                                              Number(2),
                                              '<=',
                                              Number(5)
                                             ), [Print(BinaryOperation(
                                                           Reference('n'),
                                                           '-',
                                                           Reference('n')))],
                                                [Print(BinaryOperation(
                                                           Reference('m'),
                                                           '*',
                                                           Number(0)))])))
