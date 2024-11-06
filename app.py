import streamlit as st
def great(text):
    st.write(f"Hello {text}")
def app():
    st.title('Welcome to HolidayMatch')
    st.write('Your AI-powered travel assistant!')
    st.write('Stay tuned for updates...')
    great("Alina")

if __name__ == '__main__':
    app()
