import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2

def chi_square_analysis(data):
    """
    Funkcja wykonująca test Chi-Square na danych.
    Użytkownik wybiera odpowiednie kolumny, a funkcja wyświetla wyniki.
    """
    st.title("Chi-Square Test")

    # Użytkownik wybiera kolumny do testu
    group_col = st.selectbox("Select the group column", data.columns)
    value_col = st.selectbox("Select the value column", [col for col in data.columns if col != group_col])

    # Przygotowanie tabeli kontyngencji
    contingency_table = pd.crosstab(data[group_col], data[value_col])
    st.write("## Contingency Table")
    st.dataframe(contingency_table)

    # Obliczenie Chi-Square (ręczne)
    observed = contingency_table.values
    row_totals = observed.sum(axis=1)
    col_totals = observed.sum(axis=0)
    total = observed.sum()

    expected = np.outer(row_totals, col_totals) / total
    chi_square_stat = ((observed - expected) ** 2 / expected).sum()

    # Obliczenie p-wartości (przybliżenie przy użyciu rozkładu chi-kwadrat)
    dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    p_value = 1 - chi2.cdf(chi_square_stat, dof)

    # Wyświetlenie wyników
    st.write("## Chi-Square Test Results")
    st.write(f"Chi-Square Statistic: {chi_square_stat:.4f}")
    st.write(f"p-value: {p_value:.4f}")

    # Interpretacja
    alpha = 0.05
    if p_value < alpha:
        st.write(f"### Result: The result is statistically significant (Reject H₀). The p-value is {p_value:.4f}, which is less than 0.05.")
    else:
        st.write(f"### Result: The result is not statistically significant (Fail to reject H₀). The p-value is {p_value:.4f}, which is greater than or equal to 0.05.")

def odds_ratio_analysis(data):
    """
    Funkcja wykonująca analizę ODDS RATIO na danych.
    """
    st.title("ODDS RATIO Analysis")
    
    # Implementacja analizy ODDS RATIO (do uzupełnienia w zależności od wymagań analizy)
    
    # Przycisk powrotu
    if st.button("Powróć do menu"):
        st.session_state.page = "file"
