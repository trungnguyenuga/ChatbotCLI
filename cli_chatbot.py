import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about stock investing."},
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content']

def load_faq(path="data/faq.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

faq_data = load_faq()

def check_static_answer(user_input):
    q = user_input.lower().strip()
    for pair in faq_data:
        if q in pair['question']:
            return pair['answer']
    return None

def main():
    print("Stock Chatbot (type 'exit' to quit)")
    faq_data = load_faq()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Bot: Goodbye!")
            break

        static_reply = check_static_answer(user_input)
        if static_reply:
            print("Bot:", static_reply)
            continue

        try:
            reply = ask_gpt(user_input)
            print("Bot:", reply)
        except Exception as e:
            print("Bot: Sorry, there was an error processing your request.")
            print("Error:", str(e))


if __name__ == "__main__":
    main()
