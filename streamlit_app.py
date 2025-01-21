import streamlit as st
from file_loader import select_file
from menu import select_analysis

def main():
    
    """
    Funkcja obsługuje nawigację między różnymi stronami aplikacji Streamlit, 
    w tym wybór pliku, wybór analizy danych.
    """

    if 'page' not in st.session_state:
        st.session_state.page = "file"  #domyślna strona
    
    if st.session_state.page == "file":
        data = select_file()
        if data is not None:
            st.session_state.page = "analysis"
            st.rerun()  #odświeżenie aplikacji

    elif st.session_state.page == "analysis":
        if 'data' in st.session_state:
            select_analysis(st.session_state.data)  # przejscie do analizy
        else:
            st.write("No data available for analysis.")
        

    elif st.session_state.page == "menu":
        #przyciski po zakończeniu analizy
        if st.button("New analysis"):
            st.session_state.page = "analysis"  
            st.rerun()  

        if st.button("New file"):
            st.session_state.page = "file"  
            st.rerun()  


if __name__ == "__main__":
    main()
