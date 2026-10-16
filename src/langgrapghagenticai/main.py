import streamlit as st
from src.langgrapghagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgrapghagenticai.LLMS.groqllm import GroqLLM
from src.langgrapghagenticai.graph.graph_builder import GraphBuilder
from src.langgrapghagenticai.ui.streamlitui.display_result import DisplayResultStreamlit, render_history, HISTORY_KEY
from src.langgrapghagenticai.ui.streamlitui.styles import render_welcome, PENDING_KEY

def load_langgraph_agentic_app():
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    render_history()
    if not st.session_state[HISTORY_KEY] and PENDING_KEY not in st.session_state:
        render_welcome()
    # A typed message wins; otherwise use a clicked suggestion button.
    user_message=st.chat_input("Message the agent...") or st.session_state.pop(PENDING_KEY, None)

    if user_message:
        try:
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_models()

            if not model:
                return  # GroqLLM has already shown the specific error

            usecase=user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No use case selected.")
                return
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message,user_input.get("count_slot")).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Failed to setup graph - {e}")
                return
        except Exception as e:
            st.error(f"Error: {e}")
            return