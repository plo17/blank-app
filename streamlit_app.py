import streamlit as st
from file_loader import select_file
from menu import select_analysis

def main():
    
    if 'page' not in st.session_state:
        st.session_state.page = "file"  # Domyślnie strona "file" (Wybór pliku)
    
    if st.session_state.page == "file":
        data = select_file()
        if data is not None:
            st.session_state.page = "analysis"
            st.rerun()  # Wymuszenie odświeżenia aplikacji

    elif st.session_state.page == "analysis":
        if 'data' in st.session_state:
            select_analysis(st.session_state.data)  # Przejdź do analizy
        else:
            st.write("Brak danych do analizy.")
        
    

    elif st.session_state.page == "results":
        # Przyciski po zakończeniu analizy
        if st.button("Nowa analiza"):
            st.session_state.page = "analysis"  # Przejdź do strony wyboru analizy
            st.rerun()  # Wymuszenie odświeżenia aplikacji

        if st.button("Nowy plik"):
            st.session_state.page = "file"  # Powróć do strony wyboru pliku
            st.rerun()  # Wymuszenie odświeżenia aplikacji


if __name__ == "__main__":
    main()
