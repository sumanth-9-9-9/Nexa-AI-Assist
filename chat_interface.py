"""Main chat area: header, welcome screen, message bubbles and reply generation."""

import streamlit as st

import chat_manager
import config
import gemini_client
from prompt_cards import render_prompt_cards
from helpers import copy_button

LOADING_HTML = """
<div class="typing"><span class="d"></span><span class="d"></span><span class="d"></span>
<span>Nexa is thinking…</span></div>
"""

USER_AVATAR = "🙂"
AI_AVATAR = "✨"


def render_header(conversation: dict) -> None:
    st.markdown(
        f"""
        <div class="chat-header">
          <div class="chat-title">💬 {_escape(conversation['title'])}</div>
          <div class="chip">⚡ {_escape(st.session_state.model)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome() -> None:
    """Welcome hero + suggestion cards (shown while the chat is empty)."""
    st.markdown(
        f"""
        <div class="welcome">
          <div class="orb"></div>
          <h1 class="welcome-title">{config.WELCOME_MESSAGE}</h1>
          <p class="welcome-sub">{config.WELCOME_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not config.get_api_key(st.session_state.api_key_override):
        st.info(
            "✨ **Demo Mode Active** — You can start chatting or click any suggestion card right away! "
            "To connect to live Google Gemini models, enter your free API key in **⚙️ Settings** (sidebar) or in your `.env` file."
        )
    render_prompt_cards()


def render_messages(conversation: dict) -> None:
    """Draw every message in the conversation."""
    messages = conversation["messages"]
    for index, message in enumerate(messages):
        is_user = message["role"] == "user"
        with st.chat_message(message["role"], avatar=USER_AVATAR if is_user else AI_AVATAR):
            if message.get("is_error"):
                st.error(message["content"])
            else:
                st.markdown(message["content"])

            meta = message["time"]
            if message.get("tokens"):
                meta += f" · {message['tokens']:,} tokens"
            st.markdown(f'<div class="msg-meta">{meta}</div>', unsafe_allow_html=True)

            if not is_user:
                _render_assistant_actions(conversation["id"], index, message, is_last=index == len(messages) - 1)


def _render_assistant_actions(conversation_id: str, index: int, message: dict, is_last: bool) -> None:
    """Copy and Regenerate buttons under an AI message."""
    copy_column, regen_column, _ = st.columns([1, 1.3, 4])
    if not message.get("is_error"):
        with copy_column:
            copy_button(message["content"])
    if is_last:
        with regen_column:
            st.button(
                "🔄 Retry" if message.get("is_error") else "🔄 Regenerate",
                key=f"regen_{conversation_id}_{index}",
                on_click=chat_manager.remove_last_assistant,
            )


def generate_reply(conversation: dict) -> None:
    """Ask Gemini to answer the latest user message, then refresh the page."""
    with st.chat_message("assistant", avatar=AI_AVATAR):
        placeholder = st.empty()
        placeholder.markdown(LOADING_HTML, unsafe_allow_html=True)

        result = gemini_client.generate_response(
            messages=conversation["messages"],
            api_key=config.get_api_key(st.session_state.api_key_override),
            model=st.session_state.model,
            temperature=st.session_state.temperature,
            system_instruction=st.session_state.system_instruction,
        )
        placeholder.empty()

    if result.ok:
        chat_manager.add_message("assistant", result.text, tokens=result.total_tokens)
    else:
        chat_manager.add_message("assistant", result.error, is_error=True)
    st.rerun()


def _escape(text: str) -> str:
    return (
        str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )
