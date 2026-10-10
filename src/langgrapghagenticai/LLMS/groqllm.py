import os
import streamlit as st 
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input
    
    def get_llm_models(self):
        try:
            groq_api_key = self.user_controls_input.get("groq_api_key") or os.environ.get("GROQ_API_KEY", "")
            selected_groq_model = self.user_controls_input.get("selected_groq_model") or self.user_controls_input.get("selected_model")
            
            if not groq_api_key:
                st.error("Please enter Groq API Key")
                return None
            
            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)
            return llm
        except Exception as e:
            st.error(f"Error: {e}")
            return None

