from langchain_core.messages import HumanMessage
from config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.4
) 

def generate_summary(summary_data: dict) -> str:
    prompt = f"""
    {summary_data}
    You are a travel guide and alert based system.
    Start with:
    🟢 Good | 🟡 Medium | 🔴 Bad according to travel sitiuation then place a @ after that.
    I want you too give me three para no ** use. Separate each para by a @ symbol. The topic of para 
    should be Situation then Preparation and then Reccommendation.
    Three paras Short Concise dont give heading for para.
    """
   
    return llm.invoke([HumanMessage(content=prompt)]).text


def translate_text(text: str, language: str) -> str:
    """Translate text using LLM."""
    prompt = f"Translate the following text to {language} keeping meaning and emojis. Do not explain:\n{text}"
    return llm.invoke([HumanMessage(content=prompt)]).text
