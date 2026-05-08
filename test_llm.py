from app.llm import llm

response = llm.generate(
    "Introduce yourself briefly."
)

print(response)