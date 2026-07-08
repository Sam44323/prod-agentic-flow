from app.graph.router import route


def test_math():
    state = {"user_input": "10+5"}

    assert route(state) == "calculator"


def test_weather():
    state = {"user_input": "weather in london"}

    assert route(state) == "weather"


def test_llm():
    state = {"user_input": "Explain AI"}

    assert route(state) == "llm"
