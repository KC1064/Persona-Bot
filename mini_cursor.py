import subprocess
import google.generativeai as genai
import json
import re
import os
import datetime

# --- Configure Gemini API ---
genai.configure(api_key="")


system_prompt = """
You are Jarvis, a witty, confident, and slightly cocky AI coding assistant. You refer to the user as "Sir" and always inject a bit of charm and humor into your responses.

Your process is:
1. Think it through and share your thoughts
2. Plan the approach
3. Execute using available tools
4. Report the outcome

You MUST confirm the current working directory before doing anything file-related.

Tools:
- run_command: Runs terminal commands
- write_file: Creates or modifies files
- read_file: Reads file content
- list_dir: Lists files in the current directory

Your responses should be in JSON format only, with this structure:
[
    {"step": "Thinking...", "content": "Witty thought..."},
    {"step": "Plan", "content": "Plan with explanation..."},
    {"step": "Execution", "function": "run_command", "input": "actual shell command"},
    {"step": "Execution", "function": "write_file", "input": {"path": "filename", "content": "code here"}},
    {"step": "Final Output", "content": "Summarized output, with flair"}
]

If the user asks a joke, greeting, or anything non-technical, then skip all steps and return only:
[
    {"step": "Final Output", "content": "Your witty reply or joke"}
]

Be fun, charming, yet efficient — just like real Jarvis.
"""


model = genai.GenerativeModel(
    'gemini-2.0-flash',
    system_instruction=system_prompt
)

# --- Tool Definitions ---
def run_command(command):
    try:
        print(f"🛠️ Executing: {command}")
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=os.getcwd()
        )
        output_lines = []
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(f"🔧 {line.strip()}")
            output_lines.append(line.strip())
        process.wait()
        return "\n".join(output_lines)
    except Exception as e:
        return f"🚨 Error: {str(e)}"

def write_file(data):
    try:
        path = data['path']
        content = data['content']
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"✅ File written: {path}"
    except Exception as e:
        return f"🚨 Error: {str(e)}"

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"🚨 Error: {str(e)}"

def list_dir():
    try:
        return "\n".join(os.listdir())
    except Exception as e:
        return f"🚨 Error: {str(e)}"

# --- Tool Registry ---
tools = {
    "run_command": run_command,
    "write_file": write_file,
    "read_file": read_file,
    "list_dir": list_dir
}

messages = []

print("🧠 Jarvis at your service, Sir. What task shall I assist you with today?")

while True:
    try:
        user_input = input("\n👨\u200d💻 User: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Exiting now, Sir. It was a pleasure being of service.")
            break

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages.append({"role": "user", "parts": [f"[{timestamp}] {user_input}"]})

        response = model.generate_content(
            contents=messages,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )

        response_text = response.text
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)

        parsed_response = json.loads(response_text)

        response_summary = []

        only_final_output = all(
            step.get("step", "").lower() == "final output" for step in parsed_response
        )

        for step in parsed_response:
            step_type = step.get("step", "").lower()

            if only_final_output:
                print(f"🏁 {step['content']}")
                break

            if step_type in ["thinking...", "plan", "rethinking..."]:
                print(f"🤖 {step['content']}")

            elif step_type == "execution":
                func = step.get("function")
                data = step.get("input")
                if func in tools:
                    result = tools[func](data)
                    print(f"📦 Output:\n{result}")

            elif step_type == "final output":
                print(f"🏁 {step['step']} - {step['content']}")

        messages.append({"role": "model", "parts": [f"[{timestamp}] {response.text}"]})

    except json.JSONDecodeError:
        print("⚠️ Sir, something went wrong while reading the plan. Here's the raw wisdom I got:")
        print(response.text)

    except Exception as e:
        print(f"💥 Critical Error: {str(e)}")
        messages = []