import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
from statsmodels.stats.contingency_tables import Table2x2

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


def HW(data, locus):
    """
    Funkcja wykonuje analizę Hardy'ego-Weinberga.
    """
    # Definiowanie genotypów na podstawie locus
    if locus == "VDR FokI":
        genotypes = ["AA", "AG", "GG"]
    else:
        genotypes = ["CC", "CT", "TT"]

    # Normalizacja danych: zamiana "TC" na "CT"
    data = [genotype.replace("TC", "CT") for genotype in data]

    # Zliczanie genotypów
    aa = data.count(genotypes[0])
    ab = data.count(genotypes[1])
    bb = data.count(genotypes[2])
    
    # Obliczanie częstości alleli
    total = aa + ab + bb
    if total == 0:
        raise ValueError("Brak danych do analizy.")

    p = (2 * aa + ab) / (2 * total)
    q = 1 - p
    
    # Obliczanie oczekiwanych wartości
    expected_aa = total * p**2
    expected_ab = total * 2 * p * q
    expected_bb = total * q**2

    # Tworzenie list obserwowanych i oczekiwanych wartości
    observed = [aa, ab, bb]
    expected = [expected_aa, expected_ab, expected_bb]

    st.markdown("### Wyniki analizy HW:")
    st.write(f"**Częstość allelu p i q:** p: {p:.4f}, q: {q:.4f}")
    st.write(f"**Liczebność obserwowana:** AA: {aa}, AB: {ab}, BB: {bb}")
    st.write(f"**Liczebność oczekiwana:** AA: {expected_aa:.4f}, AB: {expected_ab:.4f}, BB:{expected_bb:.4f}\n")
    
    visualise(genotypes, observed, expected)


def visualise(genotype, observed, expected):

    # Wykres słupkowy
    width = 0.35  # Szerokość słupków

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(genotype, observed, width, label='Obserwowane', color='skyblue')
    ax.bar(genotype, expected, width, bottom=observed, label='Oczekiwane', color='lightgreen')

    # Dodanie tytułu i etykiet osi
    ax.set_title('Porównanie obserwowanych i oczekiwanych liczby genotypów')
    ax.set_xlabel('Genotyp')
    ax.set_ylabel('Liczba')
    ax.legend()

    st.pyplot(fig)


def OR(data, locus):
    """
    Funkcja oblicza odds ratio oraz przedział ufności 95% 
    dla danego locus (VDR FokI lub BSM).
    """

    if locus == "VDR FokI":
        table = pd.crosstab(data['VDR FokI'], data['Grupa'])
    else:
        table = pd.crosstab(data['BSM'], data['Grupa'])
  
    # Obliczanie wartości dla A i B
    A_cancer = 2 * table.iloc[0, 0] + table.iloc[1, 0]
    B_cancer = 2 * table.iloc[2, 0] + table.iloc[1, 0]
    A_control = 2 * table.iloc[0, 1] + table.iloc[1, 1]
    B_control = 2 * table.iloc[2, 1] + table.iloc[1, 1]

    # Tabela 2x2 dla alleli A i B
    contingency_table = pd.DataFrame({
        'Cancer': [A_cancer, B_cancer],
        'Control': [A_control, B_control]
    }, index=['Allele A', 'Allele B'])

    # Obliczanie odds ratio
    OR_value = Table2x2(contingency_table.values).oddsratio
    OR_confint = Table2x2(contingency_table.values).oddsratio_confint()

    st.write(f"### Analiza dla locus: {locus}")
    st.write("#### Tabela 2x2:")
    st.write(contingency_table)

    # Wyświetlanie wyników
    st.write(f"Odds Ratio: {OR_value:.2f}")
    st.write(f"95% Confidence Interval: ({OR_confint[0]:.2f}, {OR_confint[1]:.2f})")
    
    return OR_value, OR_confint


def OR_analysis(data):
    """
    Funkcja wykonuje analizę odds ratio 
    dla dwóch loci: 'VDR FokI' oraz 'BSM'.
    """
    for locus in ['VDR FokI', 'BSM']:
        OR(data, locus)


def HW_analysis(data):
    """
    Funkcja analizuje dane pod kątem HWE
    dla każdego locus i każdej grupy.
    """

    for locus in ['VDR FokI', 'BSM']:
        for group in ['Cancer', 'Control']:

            genotypes = data[data['Grupa'] == group][locus].tolist()
            HW(genotypes, locus)
      



