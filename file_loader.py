import streamlit as st
import pandas as pd

def select_file():
    st.title("WYBÓR PLIKU")
    
    # Wybór pliku CSV
    uploaded_file = st.file_uploader("Załaduj plik CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Załaduj dane z pliku CSV
        data = pd.read_csv(uploaded_file)
        st.session_state.data = data  # Przechowaj dane w session_state

        st.write("## Podgląd danych")
        st.dataframe(data.head())  # Pokaż podgląd danych
        st.write("Po załadowaniu pliku, wybierz odpowiednią analizę.")
        return data  # Zwróć dane do głównej funkcji
    else:
        st.write("Proszę załadować plik CSV, aby rozpocząć.")
        return None  # Zwróć None, gdy nie ma danych
