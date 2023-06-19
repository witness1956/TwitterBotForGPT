import os
import tweepy
from flask import Flask, request, jsonify
from langchainagent import langchain_agent

API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

app = Flask(__name__)

client = tweepy.Client(
    consumer_key = API_KEY,
    consumer_secret = API_KEY_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET
)

@app.route('/')
def create_tweet():
    result = langchain_agent("今日の天気は?")
    response = client.create_tweet(text = result)
    return jsonify({"status": "Tweet created", "tweet_id": response.id}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))