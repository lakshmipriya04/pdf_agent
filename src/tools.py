from langchain.agents import Tool
from utils import retrieve_relevant_text, generate_answer

def initialize_tools(vector_store, llm):
    tools = [
        Tool(
            name="VectorStoreSearcher",
            func=lambda query: retrieve_relevant_text(vector_store, query),
            description="Searches for relevant text in the vector store based on a query"
        ),
        Tool(
            name="AnswerGenerator",
            func=lambda query: generate_answer(llm, retrieve_relevant_text(vector_store, query), query),
            description="Generates an answer to a question based on the provided text"
        ),
    ]
    return tools
