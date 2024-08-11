import os
from dotenv import load_dotenv
from agent import CustomAgent
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json

# Load environment variables from .env file
load_dotenv()

def post_to_slack(answers, slack_token, channel):
    client = WebClient(token=slack_token)
    message = json.dumps(answers, indent=2)
    try:
        client.chat_postMessage(channel=channel, text=f"Question-Answer Results:\n```{message}```")
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")

def main(pdf_path, questions, slack_channel):
    agent = CustomAgent(pdf_path)
    answers = agent.get_answers(questions)
    print("answers.....", answers)
    slack_token = os.getenv("SLACK_API_TOKEN")
    post_to_slack(answers, slack_token, slack_channel)

# Example usage
if __name__ == "__main__":
    pdf_path = "../data/ThomasAlvaEdison.pdf"  # Replace with your PDF file path
    questions = [
        "What is the content about?",
        "What are his key inventions?",
        "Who is antony?"
    ]
    slack_channel = "#ai-chatbots"  # Replace with your Slack channel

    main(pdf_path, questions, slack_channel)
