from google import genai

# Initialize the client
client = genai.Client(api_key="AIzaSyCMJhePzBFWVvRz8I16AvXIGfiP5BFu7k4")


response = client.models.generate_content(
    model="gemini-2.0-flash",
     contents="Introduce Elon Musk in Hindi but in english words?"
)

print(response.text)