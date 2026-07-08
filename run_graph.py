# temp-file for testing
from app.graph.graph import app


result = app.invoke({"user_input": "2 + 2", "final_answer": ""})
result = app.invoke({"user_input": "what is lang-graph?", "final_answer": ""})

print(result)
