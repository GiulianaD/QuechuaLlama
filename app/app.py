import streamlit as st
    
# Import CSS & HTML Files

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def create_sidebar():
    st.sidebar.markdown(
        "<h2 class='stHeading'>Chat History</h2>",
        unsafe_allow_html=True
    )

    chat_history = [
    "Conversation about project management tips",
    "Discussing AI advancements in healthcare",
    "Ideas for content marketing strategy",
    "Brainstorming product features"
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
def chat_message(text, user_icon, align="left"):
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <img src="{user_icon}" alt="profile" class="profile-pic";">
            <div class="chat-message {'user-message' if align == 'left' else 'assistant-message'}" style="flex: 1;">
                <p>{text}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def chat_input():
    if prompt := st.chat_input("Say something", key="chat_input"):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        response = f"Echo: {prompt}"
        st.session_state.conversation.append({"role": "assistant", "content": response})

def display_chat():
    for message in st.session_state.conversation:
        user_icon = user_profile if message["role"] == "user" else assistant_profile
        chat_message(message["content"], user_icon, align="left" if message["role"] == "user" else "right")


user_profile = "https://i.pinimg.com/550x/f9/e5/90/f9e590368d01c87a14938ecbb96c97ec.jpg"
assistant_profile = "https://hips.hearstapps.com/hmg-prod/images/shrek-64f9ceef56099.jpg?crop=0.565xw:1.00xh;0.218xw,0&resize=1200:*"

def main():
    st.title("Chat App")

    css_content = load_file('styles.css')
    html_content = load_file('app.html')

    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

    # Sidebar
    create_sidebar()
    st.sidebar.button("Upgrade Plan 👉", key="upgrade_button")

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    chat_input()
    display_chat()

    st.html(f'{html_content}')


if __name__ == "__main__":
    main()