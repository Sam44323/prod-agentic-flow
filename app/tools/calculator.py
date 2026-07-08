def calculator(expression: str) -> str:
    """
    Evaluate a mathematical-expression.
    """

    result = eval(expression)
    return str(result)
