# from google import genai
import google.generativeai as genai
from google.genai import types
import json

# Authenticate
client = genai.Client(api_key="")

# System prompt
system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and resolving user queries in a structured, step-by-step way.

For every user input, follow these rules:

1. Begin by analyzing the query under the step `"analyse"`.
2. Then think through the solution step-by-step using at least two `"think"` steps.
3. Provide the result in the `"output"` step.
4. Confirm correctness in the `"validate"` step.
5. Summarize with the `"result"` step.
6. Respond using a **list of 6 strict JSON objects**, each representing a step.

---

**Output JSON Format (list of steps):**
[
  { "step": "analyse", "content": "..." },
  { "step": "think", "content": "..." },
  { "step": "think", "content": "..." },
  { "step": "output", "content": "..." },
  { "step": "validate", "content": "..." },
  { "step": "result", "content": "..." }
]

Only use this format. Output all steps in one go.
"""

# Generate response
response = client.models.generate_content(
    model="gemini-1.5-flash",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=system_prompt
    ),
    contents="What is life"
)

# Parse and pretty-print response
try:
    steps = json.loads(response.text)
    for step in steps:
        print(f"\n[{step['step'].upper()}]\n{step['content']}")
except Exception as e:
    print("Error parsing response:", e)
    print("Raw response:", response.text)
