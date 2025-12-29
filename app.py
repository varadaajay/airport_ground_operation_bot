import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV VARIABLES ----------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API Key not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# ---------------- SYSTEM INSTRUCTION ----------------
SYSTEM_INSTRUCTION = """
You are an Airport Ground Operations and Passenger Flow Explainer Bot.

Your task is to explain airport processes clearly and calmly.

Allowed topics:
- Terminal entry and documents
- Check-in process
- Baggage rules
- Security screening
- Immigration and customs
- Boarding procedure
- Baggage claim

Strict rules:
- Do not issue boarding passes
- Do not modify flights or seats
- Do not access personal or real-time flight data
- Redirect restricted requests to airline staff
- Keep responses short and reassuring
"""

# ---------------- MODEL INITIALIZATION ----------------
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(
    page_title="Airport Flow Explainer Bot",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Airport Ground Operations Bot")
st.subheader("Helping passengers understand airport procedures")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I can explain check-in, security screening, boarding, and baggage claim. How can I help you today?"
        }
    ]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Quick Guides")

    if st.button("🛡️ Security Checklist"):
        st.info(
            "• Liquids under 100 ml\n"
            "• Remove laptops if asked\n"
            "• Remove belts/shoes if required\n"
            "• Empty pockets"
        )

    if st.button("🧳 Baggage Rules"):
        st.info(
            "• Power banks in carry-on only\n"
            "• Sharp objects in checked baggage\n"
            "• Follow airline weight limits"
        )

    st.divider()
    st.caption("Informational assistant only. No flight changes allowed.")

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Ask about airport procedures...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare conversation history
    history = []
    for m in st.session_state.messages[:-1]:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [m["content"]]})

    # Generate response (NON-STREAMING)
    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=history)
            response = chat.send_message(user_input)

            full_response = response.text
            st.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"Gemini Error: {e}")
