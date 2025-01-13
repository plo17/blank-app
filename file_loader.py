import streamlit as st
import pandas as pd

def select_file():

    """
    Funkcja obsługuje wybór pliku CSV przez użytkownika. 
    Wczytuje dane z pliku i sprawdza, czy plik zawiera 
    wymagane kolumny: 'Grupa', 'VDR FokI' i 'BSM'.
    """

    st.title("WYBÓR PLIKU")
    
    # wybór pliku CSV
    uploaded_file = st.file_uploader("Załaduj plik CSV", type=["csv"])
    
    if uploaded_file is not None:
        # wczytanie danych z pliku CSV
        data = pd.read_csv(uploaded_file)

        if 'Grupa' in data.columns and 'VDR FokI' in data.columns and 'BSM' in data.columns:
            st.session_state.data = data  # przechowanie danych
            return data
        else:
            st.error("Plik CSV musi zawierać kolumny: 'Grupa', 'VDR FokI' i 'BSM'.")
    else:
        st.write("Proszę załadować plik CSV, aby rozpocząć.")
        return None
