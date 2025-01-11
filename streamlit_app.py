import streamlit as st
from file_loader import select_file
from menu import select_analysis

def main():
    
    if 'page' not in st.session_state:
        st.session_state.page = "file"  # Domyślnie strona "file" (Wybór pliku)
    
    if st.session_state.page == "file":
        data = select_file()  # Wybór pliku
        if data is not None:  # Jeśli dane zostały załadowane, zmień stronę i odśwież aplikację
            st.session_state.page = "analysis"
            st.rerun()  # Wymuszenie odświeżenia aplikacji

    elif st.session_state.page == "analysis":
        if 'data' in st.session_state:
            select_analysis(st.session_state.data)  # Przejdź do analizy
        else:
            st.write("Brak danych do analizy.")

if __name__ == "__main__":
    main()
