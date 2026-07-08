from app.graph.graph import app


def test_graph():
    state = {
        "user_input": "2+2",
        "tool_name": "",
        "tool_input": "",
        "tool_output": "",
        "error": "",
        "final_answer": "",
    }

    result = app.invoke(state)

    assert result["final_answer"] == "4"
