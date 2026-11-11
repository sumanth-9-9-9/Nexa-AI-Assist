"""Sidebar: logo, new chat, history, prompt library, model info and settings."""

import streamlit as st

import chat_manager
import config
import gemini_client
from prompt_templates import CATEGORY_ICONS, PROMPT_LIBRARY
from helpers import conversation_stats, export_conversation


def _run_connection_test() -> None:
    """Button callback: check the API key and model, remember the result."""
    key = config.get_api_key(st.session_state.api_key_override)
    st.session_state.api_status = gemini_client.test_connection(key, st.session_state.model)


def _render_brand() -> None:
    st.markdown(
        f"""
        <div class="brand">
          <div class="brand-logo">{config.APP_ICON}</div>
          <div>
            <div class="brand-name">{config.APP_NAME}</div>
            <div class="brand-tag">{config.APP_TAGLINE}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_history() -> None:
    st.markdown('<div class="section-label">Chat history</div>', unsafe_allow_html=True)
    conversations = st.session_state.conversations
    for conversation_id in reversed(list(conversations)):
        conversation = conversations[conversation_id]
        is_active = conversation_id == st.session_state.current_id
        title_column, delete_column = st.columns([5, 1])
        with title_column:
            st.button(
                ("● " if is_active else "💬 ") + conversation["title"],
                key=f"chat_{conversation_id}",
                on_click=chat_manager.switch_chat,
                args=(conversation_id,),
            )
        with delete_column:
            st.button("🗑", key=f"del_{conversation_id}", help="Delete this chat",
                      on_click=chat_manager.delete_chat, args=(conversation_id,))


def _render_prompt_library() -> None:
    st.markdown('<div class="section-label">Prompt library</div>', unsafe_allow_html=True)
    with st.expander("📚 Browse templates"):
        category = st.selectbox(
            "Category",
            list(PROMPT_LIBRARY),
            format_func=lambda name: f"{CATEGORY_ICONS.get(name, '•')} {name}",
            label_visibility="collapsed",
        )
        for index, template in enumerate(PROMPT_LIBRARY[category]):
            st.button(
                template["title"],
                key=f"tpl_{category}_{index}",
                help=template["prompt"],
                on_click=chat_manager.set_pending_prompt,
                args=(template["prompt"],),
            )


def _render_model_info() -> None:
    st.markdown('<div class="section-label">AI model</div>', unsafe_allow_html=True)
    key_present = bool(config.get_api_key(st.session_state.api_key_override))
    status = st.session_state.api_status

    if status is not None:
        ok, message = status
        dot, label = ("ok", message) if ok else ("bad", "Connection problem")
    elif key_present:
        dot, label = "ok", "API key found"
    else:
        dot, label = "idle", "Demo Mode (Offline)"

    st.markdown(
        f"""
        <div class="model-card">
          <b>{st.session_state.model}</b><br>
          Google Gemini · temp {st.session_state.temperature:.1f}<br>
          <span class="status-pill"><span class="dot {dot}"></span>{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if status is not None and not status[0]:
        st.caption(status[1])
    st.button("🔌 Test connection", key="test_conn", on_click=_run_connection_test)


def _render_settings() -> None:
    st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)
    with st.expander("⚙️ Settings"):
        st.selectbox("Gemini model", config.AVAILABLE_MODELS, key="model")
        st.slider("Temperature (creativity)", config.MIN_TEMPERATURE, config.MAX_TEMPERATURE,
                  step=0.1, key="temperature",
                  help="Lower = focused and predictable. Higher = more creative.")
        st.text_area("System instruction", key="system_instruction", height=130,
                     help="Controls how Nexa AI behaves in every reply.")
        st.button("Reset instruction", key="reset_instruction",
                  on_click=lambda: st.session_state.update(system_instruction=config.DEFAULT_SYSTEM_INSTRUCTION))
        st.text_input("API key (optional, this session only)", key="api_key_override", type="password",
                      help="Overrides GEMINI_API_KEY from your .env file. Never stored on disk.")


def _render_conversation_tools() -> None:
    conversation = chat_manager.get_current()
    stats = conversation_stats(conversation)

    st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)
    st.caption(f"{stats['messages']} messages · {stats['characters']:,} characters · {stats['tokens']:,} tokens")

    st.button("🧹 Clear conversation", key="clear_chat", on_click=chat_manager.clear_current)

    if conversation["messages"]:
        st.download_button("⬇️ Export as TXT", export_conversation(conversation, "txt"),
                           file_name=f"nexa-chat-{conversation['id']}.txt", mime="text/plain", key="export_txt")
        st.download_button("⬇️ Export as Markdown", export_conversation(conversation, "md"),
                           file_name=f"nexa-chat-{conversation['id']}.md", mime="text/markdown", key="export_md")

    if len(st.session_state.conversations) > 1:
        st.button("🗑 Delete all history", key="clear_all", on_click=chat_manager.clear_all)


def render_sidebar() -> None:
    with st.sidebar:
        _render_brand()
        st.button("＋  New Chat", key="new_chat", on_click=chat_manager.new_chat)
        _render_history()
        _render_prompt_library()
        _render_model_info()
        _render_settings()
        _render_conversation_tools()
