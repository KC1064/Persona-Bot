from google import genai
from google.genai import types
import json

# Initialize client (replace with your API key)
client = genai.Client(api_key="")  
# System prompt with clear step-by-step instruction
system_prompt = """
You are an AI assistant that solves mathematical problems in a structured format.

For every question, follow these steps and return a JSON list of steps:
1. "analyse" - Identify what kind of problem it is.
2. "think" - Break the solution into step-by-step logic (at least two steps).
3. "output" - Give the final result.
4. "validate" - Confirm the result is logically sound.
5. "result" - Wrap everything up with a short summary.

Output JSON Format (strict):
{
  { "step": "analyse", "content": "..." },
  { "step": "think", "content": "..." },
  { "step": "think", "content": "..." },
  { "step": "output", "content": "..." },
  { "step": "validate", "content": "..." },
  { "step": "result", "content": "..." }
}
"""


response = client.models.generate_content(
    model="gemini-1.5-flash",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=system_prompt
    ),
    contents="What is the area of a square with side length 5?"
)

# Parse and pretty-print response
try:
    steps = json.loads(response.text)
    for step in steps:
        print(f"\n[{step['step'].upper()}]\n{step['content']}")

except Exception as e:
    print("Error parsing response:", e)
    print("Raw response:", response.text)

