# main.py
import chatgpt_events as cge

# Example of generating text
prompt = "Describe the historical significance of the Eiffel Tower."
print(cge.generate_text(prompt))

# Example of starting a chat conversation
initial_prompt = "Hello, can you help me understand quantum physics?"
text_response, chat_session = cge.start_chat_conversation(initial_prompt)
print(text_response)

# Continuing the conversation
follow_up = "What is the Heisenberg Uncertainty Principle?"
print(cge.send_chat_message(chat_session, follow_up))
