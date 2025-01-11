import streamlit as st
import pandas as pd

def select_file():
    st.title("WYBÓR PLIKU")
    
    # Wybór pliku CSV
    uploaded_file = st.file_uploader("Załaduj plik CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Załaduj dane z pliku CSV
        data = pd.read_csv(uploaded_file)

        if 'Grupa' in data.columns and 'VDR FokI' in data.columns and 'BSM' in data.columns:
            st.session_state.data = data  # Przechowaj dane w session_state
            return data
        else:
            st.error("Plik CSV musi zawierać kolumny: 'Grupa', 'VDR FokI' i 'BSM'.")
    else:
        st.write("Proszę załadować plik CSV, aby rozpocząć.")
        return None  # Zwróć None, gdy nie ma danych
