import streamlit as st
import pandas as pd
def riepilogo_presenze():
    st.header('Riepilogo Presenze')

    # Leggi il file di testo e imposta le intestazioni delle colonne
    df = pd.read_csv('./registrazioni.txt', header=None, names=['Nome', 'Movimento', 'Timestamp'], delimiter=', ')

    # Dividi la colonna Timestamp in Data e Ora
    df[['Data', 'Ora']] = df['Timestamp'].str.split(' ', expand=True)

    # Rimuovi la colonna Timestamp
    df.drop(columns=['Timestamp'], inplace=True)

    # Converti la colonna Data in formato datetime
    df['Data'] = pd.to_datetime(df['Data'])

    # Formatta le date nel formato "dd/mm/yyyy"
    df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')

    # Ottieni un elenco unico di nomi
    nomi = df['Nome'].unique()

    # Widget per selezionare i nomi da filtrare con placeholder personalizzato
    selected_names = st.multiselect("Seleziona nome", nomi, placeholder="Seleziona nome...")

    # Filtra il DataFrame in base al nome selezionato
    df_filtered = df.copy()
    if selected_names:
        df_filtered = df_filtered[df_filtered['Nome'].isin(selected_names)]

    # Visualizza il DataFrame filtrato
    st.table(df_filtered)

st.title("Contacts")

riepilogo_presenze()

st.sidebar.image("logo.jpeg", use_column_width=True)
st.sidebar.success(f'Welcome *{st.session_state["name"]}*')