from services.llm_client import (
    generate_json_response,
    generate_text_response,
)

print("Testing text generation...\n")

text = generate_text_response(
    "Reply with exactly: ContractMind AI is ready."
)

print(text)

print("\nTesting JSON generation...\n")

response = generate_json_response(
    """
Return ONLY JSON.

{
    "status": "working",
    "provider": "groq"
}
"""
)

print(response)