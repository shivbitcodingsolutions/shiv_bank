import streamlit as st

if "my_text_input_value" not in st.session_state:
    st.session_state.my_text_input_value = ""

def handle_text_change():
    st.session_state.my_text_input_value = st.session_state.text_input_widget

st.title("Streamlit on_change Example")

st.text_input(
    "Enter some text:",
    key="text_input_widget",  
    on_change=handle_text_change
)


st.write(f"Current text from session state: {st.session_state.my_text_input_value}")
