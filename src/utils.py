import os
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_vector_store_from_pdf_text(text):
    text_splitter = CharacterTextSplitter(separator="\n",chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vector_store = Chroma.from_documents(documents, embeddings)
    return vector_store

def retrieve_relevant_text(vector_store, query):
    docs = vector_store.similarity_search(query)
    combined_text = " ".join([doc.page_content for doc in docs])
    return combined_text

def generate_answer(llm, text, question):
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    prompt_template = """
    You are an assistant who provides answers based strictly on the provided text. 
    Answer the following question using only the content of the provided text. 
    Find the intent of user to check if it is about the given context or not.
    Do not make any assumptions, provide additional information, or generate answers not directly supported by the text. 
    If the answer is not in the text or if there is insufficient information, respond with "Data Not Available."

    Example 1:

    Provided Text:
    "John loves playing basketball on weekends. He also enjoys watching basketball games on TV."

    Question:
    "Does John like playing soccer?"

    Answer:
    "Data Not Available."

    Explanation:
    The question about John liking soccer is not addressed in the provided text, which only discusses his interest in basketball.

    Example 2:

    Provided Text:
    "The new library opens at 9 AM and closes at 6 PM on weekdays. On weekends, it operates from 10 AM to 4 PM."

    Question:
    "What are the weekend hours of the new library?"

    Answer:
    "The new library operates from 10 AM to 4 PM on weekends."

    Text: {text}

    Question: {question}

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text", "question"])
    chain = LLMChain(llm=llm, prompt=prompt)
    answer = chain.run({"text": text, "question": question})
    return answer.strip()
