import streamlit as st
import sqlite3
import bcrypt
import os
import time
import re

# * Définir le chemin de la base de données dans le dossier souhaité *
DB_PATH = os.path.join("Code", "src", "Back", "db", "users.sqlite")

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

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False

def is_valid_password(password):
    return (
        len(password) >= 8 and 
        re.search(r"\d", password) and 
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def reset_fields():
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.confirm_password = ""

def show_login_page():
    st.title("Connexion sécurisée à l'application")
    init_db()

    if 'menu' not in st.session_state:
        st.session_state.menu = "Connexion"
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'password' not in st.session_state:
        st.session_state.password = ""
    if 'confirm_password' not in st.session_state:
        st.session_state.confirm_password = ""

    if st.session_state.menu == "Créer un compte":
        st.subheader("Créer un compte")
        username = st.text_input("Nom d'utilisateur", key="username_create")
        password = st.text_input("Mot de passe", type="password", key="password_create")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="confirm_password_create")

        col_spacer, col1, col2, col_spacer = st.columns([1, 1, 1, 1])
        if col1.button("S'inscrire"):
            if password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas.")
            elif not is_valid_password(password):
                st.error("⚠️ Le mot de passe doit contenir au moins 8 caractères, un chiffre et un caractère spécial.")
            elif add_user(username, password):
                st.success("✅ Compte créé avec succès ! Redirection vers la connexion...")
                time.sleep(2)
                st.session_state.menu = "Connexion"
                reset_fields()
                st.rerun()
            else:
                st.error("❌ Nom d'utilisateur déjà pris.")
        if col2.button("Déjà un compte ?"):
            st.session_state.menu = "Connexion"
            reset_fields()
            st.rerun()

    elif st.session_state.menu == "Connexion":
        st.subheader("Connexion")
        username = st.text_input("Nom d'utilisateur", key="username_login")
        password = st.text_input("Mot de passe", type="password", key="password_login")

        col_spacer, col1, col2 = st.columns([1, 2,2])
        if col1.button("Se connecter"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Bienvenue {username} !")
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects.")
        if col2.button("Créer un compte"):
            st.session_state.menu = "Créer un compte"
            reset_fields()
            st.rerun()
