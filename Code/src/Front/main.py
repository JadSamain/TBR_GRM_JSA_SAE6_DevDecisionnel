import streamlit as st
import sqlite3
import bcrypt
import os

# Définir le chemin de la base de données dans le dossier souhaité
DB_PATH = os.path.join("Code", "src", "Back", "db", "users.sqlite")

# Initialisation de la base de données
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ajouter un utilisateur
def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Nom d'utilisateur déjà existant
    finally:
        conn.close()

# Vérifier les identifiants
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_pw = result[0]
        return bcrypt.checkpw(password.encode(), stored_pw)
    return False

# Application principale
def main():
    st.title("Application sécurisée avec SQLite 🔐")
    init_db()  # Assure que la table est créée

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'menu' not in st.session_state:
        st.session_state.menu = "Connexion"

    # Interface sans barre latérale
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Connexion"):
            st.session_state.menu = "Connexion"
    with col2:
        if st.button("Créer un compte"):
            st.session_state.menu = "Créer un compte"

    if st.session_state.menu == "Créer un compte":
        st.subheader("Créer un compte")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password")

        if st.button("S'inscrire"):
            if password != confirm_password:
                st.error("Les mots de passe ne correspondent pas.")
            elif add_user(username, password):
                st.success("Compte créé avec succès ! Vous pouvez vous connecter.")
                st.session_state.menu = "Connexion"
                st.rerun()
            else:
                st.error("Nom d'utilisateur déjà utilisé.")

    elif st.session_state.menu == "Connexion":
        st.subheader("Connexion")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Bienvenue {username} !")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

    if st.session_state.logged_in:
        st.write(f"🎉 Bienvenue, {st.session_state.username} ! Voici le contenu protégé.")
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
