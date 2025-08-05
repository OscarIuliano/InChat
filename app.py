import streamlit as st
from auth import crea_tabella_utenti, login, registra

import sqlite3
from chat import crea_tabella_messaggi, invia_messaggio, leggi_chat

# Crea la tabella utenti al primo avvio
crea_tabella_utenti()

# Titolo app
st.set_page_config(page_title="Login Messaggistica", layout="centered")
st.title("💬 Login / Registrazione")

# Inizializza session state
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False
    st.session_state.username = ""

# Se utente autenticato, mostra la "home"
if st.session_state.autenticato:
    # Crea tabella messaggi (solo la prima volta)
    crea_tabella_messaggi()

    st.sidebar.button("🔒 Logout", on_click=lambda: st.session_state.update({"autenticato": False, "username": ""}) or st.rerun())
    st.success(f"✅ Benvenuto, {st.session_state.username}!")

    # Ottieni altri utenti
    conn = sqlite3.connect("utenti.db")
    c = conn.cursor()
    c.execute("SELECT username FROM utenti WHERE username != ?", (st.session_state.username,))
    altri_utenti = [row[0] for row in c.fetchall()]
    conn.close()

    if altri_utenti:
        destinatario = st.selectbox("📨 Seleziona un utente con cui chattare", altri_utenti)

        # Mostra conversazione
        st.subheader(f"💬 Chat con {destinatario}")
        chat = leggi_chat(st.session_state.username, destinatario)
        for mittente, testo, timestamp in chat:
            if mittente == st.session_state.username:
                st.markdown(f"<div style='text-align:right'><b>Tu:</b> {testo} <br><small>{timestamp}</small></div><hr>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left'><b>{mittente}:</b> {testo} <br><small>{timestamp}</small></div><hr>", unsafe_allow_html=True)

        # Campo di invio messaggio
        testo = st.text_input("✍️ Scrivi un messaggio:")
        if st.button("Invia") and testo.strip():
            invia_messaggio(st.session_state.username, destinatario, testo)
            st.rerun()
    else:
        st.info("Non ci sono altri utenti registrati per chattare.")

else:
    # Tabs per Login e Registrazione
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registrati"])

    with tab1:
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Login"):
            if login(user, pwd):
                st.session_state.autenticato = True
                st.session_state.username = user
                st.rerun()
            else:
                st.error("❌ Credenziali errate.")

    with tab2:
        new_user = st.text_input("Nuovo username", key="reg_user")
        new_pwd = st.text_input("Nuova password", type="password", key="reg_pwd")
        if st.button("Registrati"):
            if registra(new_user, new_pwd):
                st.success("✅ Registrazione completata. Ora puoi fare login.")
            else:
                st.warning("⚠️ Username già esistente.")
