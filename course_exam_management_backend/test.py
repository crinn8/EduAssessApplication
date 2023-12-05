import ast

code = """def cal_sum(a):
    return a+10

if __name__ == '__main__':
    a = 10
    b=20
    c=a+b
    """

tree = ast.parse(code)

# Find the last expression or assignment statement in the if block
last_expr = None
for stmt in tree.body:
    if isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Compare) and len(stmt.test.ops) == 1:
        if isinstance(stmt.test.ops[0], ast.Eq) and isinstance(stmt.test.left, ast.Name) and stmt.test.left.id == "__name__":
            if isinstance(stmt.test.comparators[0], ast.Constant) and stmt.test.comparators[0].value == "__main__":
                last_stmt = None
                for expr in stmt.body:
                    if isinstance(expr, (ast.Expr, ast.Assign)):
                        last_stmt = expr

                if isinstance(last_stmt, ast.Assign):
                    # If the last statement is an assignment, create a new expression statement to wrap it in a print call
                    print_call = ast.Call(func=ast.Name(id="print", ctx=ast.Load()),
                                          args=[last_stmt.targets[0], ast.Constant(value="="), last_stmt.value],
                                          keywords=[])

                    print_expr = ast.Expr(value=print_call)
                    stmt_idx = tree.body.index(stmt)
                    tree.body[stmt_idx].body[-1] = print_expr
                elif isinstance(last_stmt, ast.Expr):
                    # If the last statement is an expression, wrap it in a print call
                    print_call = ast.Call(func=ast.Name(id="print", ctx=ast.Load()),
                                          args=[last_stmt.value],
                                          keywords=[])

                    print_expr = ast.Expr(value=print_call)
                    stmt_idx = tree.body.index(stmt)
                    tree.body[stmt_idx].body[-1] = print_expr

                # Generate the new code
                new_code = ast.unparse(tree)
                print(new_code)
                break
else:
    print("No expression or assignment statement found")
