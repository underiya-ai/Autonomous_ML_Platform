from langchain_groq import ChatGroq
from dotenv import load_dotenv
from service.profile_extractor import extract_profile_data
from schema.state import DatasetProfileState

load_dotenv()

def generate_summary_agent(state:DatasetProfileState)