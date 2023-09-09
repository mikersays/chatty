import openai
import sys
import time
import threading
import os
from datetime import datetime
import platform  # To determine the OS

# Use readline for Unix-based systems, pyreadline for Windows
if platform.system() == 'Windows':
    import pyreadline as readline
else:
    import readline

# Set up your API key. Replace the entire <API key> string with your OpenAI API key.
openai.api_key = "<API key>"

# Function to generate a response using GPT-4
def generate_response(prompt, messages, max_tokens=5000, temperature=1):
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        top_p=1,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message['content']})
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
def call_gpt_with_spinner(prompt, messages):
    stop_flag = threading.Event()
    spinner = threading.Thread(target=spinning_cursor, args=(stop_flag,))
    spinner.daemon = True
    spinner.start()

    response = generate_response(prompt, messages)

    stop_flag.set()
    spinner.join()
    sys.stdout.write("\b")
    sys.stdout.flush()

    return response

# Function to get the user's desktop path
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# Function to read the instruction from an external file
def read_instruction_from_file(file_path):
    with open(file_path, "r") as file:
        instruction = file.read().strip()
    return instruction

# Main function to start the chatbot
def chatbot():
    print("Ask me anything! Type 'q' to exit.")
    print("----------------------------------")
    user_input = ""

    # Prepare the output file
    desktop_path = get_desktop_path()
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"chat_output_{current_time}.md"  # Changed the file extension to ".md"
    output_file_path = os.path.join(desktop_path, output_filename)

    system_instruction = read_instruction_from_file("AIpersona.txt")
    messages = [{"role": "system", "content": system_instruction}]
    
    with open(output_file_path, "w") as output_file:
        while user_input.lower() != "q":
            user_input = input("User: ")  # Replace this line

            if user_input.lower() != "q":
                output_file.write(f"User: {user_input}\n\n")  # Added an extra line

                print("AI: ", end=" ", flush=True)  # Modified this line
                response = call_gpt_with_spinner(user_input, messages)
                print(response)

                output_file.write(f"AI: {response}\n\n")  # Added an extra line

    print(f"Chatbot conversation saved to: {output_file_path}")

if __name__ == "__main__":
    chatbot()
