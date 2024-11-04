import streamlit as st
import requests

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
        "Discussing Inti, the sun god.",
        "Consulting about Quechua grammar.",
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
        <div style="display: flex; align-items: center; margin-bottom: 10px; flex-direction: {flex_direction};">
            <div class="chat-message {message_class}" style="display: inline-block; flex: 1; text-align: left;">
                <p>{text}</p>
            </div>
            <img src="{user_icon}" alt="profile" class="profile-pic"; {margin_side}">
        </div>
        """,
        unsafe_allow_html=True
    )
    

def chat_input():
    # Hacer Validaciones del input
    if prompt := st.chat_input("Say something", key="chat_input"):
        st.session_state.conversation.append({"role": "user", "content": prompt})

        print("PROMPT: ", prompt)
        payload = {
        "message": prompt,
        }

        response = f'echo: {prompt}'
        st.session_state.conversation.append({"role": "assistant", "content": response})

        # Send a POST request to the server
        # response = requests.post(SERVER_URL,json=payload)
        # print("RESPONSE: ", response)
        # print("JSON: ",  response.json())
        # st.session_state.conversation.append({"role": "assistant", "content": response.json().get("response")})

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

    # Sidebar
    create_sidebar()

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    chat_input()
    display_chat()

    st.html(f'{html_content}')


if __name__ == "__main__":
    main()