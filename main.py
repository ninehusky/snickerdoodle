import argparse
from pyverilog.vparser.parser import parse
from pyverilog.vparser.ast import Node, Plus
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator


# Define a visitor to traverse the AST and apply commutativity rule
class CommutativityRewriter(Node):
    def visit(self, node):
        if isinstance(node, Plus):
            (l, r) = node.children()
            node.left = r
            node.right = l

        for child in node.children():
            self.visit(child)
        return node


# Define a function to apply the commutativity rule
def apply_commutativity(ast):
    return CommutativityRewriter().visit(ast)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Apply semantics-preserving rewrite rules to Verilog code"
    )
    parser.add_argument("filename")

    ast, _ = parse([parser.parse_args().filename])

    modified_ast = CommutativityRewriter().visit(ast)
    result = ASTCodeGenerator().visit(modified_ast)
    print(result)
