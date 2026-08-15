from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config import GROQ_API_KEY,GOOGLE_API_KEY

Groq_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)

Gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=GOOGLE_API_KEY
    )