"""Gemini API wrapper built on the official Google Gen AI SDK (``google-genai``).

This module knows nothing about Streamlit. It takes a list of messages and
returns a ``GeminiResult``, so it is easy to test and reuse.
"""

from dataclasses import dataclass
from typing import Optional

from google import genai
from google.genai import errors, types

import config


@dataclass
class GeminiResult:
    """What we get back from a Gemini call."""

    text: str = ""
    total_tokens: Optional[int] = None
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None


def _build_contents(messages: list[dict]) -> list[types.Content]:
    """Convert our chat messages into the format Gemini expects.

    Gemini uses the roles "user" and "model" (not "assistant"). Error messages
    are skipped so they never pollute the conversation context.
    """
    contents = []
    for message in messages:
        if message.get("is_error"):
            continue
        role = "user" if message["role"] == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=message["content"])])
        )
    return contents


def _friendly_error(exc: Exception) -> str:
    """Turn an SDK exception into a short, helpful message."""
    if isinstance(exc, errors.APIError):
        code = getattr(exc, "code", None)
        detail = (getattr(exc, "message", "") or str(exc)).strip()
        lowered = detail.lower()
        if "api key" in lowered or "api_key" in lowered or code in (401, 403):
            return ("Your API key was rejected. Check GEMINI_API_KEY in your .env file "
                    "or the key in Settings.")
        if code == 404:
            return ("This model was not found. Choose another model in Settings or update "
                    "AVAILABLE_MODELS in config.py.")
        if code == 429:
            return ("Rate limit or quota reached. Please wait a moment and try again, "
                    "or check your quota in Google AI Studio.")
        if code == 400:
            return f"The request was not accepted by Gemini: {detail[:200]}"
        if code and code >= 500:
            return "Gemini is temporarily unavailable. Please try again shortly."
        return f"Gemini API error ({code}): {detail[:200]}"
    if isinstance(exc, (ConnectionError, TimeoutError)):
        return "Could not reach Gemini. Please check your internet connection."
    return f"Unexpected error: {exc}"


