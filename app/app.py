import streamlit as st
import requests
import re

SERVER_URL = "http://127.0.0.1:8000/chat"

# Import CSS & HTML Files

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def create_sidebar():
    st.sidebar.markdown(
        "<h2 class='stHeading'>Chat History</h2>"
        ,
        unsafe_allow_html=True
    )

    chat_history = [
        "Asking about the main gods in Inca mythology.",
        "Consulting about Quechua grammar.",
        "Discussing Inti, the sun god.",
        "Translating a poem to Quechua.",
        "Stories about Pachamama.",
        "Translating basic sentences.",
        "Words related to Carnaval culture.",
        "Importance of sacred animals."
    ]
    
    for chat in chat_history:
        st.sidebar.markdown(
            f"""
            <div class="chat-item">
                {chat}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.sidebar.button("Upgrade Plan 👉", key="upgrade_button")
        
def chat_message(text, user_icon, align="left"):
    flex_direction = "row" if align == "right" else "row-reverse"
    message_class = "assistant-message" if align == "left" else "user-message"
    margin_side = "margin-left: 15px;" if align == "left" else "margin-right: 15px;"

    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-start; margin-bottom: 10px; flex-direction: {flex_direction};">
            <div class="chat-message {message_class}" style="flex: 1; text-align: left; max-width: 100%;">
                <p>{text}</p>
            </div>
            <img src="{user_icon}" alt="profile" class="profile-pic" style="{margin_side}">
        </div>
        """,
        unsafe_allow_html=True
    )

def show_custom_toast(message):
    st.markdown(
        f"""
        <div class="toast">
            <span style="font-size: 24px; margin-right: 10px;">⚠️</span>
            <span>{message}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def validate_user_input(prompt):

    if not prompt.strip():
        show_custom_toast("Please enter some text to translate.")
        return False
    elif any(char.isdigit() for char in prompt):
        show_custom_toast("Please enter text without numbers.")
        return False
    elif not any(char.isalpha() for char in prompt):
        show_custom_toast("The text must contain letters.")
        return False
    elif len(prompt) <= 2:
        show_custom_toast("The text must contain more than one letter.")
        return False
    elif len(prompt) > 300:
        show_custom_toast("The text cannot exceed 300 characters.")
        return False
    elif len(prompt.split()) <= 1:
        show_custom_toast("The text must contain more than one word.")
        return 
    elif len(set(prompt.split())) <= 3 and len(prompt.split()[0]) == 1:
        show_custom_toast("Please enter more meaningful text.")
        return False
    elif not re.search(r'[aeiouáéíóú]', prompt, re.IGNORECASE):
        show_custom_toast("Please enter more meaningful text.")
        return False
    return True

def send_message_to_server(prompt):
    payload = {"message": prompt}
    try:
        response = requests.post(SERVER_URL, json=payload)
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("response", "Sorry, I didn't understand your request.")
    except requests.exceptions.RequestException:
        show_custom_toast("Connection error. Please check the server and try again.")
    except ValueError:
        show_custom_toast("Error processing the response. The response is not in the expected format.")
    return None


def chat_input():
    prompt = st.chat_input("Say something", key="chat_input")
    if prompt and validate_user_input(prompt):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        assistant_response = send_message_to_server(prompt)
        if assistant_response:
            st.session_state.conversation.append({"role": "assistant", "content": assistant_response})


def display_chat():
    for message in st.session_state.conversation:
        user_icon = user_profile if message["role"] == "user" else assistant_profile
        chat_message(message["content"], user_icon, align="right" if message["role"] == "user" else "left")


assistant_profile = "https://i.pinimg.com/550x/f9/e5/90/f9e590368d01c87a14938ecbb96c97ec.jpg"
user_profile = "https://hips.hearstapps.com/hmg-prod/images/shrek-64f9ceef56099.jpg?crop=0.565xw:1.00xh;0.218xw,0&resize=1200:*"

def main():
    st.title("Llama Quechua")

    css_content = load_file('styles.css')
    html_content = load_file('app.html')

    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

    create_sidebar()

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    chat_input()
    display_chat()

    st.html(f'{html_content}')


if __name__ == "__main__":
    main()