# PDF-QA Agent

This project uses OpenAI's language model and LangChain to create a question-answering system that extracts and analyzes text from a PDF document. It retrieves answers to specific questions based on the content of the provided PDF and posts the results to a Slack channel.

## Project Structure

- **`agent.py`**: Contains the `CustomAgent` class responsible for initializing the language model, vector store, and agent, and getting answers to questions.
- **`tools.py`**: Defines the tools used by the agent, including text retrieval and answer generation.
- **`utils.py`**: Utility functions for extracting text from PDFs, creating a vector store, and generating answers.
- **`main.py`**: Main script to run the PDF processing and post results to Slack.
- **`.env`**: Configuration file for storing API keys and other sensitive information.

## Setup

### Prerequisites

Ensure you have Python 3.7+ installed. You also need to set up an OpenAI account and a Slack workspace.

### Installation

1. Clone the repository:
   bash
   git clone https://github.com/yourusername/pdf-qa-agent.git
   cd pdf-qa-agent

2. Create a virtual environment (optional but recommended):

    bash
    Copy code
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:

    bash
    Copy code
    pip install -r requirements.txt