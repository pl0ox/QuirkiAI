from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def initialize_model():
    # Define the local directory where you want to store the model
    cache_dir = "./"  # Use "./" for the current directory

    tokenizer = AutoTokenizer.from_pretrained(
        "facebook/blenderbot_small-90M",
        cache_dir=cache_dir  # Set the cache directory
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        "facebook/blenderbot_small-90M",
        cache_dir=cache_dir  # Set the cache directory
    )

    return tokenizer, model

def main():
    tokenizer, model = initialize_model()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye', 'end']:
            print("Chatbot: Goodbye!")
            break

        inputs = tokenizer(user_input, return_tensors="pt")
        result = model.generate(**inputs)
        bot_response = tokenizer.decode(result[0], skip_special_tokens=True)

        print("Chatbot:", bot_response)

if __name__ == "__main__":
    main()