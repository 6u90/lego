import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import pandas as pd

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)



authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def registra_presenza():
    st.header('Registra Presenza')
    nome = st.text_input('Il tuo nome', value=st.session_state["name"], disabled=True)
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

st.title("LEGO - Registra Presenza")

authenticator.login()
if st.session_state["authentication_status"]:
    registra_presenza()
    st.sidebar.button("Logout", key="logout_button")
    st.sidebar.success(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "main")
    authenticator.login()
    
    # authenticator.logout()


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# st.set_page_config(
#     page_title="Multipage app",
#     page_icon="🏗️"
# )

st.sidebar.image("logo.jpeg", use_column_width=True)


# if st.sidebar.button("Logout", key="logout_button"):
#     authenticator.logout("Logout", "main")
