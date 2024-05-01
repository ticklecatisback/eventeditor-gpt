# chatgpt_events.py
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow

# Configure the API key securely, possibly loaded from environment variables or a secure config
api_key = "AIzaSyBTN7175fA82A3kn5bzLqAhAuZaDG2wKVs"
genai.configure(api_key=api_key)

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_credentials():
    # Load the client secrets from the file downloaded from the Google Cloud Console
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_144218831046-r3fa4tosi7csjt07iamq6kmomoma5cbv.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)  # This opens a local server to handle the OAuth flow
    return creds


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


if __name__ == "__main__":
    prompt = "Explain the implications of machine learning in healthcare."
    print(generate_text(prompt))