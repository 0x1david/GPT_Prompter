import openai
import tkinter as tk
from tkinter import ttk
from openai import ChatCompletion

# Save the API key
def save_api_key():
    api_key = api_key_entry.get()
    if api_key:
        openai.api_key = api_key
        if save_key_var.get():
            with open("api_key.txt", "w") as f:
                f.write(api_key)
        show_prompt_tab()

# Load the API key
def load_api_key():
    try:
        with open("api_key.txt", "r") as f:
            api_key = f.read().strip()
            openai.api_key = api_key
            return api_key
    except FileNotFoundError:
        return ""

# Show the prompt tab
def show_prompt_tab():
    api_key_frame.grid_remove()
    prompt_frame.grid(row=0, column=0, sticky="nsew")

# Show the API key tab
def show_api_key_tab():
    prompt_frame.grid_remove()
    api_key_frame.grid(row=0, column=0, sticky="nsew")

# Get restructured prompt
def get_restructured_prompt(prompt):
    messages = [{"role": "user", "content": f"Please rephrase the following text into a prompt that is clear, concise, and well-formatted for an AI language model to understand and process effectively: <{prompt}>"}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message["content"].strip()

# Get completion
def get_completion(prompt, gpt_ver):
    print(gpt_ver)
    messages = [{"role": "user", "content": prompt}]
    response = ChatCompletion.create(
        model="gpt-4" if gpt_ver.get() else 'gpt-3.5-turbo',
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

# Submit prompt and display the result
def submit_prompt(gpt_ver, reprompt):
    print(gpt_ver)
    first_prompt = prompt_entry.get("1.0", tk.END).strip()
    if first_prompt:
        if reprompt.get():
            second_prompt = get_restructured_prompt(first_prompt)
            sp_label.config(text=f"Second Prompt:")
            sp_entry.delete("1.0", tk.END)
            sp_entry.insert(tk.END, second_prompt)
            response = get_completion(second_prompt, gpt_ver)
        else:
            response = get_completion(first_prompt, gpt_ver)
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, response)

# Init Window
root = tk.Tk()
root.title("ChatGPT App")
root.geometry("1200x900")

# Create the API Key Frame
api_key_frame = ttk.Frame(root, padding="30 30 30 30")
api_key_frame.grid(row=0, column=0, sticky="nsew")
prompt_frame = ttk.Frame(root, padding="30 30 30 30")

# Add Widgets to the API Key Frame
api_key_label = ttk.Label(api_key_frame, text="Enter your OpenAI API Key:")
api_key_label.grid(row=0, column=0, padx=(0, 10))
api_key_entry = ttk.Entry(api_key_frame, width=50)
api_key_entry.grid(row=0, column=1)
api_key_entry.insert(0, load_api_key())

# Create Tick Button for Saving API Key
save_key_var = tk.BooleanVar()
save_key_checkbutton = ttk.Checkbutton(api_key_frame, text="Save API key", variable=save_key_var)
save_key_checkbutton.grid(row=1, columnspan=2, pady=(10, 0))

# Submit Key Button
api_key_submit_button = ttk.Button(api_key_frame, text="Continue", command=save_api_key)
api_key_submit_button.grid(row=2, columnspan=2, pady=(10, 0))

# Primary Prompt Insert Window
prompt_label = ttk.Label(prompt_frame, text="Enter your prompt:")
prompt_label.grid(row=0, column=0, sticky="w")
prompt_entry = tk.Text(prompt_frame, wrap="word", height=10, width=50)
prompt_entry.grid(row=1, column=0, pady=(10, 0), sticky='nsew')

# Secondary Prompt Display Window
sp_label = ttk.Label(prompt_frame, text="Generated Prompt:")
sp_label.grid(row=2, column=0, pady=(10, 0), sticky="w")
sp_entry = tk.Text(prompt_frame, wrap="word", height=20, width=50)
sp_entry.grid(row=3, rowspan=1, column=0, pady=(10, 0), sticky="nsew")

# Response Display Window
response_label = ttk.Label(prompt_frame, text="Generated response:")
response_label.grid(row=0, column=1, padx=(30, 0), sticky="w")
response_text = tk.Text(prompt_frame, wrap="word", height=12, width=50)
response_text.grid(row=1, column=1, rowspan=3, padx=(30, 0), pady=(10, 0), sticky="nsew")

# Create Tick Button for Changing GPT Model
gpt_version = tk.BooleanVar()
save_key_checkbutton = ttk.Checkbutton(prompt_frame, text="GPT-4", variable=gpt_version)
save_key_checkbutton.grid(row=5, column=5, pady=(10, 0))

# Create Tick Button for Re-Prompting
reprompt = tk.BooleanVar()
save_key_checkbutton = ttk.Checkbutton(prompt_frame, text="Re-Prompt", variable=reprompt)
save_key_checkbutton.grid(row=4, column=5, pady=(10, 0))

# Button to Submit the prompts
submit_button = ttk.Button(prompt_frame, text="Submit", command=lambda: submit_prompt(gpt_ver=gpt_version, reprompt=reprompt))
submit_button.grid(row=4, column=0, pady=(10, 0))

# Button to Change the API Key
change_api_key_button = ttk.Button(prompt_frame, text="Change API Key", command=show_api_key_tab)
change_api_key_button.grid(row=4, column=1, columnspan=2, pady=(10, 0))

# Configure Window Layout
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Configure Prompt Frame Layout
prompt_frame.columnconfigure(0, weight=1)
prompt_frame.columnconfigure(1, weight=1)
prompt_frame.rowconfigure(1, weight=1)

# Start Main Loop
root.mainloop()


