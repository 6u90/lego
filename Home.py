import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import pandas as pd

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(page_title="LEGO - Presenze", page_icon="🏗️")

# Inizializza l'autenticatore
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Funzione per la registrazione della presenza
def registra_presenza():
    st.header('Registra Presenza')
    nome = st.text_input('Il tuo nome', value=st.session_state.get("name", ""), disabled=True)
    movimento = st.radio('Seleziona il movimento', ['Entrata', 'Uscita'])

    # Controllo che tutti i campi siano stati compilati
    if nome and movimento:
        if st.button('Registra'):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('registrazioni.txt', 'a') as file:
                file.write(f"{nome}, {movimento}, {timestamp}\n")
            st.success(f'Presenza registrata per {nome} - {timestamp}')
    else:
        st.warning("Inserisci tutti i campi prima di registrare la presenza.")

# Pagina principale
def main():
    st.title("LEGO - Registra Presenza")
    st.image("logo.jpeg", width=300)
    
    # Effettua il login
    authenticator.login()

    # Se l'utente è autenticato, mostra la funzione di registrazione presenza
    if st.session_state["authentication_status"]:
        registra_presenza()
        st.sidebar.success(f'Welcome *{st.session_state.get("name", "")}*')

        # Imposta il cookie per il login persistente
        authenticator.set_cookie()

    # Se l'utente non è autenticato, mostra messaggio di errore o richiesta di login
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    st.sidebar.image("logo.jpeg", use_column_width=True)

# Esegui la funzione principale
if __name__ == "__main__":
    main()
