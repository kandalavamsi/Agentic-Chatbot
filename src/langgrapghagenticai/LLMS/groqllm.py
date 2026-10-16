import streamlit as st
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_models(self):
        try:
            # The key must come from the user's own sidebar input.
            # There is intentionally NO fallback to os.environ / server secrets,
            # so a public deployment can never spend the owner's Groq quota.
            groq_api_key = (self.user_controls_input.get("groq_api_key") or "").strip()
            selected_groq_model = (
                self.user_controls_input.get("selected_groq_model")
                or self.user_controls_input.get("selected_model")
            )

            if not groq_api_key:
                st.error("Please enter your Groq API Key in the sidebar.")
                return None

            return ChatGroq(api_key=groq_api_key, model=selected_groq_model)
        except Exception as e:
            st.error(f"Error: {e}")
            return None