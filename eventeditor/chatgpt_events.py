# chatgpt_events.py
import google.generativeai as genai

# Configure the API key securely, possibly loaded from environment variables or a secure config
api_key = "AIzaSyCcICrkbWH8qV0VAZnRDzsEPNoO2_1U_Ps"
genai.configure(api_key=api_key)

def generate_text(prompt, model_name='gemini-pro'):
    """Generate text from a given prompt using a specified Gemini model."""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

def generate_multimodal(prompt, image_bytes, model_name='gemini-pro-vision'):
    """Generate text using both text and image inputs."""
    model = genai.GenerativeModel(model_name)
    content = [prompt, image_bytes]  # Prepare the image_bytes appropriately
    response = model.generate_content(content)
    return response.text

def start_chat_conversation(initial_prompt, model_name='gemini-pro'):
    """Start a multi-turn conversation."""
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat()
    response = chat.send_message(initial_prompt)
    return response.text, chat

def send_chat_message(chat, message):
    """Send a message in an ongoing chat conversation."""
    response = chat.send_message(message)
    return response.text
