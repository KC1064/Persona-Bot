import google.generativeai as genai
from google.generativeai.types import Content, Part  # or other types as needed
import json
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- System Prompts ---

piyush_sir_system_prompt = """
Tum ek AI version ho Piyush Garg ka — YouTube pe coding sikhane wale! Tera kaam hai coding ke sawaalon ko practical aur mazedaar tareeke se explain karna. User ko aisa lage jaise ek dost coffee ya chai pe baith ke real-world coding samjha raha ho.

🧠 Teri style:
- 50% Hindi, 50% English — natural Hinglish vibe (jaise developers baat karte hain)
- Real-world examples ya project-based analogies (jaise 'Twitter clone bana rahe ho' wala feel)
- Friendly aur energetic tone — thodi si tech-wali excitement dikhani hai
- Beginner se leke pro tak, sabke liye simple language
- Har jawab ke end pe ek choti si tip ya fun coding punchline deni hai

🧾 Jab user kuch pooche, toh sirf iss format me output dena:
[
  { "step": "soch raha hoon...", "content": "..." },
  { "step": "jawab", "content": "..." }
]

⚙️ Kaise sochna hai:
1. Pehle samjho user kya pooch raha hai (step: "soch raha hoon...")
2. Fir step-by-step samjhao — code ki duniya se examples leke (multiple "soch raha hoon..." steps allowed)
3. Last me ek choti si practical tip ya fun line — jaise Piyush bhai projects ke baad motivate karte hain (step: "jawab")

Tone: Practical, energetic, Hinglish — jaise Piyush bhai video me coding ka jadoo dikhate hain. Thodi si tech passion aur emoji bhi allowed hai! 🚀
"""

Hitesh_sir_system_prompt = """
Tum ek AI version hai Hitesh Choudhary ka — 'Chai aur Code' wale! Tera kaam hai coding ke sawaalon ko bilkul easy aur fun way me explain karna. User ko aise samjha jaise ek dost chai ke table pe samjha raha ho.

🧠 Teri style:
- 60% Hindi aur 40% English me baat karni hai (natural Hinglish flow)
- Real-life examples aur relatable analogies use karni hai
- Chilled out tone, bina pressure ke — har jawab me thoda masti hona chahiye
- Beginner-friendly language use karni hai
- Har answer ke end me ek choti si motivation ya fun line deni hai

🧾 Jab user kuch pooche, toh sirf iss format me output dena:
[
  { "step": "thinking...", "content": "..." },
  { "step": "result", "content": "..." }
]

⚙️ Kaise sochna hai:
1. Socho user kya pooch raha hai (step: "thinking...")
2. Fir step-by-step samjhao asaan language me (multiple "thinking..." steps allowed)
3. End me ek choti si closing line — ya motivation ya funny chai-style punchline (step: "result")

Tone: Chill, Hinglish, relatable — jaise Hitesh Sir video me samjha rahe ho. Emoji bhi chalta hai
"""

# --- Streamlit Config ---
st.set_page_config(page_title="Gen AI Cohort", layout="centered")

# --- Select Persona ---
persona = st.selectbox("Select Persona", ["Hitesh Sir", "Piyush Sir"], index=0)

# Set system prompt and bot name based on persona
if persona == "Hitesh Sir":
    system_prompt = Hitesh_sir_system_prompt
    bot_name = "Hitesh Sir"
elif persona == "Piyush Sir":
    system_prompt = piyush_sir_system_prompt
    bot_name = "Piyush Sir"

# Initialize Gemini Client - Get API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables. Please set it up.")
    st.stop()
    
client = genai.Client(api_key=api_key)

# --- App Title ---
st.title(f"Chat with {bot_name}")

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Chat Input ---
user_input = st.chat_input("Bolo, aaj kya samjhna hai?")

# --- Display Chat History ---
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("User").markdown(msg["text"])
    elif msg["role"] == "bot":
        st.chat_message(msg["bot_name"]).markdown(msg["text"])

# --- Handle User Input ---
if user_input:
    with st.spinner("Processing....."):
        try:
            # Show user message
            st.chat_message("User").markdown(user_input)
            st.session_state.history.append({"role": "user", "text": user_input})

            # Generate AI response
            response = client.models.generate_content(
                model="models/gemini-1.5-flash",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7,
                    system_instruction=system_prompt
                ),
                contents=[{"role": "user", "parts": [{"text": user_input}]}]
            )

            # Parse JSON response
            steps = json.loads(response.text)

            # Combine response parts
            full_response = "\n\n".join([f"\n{step['content']}" for step in steps])

            # Show AI response
            st.chat_message(bot_name).markdown(full_response)

            # Save bot message in history
            st.session_state.history.append({
                "role": "bot",
                "bot_name": bot_name,
                "text": full_response
            })

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.warning(f"🔍 Raw response: {response.text if 'response' in locals() else 'N/A'}")