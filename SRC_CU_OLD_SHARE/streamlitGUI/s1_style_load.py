import streamlit as st
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_click_button(url, text, style="button-5"):
    # Create a button with a link to the URL
    button_html = f'<a href="{url}" target="_blank" class="{style}">{text}</a>'
    st.markdown(button_html, unsafe_allow_html=True)