"""The four suggestion cards shown on the welcome screen."""

import streamlit as st

import chat_manager

SUGGESTION_CARDS = [
    {
        "icon": "🧠",
        "title": "Explain a complex topic",
        "desc": "Break down hard ideas into simple, clear explanations.",
        "prompt": "Explain how neural networks learn, in simple terms. Use an everyday analogy and then a short technical summary.",
    },
    {
        "icon": "💻",
        "title": "Generate Python code",
        "desc": "Get clean, commented, ready-to-run Python snippets.",
        "prompt": "Write a clean, well-commented Python script that reads a CSV file with pandas and prints summary statistics for each column.",
    },
    {
        "icon": "✍️",
        "title": "Write professional content",
        "desc": "Emails, reports and posts with the right tone.",
        "prompt": "Write a professional email to a manager requesting feedback on my internship project. Keep it polite, concise and confident.",
    },
    {
        "icon": "📄",
        "title": "Summarize a document",
        "desc": "Turn long text into key points and action items.",
        "prompt": "I want you to summarize a document. Ask me to paste the text, then give me a short summary, 5 key points and any action items.",
    },
]


def render_prompt_cards() -> None:
    """Show the cards in a 2x2 grid. Clicking a button sends that card's prompt."""
    for row_start in range(0, len(SUGGESTION_CARDS), 2):
        columns = st.columns(2)
        for column, index in zip(columns, range(row_start, row_start + 2)):
            card = SUGGESTION_CARDS[index]
            with column:
                st.markdown(
                    f"""
                    <div class="glass-card">
                      <div class="card-icon">{card['icon']}</div>
                      <div class="card-title">{card['title']}</div>
                      <div class="card-desc">{card['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.button(
                    "Try this →",
                    key=f"card_{index}",
                    on_click=chat_manager.set_pending_prompt,
                    args=(card["prompt"],),
                )
