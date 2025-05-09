import streamlit as st
import base64
from Front.UsersLogin import show_login_page
from Front import home, map, explorer, compare, about
from datetime import date

# Initialisation robuste des variables de session
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Accueil"

def add_logo():
    try:
        with open("Code\src\Front\img\logo.png", "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
    except FileNotFoundError:
        return ""

def run_app():
    st.set_page_config(page_title="Stat & More App", layout="wide")

    if not st.session_state["is_logged_in"]:
        show_login_page()
        return
    
    # --- Sidebar avec filtres ---
    st.sidebar.header("Filtres")

    start_date = st.sidebar.date_input("Date de début", value=date(2022, 1, 1))
    end_date = st.sidebar.date_input("Date de fin", value=date(2022, 12, 31))
    st.sidebar.selectbox("Secteur", ["Tous", "Agricole", "Industriel", "Tertiaire", "Résidentiel"])
    st.sidebar.selectbox("Énergie", ["Toutes", "Électricité", "Gaz", "Chaleur/Froid"])
    st.sidebar.selectbox("Zone géographique", ["France entière", "Région", "Département", "IRIS"])


    # --- En-tête avec logo, navigation et déconnexion ---
    logo_data = add_logo()
    cols = st.columns([2, 10, 1, 2])


    with cols[0]:
        st.markdown(
            f"<div style='display: flex; align-items: center;'>"
            f"<img src='data:image/png;base64,{logo_data}' height='40' style='margin-right: 10px;'>"
            f"<h3 style='margin: 0;'>Stat & More</h3></div>",
            unsafe_allow_html=True
        )

    with cols[1]:
        nav_items = ["Accueil", "Carte", "Explorateur", "Comparaison", "À propos"]
        nav_cols = st.columns(len(nav_items))
        for i, label in enumerate(nav_items):
            is_active = st.session_state["current_page"] == label
            button_style = (
                "background-color: #f63366; color: white;"
                if is_active else
                "background-color: transparent; color: black;"
            )
            if nav_cols[i].button(label, key=f"nav_{label}", use_container_width=True, help=label):
                st.session_state["current_page"] = label
            nav_cols[i].markdown(
                f"""
                <style>
                div[data-testid="column"]:nth-of-type({i+1}) button {{
                    {button_style}
                    border: none;
                    padding: 10px 16px;
                    border-radius: 5px;
                    font-weight: bold;
                    cursor: pointer;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    with cols[3]:
        if st.button("Déconnexion", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()

    st.markdown("---")

    # --- Appel de la page sélectionnée ---
    page_map = {
        "Accueil": home.run_page,
        "Carte": map.run_page,
        "Explorateur": explorer.run_page,
        "Comparaison": compare.run_page,
        "À propos": about.run_page,
    }

    page_map[st.session_state["current_page"]]()