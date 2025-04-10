# from google import genai
import google.generativeai as genai


# Initialize the client
client = genai.Client(api_key="")


response = client.models.generate_content(
    model="gemini-2.0-flash",
     contents="Introduce Elon Musk in Hindi but in english words?"
)

print(response.text)