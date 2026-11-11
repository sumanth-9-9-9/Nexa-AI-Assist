"""Conversation management, stored in Streamlit's session state.

Session state lives only while the browser tab is open, which keeps this
project simple. (See README "Future enhancements" for saving to a database.)
"""

import uuid

import streamlit as st

import config
from helpers import current_time, make_title


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
def init_state() -> None:
    """Create all session-state keys the first time the app runs."""
    defaults = {
        "conversations": {},          # {conversation_id: conversation dict}
        "current_id": None,           # id of the conversation being shown
        "pending_prompt": None,       # prompt queued by a card / template button
        "model": config.DEFAULT_MODEL,
        "temperature": config.DEFAULT_TEMPERATURE,
        "system_instruction": config.DEFAULT_SYSTEM_INSTRUCTION,
        "api_key_override": "",       # key typed in Settings (session only)
        "api_status": None,           # (ok: bool, message: str) after a connection test
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    if st.session_state.current_id not in st.session_state.conversations:
        new_chat()


# ---------------------------------------------------------------------------
# Conversations
# ---------------------------------------------------------------------------
def get_current() -> dict:
    return st.session_state.conversations[st.session_state.current_id]


def new_chat() -> None:
    """Start a new conversation (re-uses the current one if it is still empty)."""
    current = st.session_state.conversations.get(st.session_state.current_id)
    if current is not None and not current["messages"]:
        return

    conversation_id = uuid.uuid4().hex[:8]
    st.session_state.conversations[conversation_id] = {
        "id": conversation_id,
        "title": config.NEW_CHAT_TITLE,
        "messages": [],
    }
    st.session_state.current_id = conversation_id


def switch_chat(conversation_id: str) -> None:
    if conversation_id in st.session_state.conversations:
        st.session_state.current_id = conversation_id


def delete_chat(conversation_id: str) -> None:
    st.session_state.conversations.pop(conversation_id, None)
    if st.session_state.current_id == conversation_id:
        remaining = list(st.session_state.conversations)
        st.session_state.current_id = remaining[-1] if remaining else None
    if st.session_state.current_id is None:
        new_chat()


def clear_current() -> None:
    """Remove all messages from the current conversation (context is reset)."""
    conversation = get_current()
    conversation["messages"] = []
    conversation["title"] = config.NEW_CHAT_TITLE


def clear_all() -> None:
    """Delete the entire chat history."""
    st.session_state.conversations = {}
    st.session_state.current_id = None
    new_chat()


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------
def add_message(role: str, content: str, tokens: int | None = None, is_error: bool = False) -> None:
    """Append a message. The first user message becomes the conversation title."""
    conversation = get_current()
    conversation["messages"].append(
        {
            "role": role,            # "user" or "assistant"
            "content": content,
            "time": current_time(),
            "tokens": tokens,
            "is_error": is_error,
        }
    )
    if role == "user" and conversation["title"] == config.NEW_CHAT_TITLE:
        conversation["title"] = make_title(content)


def remove_last_assistant() -> None:
    """Drop the last AI reply so it can be regenerated."""
    messages = get_current()["messages"]
    if messages and messages[-1]["role"] == "assistant":
        messages.pop()


def set_pending_prompt(prompt: str) -> None:
    """Queue a prompt (from a card or template). app.py sends it on the next run."""
    st.session_state.pending_prompt = prompt
