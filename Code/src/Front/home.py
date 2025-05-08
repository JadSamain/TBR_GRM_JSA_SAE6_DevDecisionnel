import streamlit as st
from datetime import date

def run_home():
    logout_clicked = False

    # --- Bandeau haut ---
    with st.container():
        cols = st.columns([4, 6, 2])
        with cols[0]:
            st.markdown("## 📊 Stat & More Dashboard")
        with cols[1]:
            st.radio("Navigation", ["Accueil", "Carte", "Explorateur", "Comparaison", "À propos"],
                     horizontal=True, label_visibility="collapsed")
        with cols[2]:
            logout_clicked = st.button("🔒 Déconnexion")  # On capture le clic ici

    st.markdown("---")

    col1, col2 = st.columns([1, 4])

    with col1:
        st.subheader("Filtres")
        start_date = st.date_input("Date de début", value=date(2022, 1, 1))
        end_date = st.date_input("Date de fin", value=date(2022, 12, 31))
        st.selectbox("Secteur", ["Tous", "Agricole", "Industriel", "Tertiaire", "Résidentiel"])
        st.selectbox("Énergie", ["Toutes", "Électricité", "Gaz", "Chaleur/Froid"])
        st.selectbox("Zone géographique", ["France entière", "Région", "Département", "IRIS"])

    with col2:
        st.markdown("### Bienvenue sur la plateforme de visualisation Stat & More")
        st.info("Veuillez sélectionner des filtres à gauche. Les indicateurs apparaîtront ici.")

    # --- Déconnexion gérée proprement à la fin ---
    if logout_clicked:
        st.session_state["is_logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()
