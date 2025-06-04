import openai
import os
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

def main():
    print("Stock Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Bot: Goodbye!")
            break
        reply = ask_gpt(user_input)
        print("Bot:", reply)

if __name__ == "__main__":
    main()
