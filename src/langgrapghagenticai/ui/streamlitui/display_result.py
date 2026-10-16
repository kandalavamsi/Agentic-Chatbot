import streamlit as st

HISTORY_KEY = "chat_history"  # list of {"role": "user"|"assistant", "content": str}
AVATARS = {"user": "👤", "assistant": "🤖"}


def chat_message(role):
    return st.chat_message(role, avatar=AVATARS[role])


def init_history():
    """Create the per-session chat history if it doesn't exist yet."""
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []


def clear_history():
    st.session_state[HISTORY_KEY] = []


def render_count(slot):
    """Write the 'N messages' caption into a sidebar placeholder."""
    turns = len(st.session_state[HISTORY_KEY]) // 2
    slot.caption(f"💬 {turns} message{'s' if turns != 1 else ''} in this chat")


def render_history():
    """Re-draw earlier turns. Streamlit reruns the script on every interaction,
    so without this the conversation would vanish from the screen."""
    for msg in st.session_state[HISTORY_KEY]:
        with chat_message(msg["role"]):
            st.write(msg["content"])


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message, count_slot=None):
        self.count_slot = count_slot
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        if self.usecase != "Basic Chatbot":
            return

        with chat_message("user"):
            st.write(self.user_message)

        # Send the WHOLE conversation so the model remembers earlier turns.
        history = st.session_state[HISTORY_KEY]
        messages = [(m["role"], m["content"]) for m in history]
        messages.append(("user", self.user_message))

        reply = None
        with chat_message("assistant"):
            with st.spinner("Thinking..."):
                for event in self.graph.stream({"messages": messages}):
                    for value in event.values():
                        reply = value["messages"].content
            if reply is not None:
                st.write(reply)

        # Only commit the turn once the model actually answered, so a failed
        # call (e.g. bad API key) doesn't leave a dangling user message.
        if reply is not None:
            history.append({"role": "user", "content": self.user_message})
            history.append({"role": "assistant", "content": reply})
            if self.count_slot is not None:
                render_count(self.count_slot)  # sidebar was drawn before this turn