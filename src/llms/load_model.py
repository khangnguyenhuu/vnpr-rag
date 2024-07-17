
import os
from src.constants import cfg

def load_model_groq(model_id):
    from llama_index.llms.groq import Groq
    return Groq(model=model_id, temperature=cfg.LLM_MODEL.TEMPERATURE, sequence_length=cfg.LLM_MODEL.MAX_TOKENS, top_p=0.5, api_key=os.getenv("GROQ_API_KEY"))

def load_model_openai(model_id):
    from llama_index.llms.openai import OpenAI
    return OpenAI(model=model_id, temperature=cfg.LLM_MODEL.TEMPERATURE, api_key=os.getenv("OPENAI_API_KEY"))

def load_model_ollama(model_id):
    from llama_index.llms.ollama import Ollama
    return Ollama(model=model_id, temperature=cfg.LLM_MODEL.TEMPERATURE, base_url='http://localhost:11434')