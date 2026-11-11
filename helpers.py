"""Small reusable helpers: time, titles, export, copy button and custom CSS."""

import json
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from config import APP_NAME, MAX_TITLE_LENGTH


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------
def current_time() -> str:
    """Timestamp shown under each message, e.g. '09:41 PM'."""
    return datetime.now().strftime("%I:%M %p")


def make_title(text: str) -> str:
    """Create a short conversation title from the first user message."""
    single_line = " ".join(text.split())
    if len(single_line) <= MAX_TITLE_LENGTH:
        return single_line
    return single_line[: MAX_TITLE_LENGTH - 1].rstrip() + "…"


def conversation_stats(conversation: dict) -> dict:
    """Count messages, characters and (when Gemini reports them) tokens."""
    messages = [m for m in conversation["messages"] if not m.get("is_error")]
    return {
        "messages": len(messages),
        "characters": sum(len(m["content"]) for m in messages),
        "tokens": sum(m.get("tokens") or 0 for m in messages),
    }


def export_conversation(conversation: dict, fmt: str = "txt") -> str:
    """Return the conversation as plain text ('txt') or Markdown ('md')."""
    exported_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    messages = [m for m in conversation["messages"] if not m.get("is_error")]
    lines = []

    if fmt == "md":
        lines += [f"# {conversation['title']}", f"*Exported from {APP_NAME} on {exported_on}*", ""]
        for m in messages:
            who = "🧑 You" if m["role"] == "user" else f"✨ {APP_NAME}"
            lines += [f"### {who} · {m['time']}", "", m["content"], ""]
    else:
        lines += [f"{conversation['title']}", f"Exported from {APP_NAME} on {exported_on}", "=" * 50, ""]
        for m in messages:
            who = "You" if m["role"] == "user" else APP_NAME
            lines += [f"[{m['time']}] {who}:", m["content"], ""]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Copy-to-clipboard button
# ---------------------------------------------------------------------------
def copy_button(text: str) -> None:
    """Render a small button that copies ``text`` to the clipboard (runs in the browser)."""
    # Escape every "<" so AI output can never close the <script> tag or inject HTML.
    payload = json.dumps(text).replace("<", "\\u003c")
    html = f"""
    <style>
      body {{ margin: 0; background: transparent; }}
      button {{
        font: 500 13px Inter, system-ui, sans-serif; color: #e8ecf8; cursor: pointer;
        padding: 7px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,.14);
        background: rgba(255,255,255,.06); transition: all .2s;
      }}
      button:hover {{ border-color: #22d3ee; box-shadow: 0 0 14px rgba(34,211,238,.3); }}
    </style>
    <button id="copy-btn">📋 Copy</button>
    <script>
      const text = {payload};
      const btn = document.getElementById("copy-btn");
      btn.addEventListener("click", async () => {{
        try {{
          await navigator.clipboard.writeText(text);
        }} catch (err) {{
          const area = document.createElement("textarea");
          area.value = text;
          document.body.appendChild(area);
          area.select();
          document.execCommand("copy");
          document.body.removeChild(area);
        }}
        btn.textContent = "✅ Copied!";
        setTimeout(() => (btn.textContent = "📋 Copy"), 1500);
      }});
    </script>
    """
    if hasattr(st, "iframe"):  # newer Streamlit
        st.iframe(html, height=44)
    else:  # older Streamlit versions
        components.html(html, height=44)


# ---------------------------------------------------------------------------
# Custom CSS (this is what makes the app not look like default Streamlit)
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

:root {
  --bg: #05060f; --navy: #0a1128;
  --purple: #8b5cf6; --blue: #3b82f6; --cyan: #22d3ee;
  --glass: rgba(255,255,255,0.05); --glass-strong: rgba(255,255,255,0.09);
  --border: rgba(255,255,255,0.10); --text: #e8ecf8; --muted: #8d97b5;
}

