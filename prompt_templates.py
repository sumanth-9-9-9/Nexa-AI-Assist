"""Prompt Library: reusable prompt templates grouped by category.

To add a template, append a dict with a ``title`` and a ``prompt`` to a category.
To add a category, add a new key to ``PROMPT_LIBRARY``.
"""

PROMPT_LIBRARY = {
    "General Assistant": [
        {"title": "Plan my day", "prompt": "Help me plan a productive day. Ask me about my tasks and energy levels, then create a realistic hour-by-hour schedule."},
        {"title": "Explain like I'm 12", "prompt": "Explain how the internet works in simple terms, as if I were 12 years old. Use an analogy."},
        {"title": "Pros and cons", "prompt": "Help me make a decision. Ask what the decision is, then give a balanced pros and cons table and a recommendation."},
        {"title": "Brainstorm ideas", "prompt": "Brainstorm 10 creative project ideas for a college student interested in technology. Include a one-line description for each."},
    ],
    "Python Programming": [
        {"title": "Write a function", "prompt": "Write a well-documented Python function that checks whether a string is a palindrome. Include type hints, a docstring and 3 test cases."},
        {"title": "Debug my code", "prompt": "I will paste some Python code that has a bug. Please ask me for the code and the error message, then explain the cause and show the fix."},
        {"title": "Explain a concept", "prompt": "Explain Python decorators to a beginner with a simple real-world analogy and two short code examples."},
        {"title": "Code review", "prompt": "Act as a senior Python reviewer. Ask me to paste my code, then review it for readability, PEP 8, performance and bugs."},
    ],
    "Machine Learning": [
        {"title": "Overfitting explained", "prompt": "Explain overfitting and underfitting in machine learning. Include how to detect them and 5 practical ways to reduce overfitting."},
        {"title": "Choose an algorithm", "prompt": "Help me choose a machine learning algorithm. Ask about my data and goal, then recommend 2-3 algorithms with reasons."},
        {"title": "Model metrics", "prompt": "Explain precision, recall, F1-score and ROC-AUC with a simple example, and when to use each."},
        {"title": "ML project roadmap", "prompt": "Give me a step-by-step roadmap for building my first end-to-end machine learning project, from data collection to deployment."},
    ],
    "Data Science": [
        {"title": "EDA checklist", "prompt": "Give me a practical exploratory data analysis (EDA) checklist for a new CSV dataset, with pandas code snippets for each step."},
        {"title": "Clean messy data", "prompt": "Explain the most common data-cleaning problems (missing values, duplicates, outliers) and how to fix each in pandas."},
        {"title": "Pick a chart", "prompt": "Help me pick the right chart type. Explain when to use bar, line, scatter, histogram and box plots, with one example each."},
        {"title": "Explain statistics", "prompt": "Explain p-values, confidence intervals and hypothesis testing in plain English with a coin-flip example."},
    ],
    "Generative AI": [
        {"title": "What are LLMs?", "prompt": "Explain how large language models work: tokens, embeddings, transformers and next-token prediction. Keep it beginner friendly."},
        {"title": "Prompt engineering tips", "prompt": "Teach me prompt engineering. Cover role prompting, few-shot examples, chain-of-thought, and output formatting with examples."},
        {"title": "What is RAG?", "prompt": "Explain Retrieval-Augmented Generation (RAG): why it is useful, how it works and a simple architecture diagram in text."},
        {"title": "AI risks", "prompt": "Explain hallucinations, bias and prompt injection in LLMs, and practical ways to reduce each risk."},
    ],
    "Academic Writing": [
        {"title": "Essay outline", "prompt": "Create a structured essay outline. Ask me for the topic and word count, then provide a thesis statement and section-by-section outline."},
        {"title": "Improve my paragraph", "prompt": "I will paste a paragraph. Please ask for it, then rewrite it to be clearer, more formal and more academic, and explain your changes."},
        {"title": "Literature review help", "prompt": "Explain how to write a literature review: structure, how to synthesise sources, and common mistakes to avoid."},
        {"title": "Abstract writer", "prompt": "Help me write a 150-word research abstract. Ask for the objective, method, results and conclusion, then combine them."},
    ],
    "Interview Preparation": [
        {"title": "Mock interview", "prompt": "Act as an interviewer for a Generative AI intern position. Ask me one question at a time, wait for my answer, then give feedback."},
        {"title": "Tell me about yourself", "prompt": "Help me craft a strong 60-second 'Tell me about yourself' answer for a technical internship. Ask me about my background first."},
        {"title": "Common Python questions", "prompt": "List 10 common Python interview questions for beginners with short, clear model answers."},
        {"title": "Behavioral (STAR)", "prompt": "Teach me the STAR method for behavioral interview questions and show a sample answer for 'Describe a challenge you overcame'."},
    ],
    "Content Writing": [
        {"title": "LinkedIn post", "prompt": "Write an engaging LinkedIn post announcing that I completed a Generative AI internship project. Ask me for the key details first."},
        {"title": "Professional email", "prompt": "Help me write a professional email. Ask who it is for and what I need, then draft it with a clear subject line."},
        {"title": "Blog outline", "prompt": "Create a blog post outline with a catchy title, introduction hook, 5 sections and a conclusion. Ask me for the topic first."},
        {"title": "Rewrite with tone", "prompt": "I will paste some text. Ask for it, then rewrite it in three tones: formal, friendly and persuasive."},
    ],
}

# Short descriptions shown under the category selector.
CATEGORY_ICONS = {
    "General Assistant": "🌐",
    "Python Programming": "🐍",
    "Machine Learning": "🤖",
    "Data Science": "📊",
    "Generative AI": "✨",
    "Academic Writing": "🎓",
    "Interview Preparation": "💼",
    "Content Writing": "✍️",
}
