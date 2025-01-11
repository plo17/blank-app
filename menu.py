import streamlit as st
from analysis import chi_square_analysis, odds_ratio_analysis

def select_analysis(data):

    st.write("## PODGLĄD DANYCH")
    st.dataframe(data.head())  # Pokaż 5 pierwszych wierszy

    st.title("WYBÓR ANALIZY")
    
    # Debugging: Sprawdzanie, czy funkcja jest wywołana
    st.write("Wybór analizy: Chi-Square Test lub ODDS RATIO")

    # Wybór analizy
    analysis_option = st.selectbox("Wybierz rodzaj analizy", ["-","Chi-Square Test", "ODDS RATIO"])


    if analysis_option == "Chi-Square Test":
        chi_square_analysis(data)
    elif analysis_option == "ODDS RATIO":
        odds_ratio_analysis(data)
