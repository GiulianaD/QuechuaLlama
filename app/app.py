import streamlit as st

# Import CSS & HTML Files

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

css_content = load_file('styles.css')
html_content = load_file('app.html')

st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

st.html(f'{html_content}')

