import streamlit as st
from Front.UsersLogin import show_login_page  # Correction de l'import

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.write(f"🎉 Bienvenue, {st.session_state.username} ! (Zone post-authentification à venir...)")
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
