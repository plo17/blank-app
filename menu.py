import streamlit as st
from analysis import CHI2_analysis, OR_analysis, HW_analysis

def select_analysis(data):

    """
    Funkcja obsługuje wybór analizy danych i wyświetla podgląd danych wejściowych. 
    Użytkownik może wybrać jedną z trzech analiz: test chi-kwadrat, 
    współczynnik szans (odds ratio) lub równowagę Hardy'ego-Weinberga.
    """

    st.title("WYBÓR ANALIZY")
    #wybór analizy
    analysis_option = st.selectbox("Wybierz rodzaj analizy", ["-","Chi-Square Test", "Odds ratio", "Hardy Weinberg"])

    st.write("## PODGLĄD DANYCH")
    st.dataframe(data.head())

    
    if analysis_option == "Chi-Square Test":
        CHI2_analysis(data)

    if analysis_option == "Odds ratio":
        OR_analysis(data)

    elif analysis_option == "Hardy Weinberg":
        HW_analysis(data)
    
    #dodatkowy przyciski
    if st.button("Powrót"):
        st.session_state.page = "menu"
        st.rerun()
