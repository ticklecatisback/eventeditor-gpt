import os
import google.generativeai as genai

# Load the API key from an environment variable
api_key = os.getenv('AIzaSyCcICrkbWH8qV0VAZnRDzsEPNoO2_1U_Ps')

genai.configure(api_key=api_key)


def generate_text(prompt, model_name='gemini-pro'):
    """
    Generate text from a given prompt using a specified Gemini model.

    Args:
        prompt (str): The prompt to send to the model.
        model_name (str): The name of the Gemini model to use.

    Returns:
        str: The generated text from the model.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Failed to generate text: {str(e)}")
        return None


def generate_multimodal(prompt, image_bytes, model_name='gemini-pro-vision'):
    """
    Generate text using both text and image inputs.

    Args:
        prompt (str): The text part of the input.
        image_bytes (bytes): The image data in bytes.
        model_name (str): The name of the Gemini model to use for multimodal inputs.

    Returns:
        str: The generated text from the model.
    """
    try:
        model = genai.GenerativeModel(model_name)
        content = [prompt, image_bytes]  # Prepare the image_bytes appropriately
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        print(f"Failed to generate multimodal text: {str(e)}")
        return None


def start_chat_conversation(initial_prompt, model_name='gemini-pro'):
    """
    Start a multi-turn conversation.

    Args:
        initial_prompt (str): The initial message to start the conversation.
        model_name (str): The name of the Gemini model to use for the chat.

    Returns:
        tuple: The first response text and the chat session object.
    """
    try:
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat()
        response = chat.send_message(initial_prompt)
        return response.text, chat
    except Exception as e:
        print(f"Failed to start chat conversation: {str(e)}")
        return None, None


def send_chat_message(chat, message):
    """
    Send a message in an ongoing chat conversation.

    Args:
        chat (Chat): The chat session object.
        message (str): The message to send.

    Returns:
        str: The response text from the chat.
    """
    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        print(f"Failed to send chat message: {str(e)}")
        return None

