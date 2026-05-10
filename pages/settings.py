import streamlit as st

def render_settings_page():

    st.title("⚙️ Settings")

    st.toggle("Dark Mode")
    st.toggle("Notifications")

    st.selectbox("Refresh Rate", ["5 sec", "10 sec", "30 sec", "1 min"])

    st.button("Save Settings")
