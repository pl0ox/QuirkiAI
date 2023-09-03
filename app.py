import torch
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration,AutoTokenizer,AutoModelForSeq2SeqLM
import threading
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
initialized = False  # Flag to track whether the chatbot has been initialized
tokenizer, model = None, None  # Initialize tokenizer and model variables

def initialize_model():
    global tokenizer, model, initialized
    if not initialized:  # Check if the chatbot is already initialized
        tokenizer_path = "./model/snapshots/trained1/"
        model_path = "./model/snapshots/trained1/"
        cache_dir = "./"
        try:
            tokenizer = AutoTokenizer.from_pretrained(
            "facebook/blenderbot_small-90M",
            cache_dir=cache_dir  # Set the cache directory
    )
            model = AutoModelForSeq2SeqLM.from_pretrained(
            "facebook/blenderbot_small-90M",
            cache_dir=cache_dir  # Set the cache directory
    )
            initialized = True  # Set the flag to True
        except Exception as e:
            print(f"Error initializing the model: {str(e)}")
            tokenizer, model = None, None

def chatbot_response(user_input):
    global tokenizer, model
    if tokenizer is not None and model is not None:
        inputs = tokenizer(user_input, return_tensors="pt")
        result = model.generate(**inputs)
        bot_response = tokenizer.decode(result[0], skip_special_tokens=True)
        return bot_response
    else:
        return "Chatbot is still initializing..."
    
@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    global tokenizer, model

    user_input = request.form['user_input']
    bot_response = chatbot_response(user_input) 
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    initialize_model()
    app.run(debug=False)