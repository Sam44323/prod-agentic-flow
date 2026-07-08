from app.graph.graph import app

result = app.invoke({
    "user_input": "What is LangGraph?",
    "final_answer": ""
})

print(result)
