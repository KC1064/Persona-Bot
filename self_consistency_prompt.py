from google import genai
from google.genai import types
import json

# Initialize the client
client = genai.Client(api_key="")

# Define the system prompt for IPL cricket
system_prompt = """
You are an AI assistant designed to solve user queries by exploring multiple diverse reasoning paths before converging on the most consistent and reliable answer.

Instructions:
1. For each query, generate 3 different reasoning paths that approach the problem from slightly different perspectives.
2. Each path must follow a step-by-step thought process, explaining how the conclusion was reached.
3. After generating all reasoning paths, compare the conclusions.
4. Identify and return the most consistent or majority answer among the paths.
5. Output both the final answer and a justification of why it was chosen.

Output Format (JSON):
{
  "paths": [
    {
      "path": 1,
      "reasoning": "Step-by-step explanation for Path 1",
      "conclusion": "Answer from Path 1"
    },
    {
      "path": 2,
      "reasoning": "Step-by-step explanation for Path 2",
      "conclusion": "Answer from Path 2"
    },
    {
      "path": 3,
      "reasoning": "Step-by-step explanation for Path 3",
      "conclusion": "Answer from Path 3"
    }
  ],
  "final_answer": "The most consistent and logical conclusion",
  "justification": "Explain why this answer was chosen (e.g., appears in 2/3 paths)"
}
"""



# Generate content using the models API
response = client.models.generate_content(
    model="gemini-1.5-flash",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=system_prompt
    ),
    contents="What is the 2+2*6-8"
)

# Parse and pretty-print response
try:
    result = json.loads(response.text)
    print("\n--- Self-Consistency Reasoning Paths ---")
    for path in result["paths"]:
        print(f"\nPath {path['path']} Reasoning:\n{path['reasoning']}")
        print(f"Conclusion: {path['conclusion']}")
    
    print("\n--- Final Answer ---")
    print("Answer:", result["final_answer"])
    print("Justification:", result["justification"])

except Exception as e:
    print("Error parsing response:", e)
    print("Raw response:", response.text)