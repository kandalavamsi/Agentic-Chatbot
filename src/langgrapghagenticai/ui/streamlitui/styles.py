import html
import streamlit as st

PENDING_KEY = "pending_prompt"  # set when a suggestion button is clicked
SUBTITLE = "Stateful chat powered by LangGraph and Groq"

SUGGESTIONS = [
    ("💡", "What are AI agents?"),
    ("🕸️", "Explain LangGraph in simple terms"),
    ("🐍", "Write a Python function to reverse a string"),
]

# All colours are semi-transparent / inherited so the same CSS looks right in
# both light and dark mode.
CSS = """
<style>
/* ---------- layout ---------- */
.block-container { max-width: 980px; padding-top: 2.2rem; }
footer { visibility: hidden; }

/* ---------- header ---------- */
.app-hero { margin-bottom: 1.2rem; }
.app-hero h1 {
    font-size: 2.1rem; font-weight: 800; line-height: 1.15; margin: 0; padding: 0;
    background: linear-gradient(90deg, #6C5CE7 0%, #00B4D8 100%);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-hero p { margin: .35rem 0 0 0; opacity: .65; font-size: 1rem; }

/* ---------- chat bubbles ---------- */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 1rem 1.2rem;
    margin-bottom: .8rem;
    border: 1px solid rgba(128, 128, 128, .20);
    background: rgba(128, 128, 128, .07);
    margin-right: 6%;
}
/* user messages: accent tint, nudged to the right */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, rgba(108, 92, 231, .18), rgba(0, 180, 216, .12));
    border-color: rgba(108, 92, 231, .40);
    margin-left: 12%;
    margin-right: 0;
}
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    background: rgba(128, 128, 128, .15);
    font-size: 1.3rem;
}
/* code blocks and tables inside answers */
[data-testid="stChatMessage"] pre { border-radius: 12px; }
[data-testid="stChatMessage"] table { border-radius: 10px; overflow: hidden; }

/* ---------- chat input ---------- */
[data-testid="stChatInput"] {
    border-radius: 16px;
    border: 1px solid rgba(108, 92, 231, .35);
    box-shadow: 0 2px 14px rgba(108, 92, 231, .10);
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6C5CE7;
    box-shadow: 0 2px 18px rgba(108, 92, 231, .25);
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] { border-right: 1px solid rgba(128, 128, 128, .20); }
section[data-testid="stSidebar"] h1 { font-size: 1.5rem; font-weight: 700; }
section[data-testid="stSidebar"] .stButton > button {
    width: 100%; border-radius: 12px; font-weight: 600;
}

/* ---------- welcome card + suggestion buttons ---------- */
.welcome {
    text-align: center; padding: 2.2rem 1rem 1.2rem 1rem; margin: .5rem 0 1rem 0;
    border-radius: 20px; border: 1px dashed rgba(108, 92, 231, .40);
    background: linear-gradient(135deg, rgba(108, 92, 231, .07), rgba(0, 180, 216, .05));
}
.welcome .emoji { font-size: 2.6rem; }
.welcome h3 { margin: .4rem 0 .2rem 0; font-weight: 700; }
.welcome p { margin: 0; opacity: .65; }
.main .stButton > button, [data-testid="stMain"] .stButton > button {
    border-radius: 14px; padding: .65rem .9rem; height: 100%;
    border: 1px solid rgba(108, 92, 231, .35);
    transition: transform .12s ease, box-shadow .12s ease;
}
[data-testid="stMain"] .stButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 6px 16px rgba(108, 92, 231, .22);
    border-color: #6C5CE7;
}
</style>
"""


def apply_styles():
    st.markdown(CSS, unsafe_allow_html=True)


def render_header(title: str):
    st.markdown(
        f'<div class="app-hero"><h1>{html.escape(title)}</h1>'
        f"<p>{html.escape(SUBTITLE)}</p></div>",
        unsafe_allow_html=True,
    )


def _use_suggestion(prompt: str):
    st.session_state[PENDING_KEY] = prompt


def render_welcome():
    """Empty-state card with clickable example prompts."""
    st.markdown(
        '<div class="welcome"><div class="emoji">🤖</div>'
        "<h3>How can I help you today?</h3>"
        "<p>Ask anything, or try one of these to get started.</p></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(len(SUGGESTIONS))
    for i, (col, (icon, text)) in enumerate(zip(cols, SUGGESTIONS)):
        col.button(f"{icon} {text}", key=f"suggestion_{i}",
                   on_click=_use_suggestion, args=(text,))