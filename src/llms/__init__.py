from .load_model import load_model_groq, load_model_openai, load_model_ollama
MODEL_TABLE = {
    "groq": load_model_groq,
    "openai": load_model_openai,
    "ollama": load_model_ollama
}