def _generate_demo_response(messages: list[dict]) -> GeminiResult:
    """Generate a high-quality simulated response when no Gemini API key is configured."""
    last_msg = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_msg = m.get("content", "").strip()
            break

    lowered = last_msg.lower()

    if any(k in lowered for k in ["neural network", "deep learning", "machine learning", "overfitting"]):
        reply = (
            "### 🧠 How Neural Networks Learn\n\n"
            "**Everyday Analogy:**\n"
            "Imagine learning to shoot a basketball. The first time you take a shot, you shoot too far to the left. "
            "Your brain notices the mistake, adjusts your arm angle, and next time you shoot a bit more to the right. "
            "After hundreds of repetitions, your muscles 'remember' the exact movement needed to score consistently.\n\n"
            "**Technical Breakdown:**\n"
            "1. **Forward Propagation:** Input features are passed through layers of artificial neurons. Each connection has a **weight** and **bias** that compute an initial prediction.\n"
            "2. **Loss Calculation:** A loss function measures the difference (error) between the prediction and the true target.\n"
            "3. **Backpropagation:** Using calculus (the chain rule), gradients of the loss with respect to each weight are calculated backwards through the network.\n"
            "4. **Optimization (Gradient Descent):** An optimizer (e.g. Adam, SGD) updates the weights in the direction that minimizes the loss.\n\n"
            "> 💡 *Nexa AI is running in Demo Mode. Connect your Gemini API key in Settings or .env to unlock real-time Gemini generation.*"
        )
    elif any(k in lowered for k in ["python", "pandas", "csv", "code", "script", "function", "dataframe"]):
        reply = (
            "### 🐍 Python Data Analysis Script\n\n"
            "Here is a clean, well-commented script using **pandas** to read a CSV dataset and display descriptive statistics:\n\n"
            "```python\n"
            "import pandas as pd\n\n"
            "def analyze_dataset(file_path: str) -> None:\n"
            "    \"\"\"Load a CSV file and display descriptive statistics.\"\"\"\n"
            "    try:\n"
            "        df = pd.read_csv(file_path)\n"
            "        print(f'✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.\\n')\n"
            "        \n"
            "        print('--- Column Types & Missing Values ---')\n"
            "        print(df.info())\n"
            "        \n"
            "        print('\\n--- Numerical Summary Statistics ---')\n"
            "        print(df.describe().T)\n"
            "    except FileNotFoundError:\n"
            "        print(f'❌ Error: File {file_path} not found.')\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    analyze_dataset('data.csv')\n"
            "```\n\n"
            "> 💡 *Nexa AI is running in Demo Mode. Connect your Gemini API key in Settings or .env to unlock real-time Gemini generation.*"
        )
    elif any(k in lowered for k in ["email", "feedback", "manager", "internship", "letter"]):
        reply = (
            "### ✍️ Professional Feedback Request Email\n\n"
            "**Subject:** Mid-Project Review & Feedback Request – [Your Name]\n\n"
            "Dear [Manager's Name],\n\n"
            "I hope you are having a productive week.\n\n"
            "As we reach the midpoint of my internship project on **Nexa AI Assistant**, I would greatly appreciate the opportunity to get your feedback on my progress and deliverables so far.\n\n"
            "I have summarized the core milestones achieved, including the modular architecture and user interface enhancements. If your calendar permits, I would love to schedule a brief 15-minute catch-up next week, or I would be happy to share a summary document for your async review.\n\n"
            "Thank you very much for your continuous guidance and mentorship.\n\n"
            "Best regards,\n\n"
            "**[Your Name]**  \n"
            "Generative AI Intern  \n"
            "[Your Contact Information]\n\n"
            "> 💡 *Nexa AI is running in Demo Mode. Connect your Gemini API key in Settings or .env to unlock real-time Gemini generation.*"
        )
    elif any(k in lowered for k in ["summarize", "summary", "document", "article"]):
        reply = (
            "### 📄 Document Summary Template\n\n"
            "Please paste the text or document you would like analyzed! Once provided, I will extract:\n\n"
            "1. **Executive Summary:** A concise 2-3 sentence overview.\n"
            "2. **Key Takeaways (Top 5 Points):** Core findings and crucial data points.\n"
            "3. **Action Items & Next Steps:** Concrete responsibilities and timeline.\n\n"
            "> 💡 *Nexa AI is running in Demo Mode. Connect your Gemini API key in Settings or .env to unlock real-time Gemini generation.*"
        )
    elif any(k in lowered for k in ["hi", "hello", "hey", "who are you", "help"]):
        reply = (
            "Hello! I am **Nexa AI**, your smart assistant.\n\n"
            "I can help you with:\n"
            "- 🧠 Explaining complex scientific, ML, or tech topics\n"
            "- 💻 Writing, debugging, and reviewing Python code\n"
            "- ✍️ Drafting professional emails, articles, and reports\n"
            "- 📊 Data Science, prompt engineering, and interview preparation\n\n"
            "Feel free to ask me anything or click one of the suggested cards below!\n\n"
            "> 💡 *Running in Demo Mode. To enable live Gemini LLM responses, add your free API key in **Settings** or in `.env`.*"
        )
    else:
        reply = (
            f"### 🤖 Response to: *\"{last_msg}\"*\n\n"
            "Thank you for your question! Here is a structured overview:\n\n"
            "- **Overview:** The topic you mentioned involves understanding the underlying principles and structuring a systematic approach.\n"
            "- **Key Insight:** When exploring this domain, prioritizing clear requirements and iterative verification yields the best outcomes.\n"
            "- **Practical Tip:** You can test related concepts using the Prompt Library in the sidebar or adjusting generation parameters.\n\n"
            "> 💡 *Nexa AI is running in Demo Mode. To connect to live Google Gemini models (Gemini 2.5 Flash, etc.), add your free Gemini API key in **Settings** or your `.env` file.*"
        )

    return GeminiResult(text=reply, total_tokens=max(24, len(reply.split())))


def generate_response(
    messages: list[dict],
    api_key: str,
    model: str,
    temperature: float,
    system_instruction: str,
) -> GeminiResult:
    """Send the whole conversation to Gemini and return its reply."""
    if not api_key:
        return _generate_demo_response(messages)

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=_build_contents(messages),
            config=types.GenerateContentConfig(
                system_instruction=system_instruction or None,
                temperature=temperature,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - we want to show every failure nicely
        return GeminiResult(error=_friendly_error(exc))

    text = (response.text or "").strip()
    if not text:
        reason = ""
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            reason = f" (blocked: {response.prompt_feedback.block_reason})"
        elif response.candidates and response.candidates[0].finish_reason:
            reason = f" (finish reason: {response.candidates[0].finish_reason})"
        return GeminiResult(error=f"Gemini returned an empty response{reason}. Try rephrasing your message.")

    usage = response.usage_metadata
    tokens = getattr(usage, "total_token_count", None) if usage else None
    return GeminiResult(text=text, total_tokens=tokens)


def test_connection(api_key: str, model: str) -> tuple[bool, str]:
    """Check that the key works and the model exists. Returns (ok, message)."""
    if not api_key:
        return True, "Demo Mode Active (Ready to chat)"
    try:
        client = genai.Client(api_key=api_key)
        client.models.get(model=model)
        return True, "Connected"
    except Exception as exc:  # noqa: BLE001
        return False, _friendly_error(exc)
