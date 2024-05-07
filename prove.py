import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Funzione per la registrazione della presenza
def registra_presenza():
    st.header('Registra Presenza')
    nome = st.text_input('Inserisci il tuo nome')
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

# Funzione per visualizzare il riepilogo delle presenze
def riepilogo_presenze():
    st.header('Riepilogo Presenze')

    # Leggi il file di testo e imposta le intestazioni delle colonne
    df = pd.read_csv('registrazioni.txt', header=None, names=['Nome', 'Movimento', 'Timestamp'], delimiter=', ')

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

# Funzione per visualizzare le statistiche
def statistiche():
    st.header('Statistiche')

    # Leggi il file di testo e imposta le intestazioni delle colonne
    df = pd.read_csv('registrazioni.txt', header=None, names=['Nome', 'Movimento', 'Timestamp'], delimiter=', ')

    # Dividi la colonna Timestamp in Data e Ora
    df[['Data', 'Ora']] = df['Timestamp'].str.split(' ', expand=True)

    # Converti la colonna Data in formato datetime
    df['Data'] = pd.to_datetime(df['Data'])

    # Calcola il numero di presenze per ciascun nome
    presenze_per_nome = df['Nome'].value_counts()

    # Visualizza il grafico a barre delle presenze per nome
    st.write("Numero di presenze")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=presenze_per_nome.index, y=presenze_per_nome.values, ax=ax1)
    ax1.set_xlabel('Nome')
    ax1.set_ylabel('Numero di Presenze')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    st.pyplot(fig1)

    # Calcola il numero di presenze per ciascun giorno
    presenze_per_giorno = df['Data'].value_counts()

    # Visualizza il grafico a barre delle presenze per giorno
    st.write("Numero di presenze per giorno")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=presenze_per_giorno.index, y=presenze_per_giorno.values, ax=ax2)
    ax2.set_xlabel('Giorno')
    ax2.set_ylabel('Numero di Presenze')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    st.pyplot(fig2)

# Funzione principale
def main():
    # Aggiungi un logo alla sidebar
    st.sidebar.image('logo.jpeg', use_column_width=True)

    st.sidebar.title('LEGO - Presenze')
    scelta_menu = st.sidebar.radio('Seleziona', ['Registra Presenza', 'Riepilogo Presenze', 'Statistiche'])

    if scelta_menu == 'Registra Presenza':
        registra_presenza()
    elif scelta_menu == 'Riepilogo Presenze':
        riepilogo_presenze()
    elif scelta_menu == 'Statistiche':
        statistiche()

if __name__ == '__main__':
    main()
