"""Nexa AI - Smart AI Assistant (entry point).

Run with:  streamlit run app.py
"""

import streamlit as st

import chat_manager
import config
from chat_interface import generate_reply, render_header, render_messages, render_welcome
from sidebar import render_sidebar
from helpers import inject_css

st.set_page_config(
    page_title=f"{config.APP_NAME} – {config.APP_TAGLINE}",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    chat_manager.init_state()
    inject_css()

    # 1. Collect the user's input: typed text, or a prompt queued by a card/template.
    typed_prompt = st.chat_input("Message Nexa AI…")
    prompt = st.session_state.pending_prompt or typed_prompt
    st.session_state.pending_prompt = None
    if prompt:
        chat_manager.add_message("user", prompt)

    # 2. Draw the interface.
    render_sidebar()
    conversation = chat_manager.get_current()
    render_header(conversation)

    if not conversation["messages"]:
        render_welcome()
        return

    render_messages(conversation)

    # 3. If the last message is from the user, Gemini still owes a reply
    #    (this also powers "Regenerate").
    if conversation["messages"][-1]["role"] == "user":
        generate_reply(conversation)


main()
