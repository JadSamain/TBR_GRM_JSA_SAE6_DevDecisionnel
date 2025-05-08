# app.py
import streamlit as st
from UsersLogin import show_login_page
from home import run_home

# Initialisation des variables de session
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

def run_app():
    st.set_page_config(page_title="Stat & More App", layout="wide")

    if not st.session_state["is_logged_in"]:
        show_login_page()
    else:
        run_home()