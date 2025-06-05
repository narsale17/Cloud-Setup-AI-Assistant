from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import google.generativeai as genai
import os

# Initialize the Flask app and set up folders
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = '123456778'

# Configure the Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyAg_2eibUL8r7qODzAqTHYJVqhW3g23kCI"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.0-flash")
chat = model.start_chat()

# Define configuration templates for various GCP services
TEMPLATES = {
    "host_website": {"fields": ["region", "storage_type", "machine_type", "domain"]},
    "create_vm": {"fields": ["region", "zone", "machine_type", "boot_disk"]},
    "deploy_container": {"fields": ["region", "container_image", "memory", "cpu"]},
    "setup_database": {"fields": ["database_type", "region", "storage_size"]}
}

# Route to reset user session
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    return jsonify({"message": "Session cleared"})

# Store user's name and experience level in session
@app.route("/store_user_info", methods=["POST"])
def store_user_info():
    session.clear()  # 🔁 full reset
    data = request.get_json()
    session['name'] = data.get('name')
    session['experience'] = data.get('experience')
    return jsonify({'message': 'User info stored successfully'})

# Detect user intent based on input text
def detect_intent(user_input):
    user_input = user_input.lower()
    if "website" in user_input:
        return "host_website"
    elif "vm" in user_input or "compute engine" in user_input:
        return "create_vm"
    elif "container" in user_input or "cloud run" in user_input:
        return "deploy_container"
    elif "sql" in user_input or "database" in user_input:
        return "setup_database"
    return None

# Route for landing page
@app.route("/")
def index():
    return render_template("index.html")

# Main chatbot route to handle conversation logic
@app.route("/chat", methods=["POST"])
def chat_handler():
    user_input = request.get_json().get("message")
    experience = session.get("experience", "Beginner")
    name = session.get("name", "User")

    # If intent is not set yet, detect and initialize flow
    if "intent" not in session:
        intent = detect_intent(user_input)
        if not intent:
            return jsonify({"sify": f"Sorry {name}, I didn't understand that. Please specify what you want to set up on GCP."})

        # Set up initial session variables for flow
        session["intent"] = intent
        session["fields"] = {}
        session["current_index"] = 0
        session["last_question"] = ""
        session["awaiting_answer"] = True

        fields = TEMPLATES[intent]["fields"]
        first_field = fields[0]

        # Ask first question based on experience level
        prompt = f"""
You are a helpful GCP setup assistant named SIFY guiding {name} to configure '{intent.replace('_', ' ')}'.
The user's experience level is: {experience}.

Your goal is to ask a single, clear, and concise question about the configuration parameter: '{first_field}'.

Consider the user's experience level when phrasing the question:

- Beginner: Use simple language, briefly explain the concept if necessary, and provide one concrete example in parentheses if applicable. Start with phrases like "To set up your...", "What kind of...", or "For your...".
- Intermediate: Use standard GCP terminology, provide a brief explanation if a term might be ambiguous, and offer a few common options as examples in parentheses. Start with phrases like "Specify the...", "Choose a...", or "What is the...".
- Expert: Use direct GCP terminology without explanations or examples. Phrase the question as a clear request for a specific value. Start with phrases like "Enter the...", "Select the...", or "Provide the...".

Now, ask the question for '{first_field}'.
"""
        question = chat.send_message(prompt).text.strip()
        session["last_question"] = question
        return jsonify({"sify": f"Got it, {name}! Let's configure your {intent.replace('_', ' ')}.\n\n{question}"})

    # Continue flow if intent already detected
    intent = session["intent"]
    fields = TEMPLATES[intent]["fields"]
    current_index = session.get("current_index", 0)
    last_question = session.get("last_question", "")
    awaiting_answer = session.get("awaiting_answer", True)
    
    # Check if user's input is a question or clarification request
    # Words that likely indicate the user is asking a question rather than providing an answer
    question_indicators = ["what", "which", "how", "can", "could", "would", "should", "will", "?", "recommend", "suggest", "help"]
    likely_question = any(indicator in user_input.lower() for indicator in question_indicators)
    
    if awaiting_answer and likely_question and current_index < len(fields):
        # User seems to be asking for clarification rather than answering
        current_field = fields[current_index]
        
        # Prepare context from previously collected fields
        previous_fields_context = ""
        if session["fields"]:
            previous_fields_context = "Previously collected information:\n"
            for field, value in session["fields"].items():
                previous_fields_context += f"- {field}: {value}\n"
        
        # Generate a response to the user's question before continuing
        # Handle user's clarification request
        clarification_prompt = f"""
You are a helpful GCP setup assistant named SIFY guiding {name} to configure '{intent.replace('_', ' ')}'.
The user's experience level is: {experience}.

{previous_fields_context}

You previously asked about '{current_field}' with this question: "{last_question}"

The user has responded with what appears to be a question rather than an answer: "{user_input}"

First, provide a helpful, informative answer to the user's question or clarification request about '{current_field}'.
Then, repeat your question about '{current_field}' in a way that makes it clear what information you need.

Remember to:
1. Answer their question completely first
2. Then ask for the specific information you need about '{current_field}'
3. If they mentioned a potential answer in their question (like a city name when asking about region), acknowledge it and confirm if that's their choice

The user's experience level is: {experience}.
"""
        response = chat.send_message(clarification_prompt).text.strip()
        return jsonify({"sify": response})
        
    # Process regular answer flow
    if current_index < len(fields):
        # Store the user's answer to the current question
        current_field = fields[current_index]
        session["fields"][current_field] = user_input
        session["current_index"] = current_index + 1

    # Check if we've collected all fields
    if session["current_index"] >= len(fields):
        # All fields have been collected, present summary
        summary = "\n".join([f"- {k}: {v}" for k, v in session["fields"].items()])
        return jsonify({
            "sify": f"✅ Configuration Complete for {intent.replace('_', ' ')}!\n\n🔧 Final Setup:\n{summary}\n\nHow would you like to proceed, {name}?\n1️⃣ GUI Steps\n2️⃣ CLI Commands\n3️⃣ Auto-Configure?",
            "complete": True
        })

    # Get the next field to ask about
    next_field = fields[session["current_index"]]

    # Prepare context from previously collected fields
    previous_fields_context = ""
    if session["fields"]:
        previous_fields_context = "Previously collected information:\n"
        for field, value in session["fields"].items():
            previous_fields_context += f"- {field}: {value}\n"

    # Create prompt for next question, including context from previous answers
    prompt = f"""
You are a helpful GCP setup assistant named SIFY guiding {name} to configure '{intent.replace('_', ' ')}'.
The user's experience level is: {experience}.

{previous_fields_context}

Your goal is to ask a single, clear, and concise question about the configuration parameter: '{next_field}'.

When relevant, reference the user's previous choices to provide context-aware recommendations or constraints.

Consider the user's experience level when phrasing the question:

- Beginner: Use simple language, briefly explain the concept if necessary, and provide one concrete example in parentheses if applicable. Start with phrases like "To set up your...", "What kind of...", or "For your...".
- Intermediate: Use standard GCP terminology, provide a brief explanation if a term might be ambiguous, and offer a few common options as examples in parentheses. Start with phrases like "Specify the...", "Choose a...", or "What is the...".
- Expert: Use direct GCP terminology without explanations or examples. Phrase the question as a clear request for a specific value. Start with phrases like "Enter the...", "Select the...", or "Provide the...".

Now, ask the question for '{next_field}', considering the previously collected information.
"""
    question = chat.send_message(prompt).text.strip()
    session["last_question"] = question
    session["awaiting_answer"] = True
    return jsonify({"sify": question})

