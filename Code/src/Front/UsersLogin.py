# * Importer les bibliothèques nécessaires *
import streamlit as st
import sqlite3
import bcrypt
import os
import time
import re  # Pour la validation du mot de passe

# * Définir le chemin de la base de données dans le dossier souhaité *
DB_PATH = os.path.join("Code", "src", "Back", "db", "users.sqlite")

# * Initialisation de la base de données *
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

# * Ajouter un utilisateur *
def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# * Vérifier les identifiants *
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

# * Vérifier la validité du mot de passe *
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# * Réinitialiser les champs de saisie *
def reset_fields():
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.confirm_password = ""

# * Application principale *
def main():
    st.title("Application sécurisée avec SQLite 🔐")
    init_db()

    # Initialisation des états
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'menu' not in st.session_state:
        st.session_state.menu = "Connexion"
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'password' not in st.session_state:
        st.session_state.password = ""
    if 'confirm_password' not in st.session_state:
        st.session_state.confirm_password = ""

    # * Interface création de compte *
    if st.session_state.menu == "Créer un compte":
        st.subheader("Créer un compte")
        username = st.text_input("Nom d'utilisateur", value=st.session_state.username, key="username_create")
        password = st.text_input("Mot de passe", type="password", value=st.session_state.password, key="password_create")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", value=st.session_state.confirm_password, key="confirm_password_create")

        # Gestion des actions après clic
        inscription_clicked = False

        col_spacer, col1, col2 = st.columns([4, 1, 2])
        with col1:
            if st.button("S'inscrire"):
                inscription_clicked = True
        with col2:
            if st.button("Déjà un compte ?"):
                st.session_state.menu = "Connexion"
                reset_fields()
                st.rerun()

        # Affichage des messages en dehors des colonnes
        if inscription_clicked:
            if password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas.")
            elif not is_valid_password(password):
                st.error("❗ Le mot de passe doit contenir au moins 8 caractères, un chiffre et un caractère spécial.")
            elif add_user(username, password):
                st.success("✅ Compte créé avec succès ! Redirection vers la connexion...⏳")
                time.sleep(2)
                st.session_state.menu = "Connexion"
                reset_fields()
                st.rerun()
            else:
                st.error("❌ Nom d'utilisateur déjà utilisé.")

    # * Interface connexion *
    elif st.session_state.menu == "Connexion":
        st.subheader("Connexion")
        username = st.text_input("Nom d'utilisateur", value=st.session_state.username, key="username_login")
        password = st.text_input("Mot de passe", type="password", value=st.session_state.password, key="password_login")

        login_clicked = False

        col_spacer, col1, col2 = st.columns([3, 1, 1])
        with col1:
            if st.button("Se connecter"):
                login_clicked = True
        with col2:
            if st.button("Créer un compte !"):
                st.session_state.menu = "Créer un compte"
                reset_fields()
                st.rerun()

        if login_clicked:
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Bienvenue {username} !")
            else:
                st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")

    # * Interface utilisateur connecté *
    if st.session_state.logged_in:
        st.write(f"🎉 Bienvenue, {st.session_state.username} ! Voici le contenu protégé.")
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            reset_fields()
            st.session_state.menu = "Connexion"
            st.rerun()

if __name__ == "__main__":
    main()
