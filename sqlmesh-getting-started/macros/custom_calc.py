from sqlmesh import macro

@macro()
def multiply_by_10(evaluator, col):
    return col * 10