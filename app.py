from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json


def save_history():
	file = open("history.json", 'w')
	json.dump(conversation_history, file) 

def load_history():
	if (os.path.exists('history.json')):
		try:
			file = open('history.json','r')
			return json.load(file)
		except:
			return []
	else:
		return []

app = Flask(__name__)
conversation_history = load_history()

@app.route("/")
def home():
	return render_template("index.html")


@app.route('/chat', methods= ["POST"])
def chat():
	client = Anthropic()
	print("API KEY:", os.environ.get("ANTHROPIC_API_KEY"))
	user_message = request.json['message']
	conversation_history.append({

		"role": "user",
		"content": user_message
	})
	response = client.messages.create(

	model= "claude-haiku-4-5-20251001",
	max_tokens = 1024,
	system = "you are a AI Engineer and now you are making me one like you show me step by step procedures following with examples and some question to solve",
	messages = conversation_history[-20:]

	)
	assistant_message = response.content[0].text

	conversation_history.append({
    		"role": "assistant",
    		"content": assistant_message
	})

	save_history()
	return jsonify({"response": assistant_message})	

@app.route('/clear', methods=['POST'])
def clear():
	global conversation_history
	conversation_history = []
	save_history()
	return jsonify({"response": "Chat cleared successfully"})

	
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)