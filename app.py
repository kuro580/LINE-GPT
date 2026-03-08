from flask import Flask, request
import requests
from openai import OpenAI

app = Flask(__name__)

LINE_TOKEN = "ここにLINEアクセストークン"
OPENAI_API_KEY = "ここにOPENAIキー"

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.json
    events = body["events"]

    for event in events:

        if event["type"] == "message":

            user_text = event["message"]["text"]
            reply_token = event["replyToken"]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": user_text}
                ]
            )

            answer = response.choices[0].message.content

            headers = {
                "Authorization": "Bearer " + LINE_TOKEN,
                "Content-Type": "application/json"
            }

            data = {
                "replyToken": reply_token,
                "messages":[
                    {"type":"text","text":answer}
                ]
            }

            requests.post(
                "https://api.line.me/v2/bot/message/reply",
                headers=headers,
                json=data
            )

    return "OK"

app.run(host="0.0.0.0", port=10000)
