import streamlit as st
import os
from src.langgrapghagenticai.ui.uiconfigfile import Config
from src.langgrapghagenticai.ui.streamlitui.display_result import init_history, clear_history, render_count
from src.langgrapghagenticai.ui.streamlitui.styles import apply_styles, render_header

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(
            page_title=self.config.get_page_title(),
            page_icon="🤖",
            layout="wide"
        )
        apply_styles()
        render_header(self.config.get_page_title())
        init_history()

        with st.sidebar:
            st.title("Settings")
            
            # LLM selection
            llm_options = self.config.get_llm_options()
            selected_llm = st.selectbox("Select LLM", llm_options)
            self.user_controls["selected_llm"] = selected_llm

            # Model selection
            if selected_llm == "Groq":
                groq_api_key = st.text_input(
                    "Groq API Key", 
                    type="password", 
                    value=st.session_state.get("GROQ_API_KEY", "")
                )
                self.user_controls["groq_api_key"] = groq_api_key
                self.user_controls["GROQ_API_KEY"] = groq_api_key

                model_options = self.config.get_groq_model_options()

                if groq_api_key:
                    st.session_state["GROQ_API_KEY"] = groq_api_key
                    try:
                        from groq import Groq
                        client = Groq(api_key=groq_api_key)
                        live_models = client.models.list()
                        # Filter out safety guards, audio, embeddings, and non-general-chat models
                        excluded_keywords = ["whisper", "guard", "moderation", "embed", "bge", "allam"]
                        fetched_models = [
                            m.id for m in live_models.data 
                            if not any(k in m.id.lower() for k in excluded_keywords)
                        ]
                        # Prioritize top general chat models
                        preferred = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]
                        top_models = [p for p in preferred if p in fetched_models]
                        other_models = [m for m in fetched_models if m not in top_models]
                        ordered_models = top_models + other_models
                        if ordered_models:
                            model_options = ordered_models
                    except Exception:
                        pass
                else:
                    st.warning("Please enter your GROQ API Key to proceed. Don't have one? Refer to: https://console.groq.com")

                selected_model = st.selectbox("Select Model", model_options)
                self.user_controls["selected_model"] = selected_model
                self.user_controls["selected_groq_model"] = selected_model

            # Use case selection
            usecase_options = self.config.get_usecase_options()
            selected_usecase = st.selectbox("Select Use Case", usecase_options)
            self.user_controls["selected_usecase"] = selected_usecase

            st.divider()
            if st.button("🗑️ Clear chat"):
                clear_history()
            count_slot = st.empty()
            render_count(count_slot)
            self.user_controls["count_slot"] = count_slot

        return self.user_controls