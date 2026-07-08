from app.graph.nodes import calculator_node


def test_calculator_node():
    state = {
        "user_input": "4*5",
        "tool_name": "",
        "tool_input": "",
        "tool_output": "",
        "error": "",
        "final_answer": "",
    }

    result = calculator_node(state)

    assert result["final_answer"] == "20"
    assert result["tool_name"] == "calculator"
