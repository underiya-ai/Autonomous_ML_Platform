from langchain_groq import ChatGroq
from utils.config import GROQ_API_KEY

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)