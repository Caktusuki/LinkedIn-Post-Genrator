import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Using a model ID directly from your active Groq models list
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b"
)

if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are ")
    print(response.content)