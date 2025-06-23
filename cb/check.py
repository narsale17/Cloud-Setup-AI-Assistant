# to check the list of gen ai models by google available, and to choose as we require

import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyAg_2eibUL8r7qODzAqTHYJVqhW3g23kCI")

# List all available models
models = genai.list_models()
for model in models:
    print(f"Model Name: {model.name}")
