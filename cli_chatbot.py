import os
import requests
import openai
import csv
import datetime

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
API_TOKEN = os.getenv("STOCK_API_TOKEN")

def ask_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about stock investing."},
            {"role": "user", "content": message}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

def log_question(user_input, context="unanswered"):
    os.makedirs("logs", exist_ok=True)
    with open("logs/unanswered.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, user_input, context])

def get_stock_list():
    url = "https://robo.aas.com.vn/Advisor/getliststock"
    headers = {
        "tradingSessionToken": API_TOKEN,
        "Content-Type": "text/plain"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def handle_user_input(user_input):
    if "list" in user_input.lower() and "stock" in user_input.lower():
        stocks = get_stock_list()
        if "error" in stocks:
            log_question(user_input, context="API error")
            return f"[API Error] {stocks['error']}"
        if not stocks:
            log_question(user_input, context="API returned empty")
            return "No stock data received from the API."
        result = "Here are some stocks:\n"
        for s in stocks[:10]:
            symbol = s.get("symbol", "N/A")
            name = s.get("name", "unknown")
            price = s.get("lastPrice", "—")
            result += f" • {symbol} – {name}: {price}\n"
        return result
    else:
        reply = ask_gpt(user_input).strip()
        if "I don't know" in reply or "I'm not sure" in reply:
            log_question(user_input, context="GPT unsure")
        return reply

def main():
    print("SmartInvest Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Bot: Goodbye!")
            break
        try:
            reply = handle_user_input(user_input)
            print("Bot:", reply)
        except Exception as e:
            print("Bot: Sorry, I encountered an error.")
            print("Error:", str(e))

if __name__ == "__main__":
    main()
