import openai
import sys
import time
import threading
import os
from datetime import datetime

# Set up your API key. Replace the entire <API token> string with your API token.
openai.api_key = "<API token>"

# Function to generate a response using GPT-4
def generate_response(prompt, max_tokens=1500, temperature=1):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace this with a valid GPT-4 model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        top_p=1,
    )
    return response.choices[0].message['content']

# Function to display a spinning loading animation
def spinning_cursor(stop_flag):
    while not stop_flag.is_set():
        for cursor in "|/-\\":
            sys.stdout.write(cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")

# Function to call GPT-4 API with a loading animation
def call_gpt_with_spinner(prompt):
    stop_flag = threading.Event()
    spinner = threading.Thread(target=spinning_cursor, args=(stop_flag,))
    spinner.daemon = True
    spinner.start()

    response = generate_response(prompt)

    stop_flag.set()
    spinner.join()
    sys.stdout.write("\b")
    sys.stdout.flush()

    return response

# Function to get the user's desktop path
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# Main function to start the chatbot
def chatbot():
    print("Welcome to the GPT-4 Chatbot! Type 'quit' to exit.")
    user_input = ""

    # Prepare the output file
    desktop_path = get_desktop_path()
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"chat_output_{current_time}.txt"
    output_file_path = os.path.join(desktop_path, output_filename)

    with open(output_file_path, "w") as output_file:
        while user_input.lower() != "quit":
            user_input = input("User: ")

            if user_input.lower() != "quit":
                output_file.write(f"User: {user_input}\n")

                print("AI: ", end="", flush=True)
                response = call_gpt_with_spinner(user_input)
                print(response)

                output_file.write(f"AI: {response}\n")

    print(f"Chatbot conversation saved to: {output_file_path}")

if __name__ == "__main__":
    chatbot()