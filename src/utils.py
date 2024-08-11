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
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
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
    Answer the following question based solely on the content of the provided text.
    Do not make any assumptions or provide information not found in the text.
    If the answer is not in the text or you cannot find sufficient information, respond with "Data Not Available".

    Text: {text}

    Question: {question}

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text", "question"])
    chain = LLMChain(llm=llm, prompt=prompt)
    answer = chain.run({"text": text, "question": question})
    return answer.strip()