/* ---------- Base ---------- */
.stApp, .stMarkdown, .stButton button, .stDownloadButton button, textarea, input {
  font-family: 'Inter', system-ui, sans-serif;
}
.stApp {
  color: var(--text);
  background:
    radial-gradient(900px 520px at 88% -8%, rgba(139,92,246,.28), transparent 60%),
    radial-gradient(800px 520px at -8% 108%, rgba(34,211,238,.16), transparent 60%),
    linear-gradient(160deg, var(--bg) 0%, var(--navy) 100%);
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 920px; padding-top: 1.6rem; padding-bottom: 7rem; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,.4); border-radius: 8px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
  background: rgba(7,10,26,.78);
  backdrop-filter: blur(22px); -webkit-backdrop-filter: blur(22px);
  border-right: 1px solid var(--border);
}
.brand { display: flex; align-items: center; gap: .7rem; margin: .2rem 0 1.1rem; }
.brand-logo {
  width: 42px; height: 42px; border-radius: 14px; display: grid; place-items: center;
  font-size: 1.3rem; background: linear-gradient(135deg, var(--purple), var(--blue) 55%, var(--cyan));
  box-shadow: 0 0 24px rgba(139,92,246,.5);
}
.brand-name { font: 700 1.25rem 'Space Grotesk', sans-serif; line-height: 1.1; }
.brand-tag { font-size: .72rem; color: var(--muted); }
.section-label {
  font-size: .7rem; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); margin: 1.1rem 0 .4rem; font-weight: 600;
}
.status-pill {
  display: inline-flex; align-items: center; gap: .45rem; padding: .3rem .75rem;
  border-radius: 999px; font-size: .78rem; border: 1px solid var(--border); background: var(--glass);
}
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.dot.ok { background: #34d399; box-shadow: 0 0 10px #34d399; }
.dot.bad { background: #f87171; box-shadow: 0 0 10px #f87171; }
.dot.idle { background: #fbbf24; box-shadow: 0 0 10px #fbbf24; }
.model-card {
  padding: .8rem .9rem; border-radius: 14px; background: var(--glass);
  border: 1px solid var(--border); font-size: .82rem; color: var(--muted); line-height: 1.6;
}
.model-card b { color: var(--text); }

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {
  width: 100%; border-radius: 12px; border: 1px solid var(--border);
  background: var(--glass); color: var(--text); font-weight: 500;
  transition: all .22s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: var(--cyan); color: #fff; transform: translateY(-1px);
  box-shadow: 0 6px 22px rgba(34,211,238,.18); background: var(--glass-strong);
}
.st-key-new_chat button {
  background: linear-gradient(135deg, var(--purple), var(--blue) 60%, var(--cyan));
  border: none; font-weight: 600; box-shadow: 0 8px 24px rgba(99,102,241,.35);
}
.st-key-new_chat button:hover { filter: brightness(1.12); box-shadow: 0 10px 30px rgba(99,102,241,.5); }

/* ---------- Inputs ---------- */
[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input {
  background: var(--glass) !important; border-radius: 12px !important;
  border: 1px solid var(--border) !important; color: var(--text) !important;
}
[data-testid="stExpander"] {
  background: var(--glass); border: 1px solid var(--border); border-radius: 14px;
}
[data-testid="stBottom"] > div { background: transparent; }
[data-testid="stChatInput"] {
  background: rgba(255,255,255,.06); border: 1px solid var(--border);
  border-radius: 20px; backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 10px 40px rgba(0,0,0,.35); transition: border-color .2s, box-shadow .2s;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--purple); box-shadow: 0 0 0 3px rgba(139,92,246,.25), 0 10px 40px rgba(0,0,0,.35);
}
[data-testid="stChatInput"] textarea { color: var(--text); }

/* ---------- Chat header ---------- */
.chat-header {
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
  padding: .75rem 1.1rem; margin-bottom: 1rem; border-radius: 16px;
  background: var(--glass); border: 1px solid var(--border);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
}
.chat-title { font: 600 1rem 'Space Grotesk', sans-serif; }
.chip {
  font-size: .74rem; padding: .25rem .7rem; border-radius: 999px; color: var(--cyan);
  border: 1px solid rgba(34,211,238,.35); background: rgba(34,211,238,.08); white-space: nowrap;
}

/* ---------- Welcome ---------- */
.welcome { text-align: center; padding: 2rem 0 1.2rem; }
.orb {
  width: 92px; height: 92px; border-radius: 50%; margin: 0 auto 1.4rem; position: relative;
  background: conic-gradient(from 0deg, var(--purple), var(--blue), var(--cyan), var(--purple));
  box-shadow: 0 0 60px rgba(139,92,246,.55);
  animation: spin 7s linear infinite, pulse 3.2s ease-in-out infinite;
}
.orb::after { content: ""; position: absolute; inset: 9px; border-radius: 50%; background: #070a1c; }
.welcome-title {
  font: 700 2.2rem/1.2 'Space Grotesk', sans-serif; margin: 0 0 .6rem;
  background: linear-gradient(90deg, #c4b5fd, #93c5fd, #67e8f9);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.welcome-sub { color: var(--muted); max-width: 520px; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes pulse { 50% { box-shadow: 0 0 90px rgba(34,211,238,.55); } }

/* ---------- Suggestion cards ---------- */
.glass-card {
  padding: 1.1rem 1.2rem; margin-bottom: .4rem; border-radius: 18px; min-height: 118px;
  background: var(--glass); border: 1px solid var(--border);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  transition: all .25s ease;
}
.glass-card:hover {
  transform: translateY(-4px); border-color: rgba(139,92,246,.6);
  box-shadow: 0 14px 40px rgba(139,92,246,.25); background: var(--glass-strong);
}
.card-icon { font-size: 1.5rem; margin-bottom: .35rem; }
.card-title { font-weight: 600; margin-bottom: .2rem; }
.card-desc { font-size: .83rem; color: var(--muted); }

/* ---------- Chat messages ---------- */
[data-testid="stChatMessage"] {
  background: var(--glass); border: 1px solid var(--border); border-radius: 18px;
  padding: 1rem 1.15rem; margin-bottom: .7rem;
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: linear-gradient(135deg, rgba(139,92,246,.30), rgba(59,130,246,.22));
  border-color: rgba(139,92,246,.45);
}
.msg-meta { font-size: .74rem; color: var(--muted); margin-top: .2rem; }

/* ---------- Loading animation ---------- */
.typing { display: flex; align-items: center; gap: .5rem; color: var(--muted); font-size: .9rem; }
.typing span.d {
  width: 8px; height: 8px; border-radius: 50%; display: inline-block;
  background: linear-gradient(135deg, var(--purple), var(--cyan)); animation: bounce 1.2s infinite ease-in-out;
}
.typing span.d:nth-child(2) { animation-delay: .15s; }
.typing span.d:nth-child(3) { animation-delay: .3s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(.5); opacity: .4; } 40% { transform: scale(1.1); opacity: 1; } }

/* ---------- Responsive ---------- */
@media (max-width: 992px) { .block-container { max-width: 100%; padding-left: 1.2rem; padding-right: 1.2rem; } }
@media (max-width: 640px) {
  .block-container { padding: 1rem .75rem 7rem; }
  .welcome-title { font-size: 1.55rem; }
  .orb { width: 72px; height: 72px; }
  .chat-header { flex-direction: column; align-items: flex-start; gap: .4rem; }
  .glass-card { min-height: 0; }
}
</style>
"""


def inject_css() -> None:
    """Apply the custom dark glassmorphism theme."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
