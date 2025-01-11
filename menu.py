import streamlit as st
from analysis import chi_square_analysis, odds_ratio_analysis, hw_analysis

def select_analysis(data):

    st.write("## PODGLĄD DANYCH")
    st.dataframe(data.head())  #5 pierwszych wierszy

    st.title("WYBÓR ANALIZY")
    
    # Wybór analizy
    analysis_option = st.selectbox("Wybierz rodzaj analizy", ["-","Chi-Square Test", "Odds ratio", "Hardy Weinberg"])

    if analysis_option == "Chi-Square Test":
        chi_square_analysis(data)

    if analysis_option == "Odds ratio":
        odds_ratio_analysis(data)

    elif analysis_option == "Hardy Weinberg":
        hw_analysis(data)

# Przyciski do zakończenia analizy i przejścia do wyników
    if st.button("Powrót"):
        st.session_state.page = "results"
        st.rerun()  # odświeżenie aplikacji i przejście do strony wyników
