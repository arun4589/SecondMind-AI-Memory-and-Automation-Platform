from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from schema import MemoryDecision
from dotenv import load_dotenv

load_dotenv()


llm1 = ChatGoogleGenerativeAI(model='gemini-3.5-flash')
llm = ChatOllama(model='qwen3:1.7b',think=False)
embed = OllamaEmbeddings(model ='nomic-embed-text')
memory_extractor = llm.with_structured_output(MemoryDecision)