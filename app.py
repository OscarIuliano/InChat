import streamlit as st
from auth import crea_tabella_utenti, login, registra

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
    st.success(f"✅ Benvenuto, {st.session_state.username}!")
    st.write("🎉 Sei dentro l'applicazione messaggistica!")
    if st.button("🔒 Logout"):
        st.session_state.autenticato = False
        st.rerun()

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
