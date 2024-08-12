import openai
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from tools import initialize_tools
import os

class CustomAgent:
    def __init__(self, pdf_path):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0, max_tokens=300)
        self.vector_store = self.create_vector_store_from_pdf(pdf_path)
        self.tools = initialize_tools(self.vector_store, self.llm)
        self.agent = initialize_agent(tools=self.tools, llm=self.llm, agent="zero-shot-react-description")

    def create_vector_store_from_pdf(self, pdf_path):
        from utils import extract_text_from_pdf, create_vector_store_from_pdf_text
        text = extract_text_from_pdf(pdf_path)
        return create_vector_store_from_pdf_text(text)

    def get_answers(self, questions):
        answers = {}
        for question in questions:
            answer = self.agent.run(question)
            answers[question] = answer if answer else "Data Not Available"
        return answers
