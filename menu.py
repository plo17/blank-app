import streamlit as st
from analysis import chi_square_analysis, OR_analysis, HW_analysis

def select_analysis(data):

    """
    Funkcja obsługuje wybór analizy danych i wyświetla podgląd danych wejściowych. 
    Użytkownik może wybrać jedną z trzech analiz: test chi-kwadrat, 
    współczynnik szans (odds ratio) lub równowagę Hardy'ego-Weinberga.
    """

    st.write("## PODGLĄD DANYCH")
    st.dataframe(data.head())

    st.title("WYBÓR ANALIZY")
    
    #wybór analizy
    analysis_option = st.selectbox("Wybierz rodzaj analizy", ["-","Chi-Square Test", "Odds ratio", "Hardy Weinberg"])

    if analysis_option == "Chi-Square Test":
        chi_square_analysis(data)

    if analysis_option == "Odds ratio":
        OR_analysis(data)

    elif analysis_option == "Hardy Weinberg":
        HW_analysis(data)
    
    #dodatkowy przyciski
    if st.button("Powrót"):
        st.session_state.page = "menu"
        st.rerun()
