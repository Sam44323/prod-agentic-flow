def calculator(expression: str) -> str:
    """
    Evaluate a mathematical-expression.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Calculation Error: {e}"