# Final route to provide instructions (GUI, CLI, or Auto)
@app.route("/final_action", methods=["POST"])
def final_action():
    data = request.get_json()
    user_choice = data.get("choice", "").strip().lower()

    # Ensure session has valid config
    if "fields" not in session or "intent" not in session:
        return jsonify({"sify": "⚠ Your session expired. Please restart the chat."})

    config = session["fields"]
    intent = session["intent"]
    experience = session.get("experience", "Beginner")
    name = session.get("name", "User")

    # Generate setup steps based on user's preferred method
    prompt = f"""
You are a GCP expert named SIFY providing setup instructions for {name} with the following configuration:

Service: {intent.replace('_', ' ')}
User Experience: {experience}
Configuration Details:
{chr(10).join([f"- {k}: {v}" for k, v in config.items()])}

The user has chosen to receive: {user_choice.upper()} instructions.

Generate the specific steps or commands for setting up this configuration on GCP using the {user_choice.upper()} method.

Consider the user's experience level when generating the output:

- Beginner: Provide very detailed, step-by-step instructions for the GUI, explaining where to click and what to enter. For CLI, provide the exact commands with explanations of each part. For Auto, explain the purpose of the script.
- Intermediate: Provide concise GUI steps using GCP Console terminology. For CLI, provide the commands with a brief explanation of key parameters. For Auto, provide a well-commented script.
- Expert: Provide the direct GUI navigation path (e.g., Compute Engine > VM instances > Create). For CLI, provide the exact commands without explanations. For Auto, provide the script without extensive comments.

Ensure the generated output is directly usable by the user.
"""
    output = chat.send_message(prompt).text.strip()
    return jsonify({
        "type": user_choice,
        "output": output
    })

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)