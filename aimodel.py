from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from schema import MemoryDecision
from dotenv import load_dotenv

load_dotenv()


llm1 = ChatGoogleGenerativeAI(model='gemini-3.5-flash')
embed1 = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001',output_dimensionality=768)
llm = ChatOllama(model='qwen3:1.7b',think=False)
embed = OllamaEmbeddings(model ='nomic-embed-text')
memory_extractor = llm.with_structured_output(MemoryDecision)