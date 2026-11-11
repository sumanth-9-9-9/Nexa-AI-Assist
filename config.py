"""Central configuration for Nexa AI.

Everything you might want to tweak (app name, models, defaults) lives here,
so beginners only need to look in one place.
"""

import os

from dotenv import load_dotenv

# Reads the .env file (if present) and loads its values as environment variables.
load_dotenv()

# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------
APP_NAME = "Nexa AI"
APP_TAGLINE = "Smart AI Assistant"
APP_ICON = "✨"
WELCOME_MESSAGE = "Hello! I'm Nexa AI. How can I help you today?"
WELCOME_SUBTITLE = "Ask anything, explore ideas, write code, or pick a prompt below to get started."

# ---------------------------------------------------------------------------
# Gemini models
# ---------------------------------------------------------------------------
# Model names change over time. If you see a "model not found" error, check
# https://ai.google.dev/gemini-api/docs/models and update this list, or set
# GEMINI_MODEL in your .env file.
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
]
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
if DEFAULT_MODEL not in AVAILABLE_MODELS:
    AVAILABLE_MODELS.insert(0, DEFAULT_MODEL)

# ---------------------------------------------------------------------------
# Generation defaults
# ---------------------------------------------------------------------------
# Google recommends leaving temperature at 1.0 for Gemini 3 models.
DEFAULT_TEMPERATURE = 1.0
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0

DEFAULT_SYSTEM_INSTRUCTION = (
    "You are Nexa AI, a friendly, accurate and professional AI assistant. "
    "Give clear, well-structured answers. Use Markdown for formatting and "
    "fenced code blocks for code. If you are unsure, say so honestly."
)

# ---------------------------------------------------------------------------
# Conversations
# ---------------------------------------------------------------------------
NEW_CHAT_TITLE = "New chat"
MAX_TITLE_LENGTH = 30


def get_api_key(override: str = "") -> str:
    """Return the Gemini API key.

    A key typed into the Settings panel (``override``) wins over the
    ``GEMINI_API_KEY`` environment variable. The key is never hardcoded.
    """
    return (override or os.getenv("GEMINI_API_KEY", "")).strip()
