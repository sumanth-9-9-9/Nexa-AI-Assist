# ✨ Nexa AI – Smart AI Assistant

A modern, dark-themed AI chatbot built with **Python**, **Streamlit** and the **Google Gemini API**.
Nexa AI looks and feels like a premium SaaS assistant: glassmorphism cards, gradient accents,
chat history, a prompt library and one-click prompt suggestions.

> Built as a Generative AI internship project to demonstrate LLM integration, prompt engineering and clean Python architecture.

---

## 🎯 Project objectives

- Integrate Google's Gemini LLM using the official **Google Gen AI SDK** (`google-genai`).
- Maintain **conversation context** across messages.
- Demonstrate **prompt engineering** with a reusable Prompt Library and a custom system instruction.
- Deliver a polished, responsive UI instead of a default Streamlit page.
- Keep the code modular and easy for beginners to read and extend.

## 🚀 Features

| Area | What you get |
|---|---|
| **Chat** | Gemini-powered replies, message bubbles, timestamps, loading animation, context memory |
| **Welcome screen** | Animated orb, greeting, four clickable suggestion cards |
| **Conversations** | New chat, chat history, auto-titles from the first message, delete one / delete all, clear current chat |
| **Response tools** | 📋 Copy response, 🔄 Regenerate / Retry |
| **Prompt Library** | 8 categories × 4 templates (General, Python, ML, Data Science, GenAI, Academic, Interview, Content) |
| **Settings** | Model picker, temperature slider, custom system instruction, optional session-only API key |
| **Insights** | Message / character / token counts, API connection status and a "Test connection" button |
| **Export** | Download any conversation as **TXT** or **Markdown** |
| **Design** | Dark navy theme, purple/blue/cyan accents, glass cards, hover effects, responsive layout |

## 🧰 Technologies used

- Python 3.10+
- [Streamlit](https://streamlit.io) – web UI
- [Google Gen AI SDK](https://github.com/googleapis/python-genai) (`google-genai`) – Gemini API
- [python-dotenv](https://pypi.org/project/python-dotenv/) – loads the API key from `.env`
- Google AI Studio – to create the API key
- Git and GitHub – version control

## 🏗 Architecture

```
┌─────────────┐    user input     ┌──────────────────┐
│  Streamlit  │ ────────────────► │      app.py      │  entry point / orchestration
│  browser UI │ ◄──────────────── │                  │
└─────────────┘    rendered UI    └───────┬──────────┘
                                          │
        ┌─────────────────────────────────┼──────────────────────────┐
        ▼                                 ▼                          ▼
  UI modules                        chat_manager.py            gemini_client.py
  sidebar.py                        conversations in           Gemini API wrapper
  chat_interface.py                 st.session_state           (errors → friendly text)
  prompt_cards.py                                                     │
        │                                                             ▼
        └──────────────► helpers.py (CSS, export, copy)   Google Gemini API
                         config.py · prompt_templates.py
```

**How a message flows:** you type → `app.py` stores it via `chat_manager` → `chat_interface.generate_reply` sends the *entire* conversation to `gemini_client` → Gemini replies → the reply is stored and the page refreshes. Because the full history is sent every time, Gemini remembers the context.

### Folder structure

Everything lives in one flat folder:

```
nexa-ai/
├── app.py                 # Entry point
├── config.py              # App name, models, defaults, API key loading
├── gemini_client.py       # Gemini API calls + error handling
├── chat_manager.py        # Conversation state (session state)
├── prompt_templates.py    # Prompt Library data
├── sidebar.py             # Logo, history, library, settings, export
├── chat_interface.py      # Header, welcome, bubbles, reply generation
├── prompt_cards.py        # The 4 suggestion cards
├── helpers.py             # CSS theme, copy button, export, titles
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔑 Get a Gemini API key

1. Go to **[Google AI Studio](https://aistudio.google.com/apikey)** and sign in with your Google account.
2. Click **Create API key** (create or pick a Google Cloud project if asked).
3. Copy the key. Treat it like a password: never share it or commit it to GitHub.

## ⚙️ Installation

```bash
# 1. Go into the project folder
cd nexa-ai

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 🔐 Configure the `.env` file

```bash
# Windows:      copy .env.example .env
# macOS/Linux:  cp .env.example .env
```

Open `.env` and paste your key:

```
GEMINI_API_KEY=AIza...your_real_key...
```

Optional: choose a default model with `GEMINI_MODEL=gemini-3.5-flash`.
`.env` is listed in `.gitignore`, so it will never be uploaded to GitHub.

## ▶️ Run the application (VS Code)

1. Open the `nexa-ai` folder in VS Code (**File → Open Folder**).
2. Select the interpreter: `Ctrl+Shift+P` → **Python: Select Interpreter** → choose `.venv`.
3. Open the integrated terminal and run:

```bash
streamlit run app.py
```

4. Your browser opens at **http://localhost:8501**. Click **Test connection** in the sidebar to confirm your key works.

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| "No API key found" | Check that `.env` is in the project root and contains `GEMINI_API_KEY=...`, then restart Streamlit |
| "API key was rejected" | Create a new key in Google AI Studio |
| "Model was not found" | Model names change. Pick another model in **Settings**, or update `AVAILABLE_MODELS` in `config.py` using the [model list](https://ai.google.dev/gemini-api/docs/models) |
| "Rate limit / quota" | Wait a minute, or switch to a lighter model such as `gemini-3.5-flash-lite` |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt` |

## 🧑‍💻 Customizing (beginner tips)

- **Add a prompt template:** edit `prompt_templates.py`.
- **Change colors:** edit the CSS variables at the top of `CUSTOM_CSS` in `helpers.py`.
- **Change the assistant's personality:** edit `DEFAULT_SYSTEM_INSTRUCTION` in `config.py`, or use Settings.
- **Add a model:** append its name to `AVAILABLE_MODELS` in `config.py`.

## 📤 Upload to GitHub

```bash
git init
git add .
git status            # make sure .env is NOT listed
git commit -m "Initial commit: Nexa AI chatbot"
git branch -M main
```

Create an empty repository on github.com (without a README), then:

```bash
git remote add origin https://github.com/<your-username>/nexa-ai.git
git push -u origin main
```

## 🖼 Screenshots

Add your screenshots to a `screenshots/` folder and reference them here:

| Welcome screen | Chat view | Prompt Library |
|---|---|---|
| `![Welcome](screenshots/welcome.png)` | `![Chat](screenshots/chat.png)` | `![Library](screenshots/library.png)` |

## 🔮 Future enhancements

- Streaming responses (word-by-word output)
- Persistent chat history (SQLite or a cloud database)
- File upload and document Q&A (PDF summarization, RAG)
- Image input using Gemini's multimodal abilities
- User login and per-user history
- Light/dark theme toggle
- Voice input and text-to-speech
- Deployment to Streamlit Community Cloud

## 📄 License

For educational use. Add a license of your choice (e.g., MIT) before sharing publicly.
