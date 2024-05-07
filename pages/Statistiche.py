import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def statistiche():
    st.header('Statistiche')

    # Leggi il file di testo e imposta le intestazioni delle colonne
    df = pd.read_csv('./registrazioni.txt', header=None, names=['Nome', 'Movimento', 'Timestamp'], delimiter=', ')

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

st.title("Projects")

statistiche()

st.sidebar.image("logo.jpeg", use_column_width=True)
st.sidebar.success(f'Welcome *{st.session_state["name"]}*')