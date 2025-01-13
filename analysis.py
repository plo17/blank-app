import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
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


def odds_ratio_analysis(data):

    """
    Funkcja oblicza odds ratio dla wszystkich kombinacji genotypów
    'VDR FokI' i 'BSM' w tabeli danych.
    
    Parameters:
    df (pd.DataFrame): Tabela z danymi zawierającymi kolumny 'Grupa', 'VDR FokI', 'BSM'.
    
    Returns:
    dict: Słownik z wynikami odds ratio dla każdej kombinacji genotypów.
    """

    st.title("ODDS RATIO Analysis")
    # Zbiór unikalnych wartości genotypów VDR FokI i BSM
    fok_genotypes = data['VDR FokI'].unique()
    bsm_genotypes = data['BSM'].unique()
    
    results = {}

    # Iterujemy po wszystkich kombinacjach genotypów
    for fok in fok_genotypes:
        for bsm in bsm_genotypes:
            # Tworzymy tabelę kontyngencyjną dla tej kombinacji genotypów
            contingency_table = pd.crosstab([data['Grupa'], data['VDR FokI']], data['BSM'])
            
            try:
                # Pobieramy wartości z tabeli kontyngencyjnej
                a = contingency_table.loc[('Cancer', fok), bsm]  # Cancer, fok, bsm
                d = contingency_table.loc[('Healthy', fok), bsm]  # Healthy, fok, bsm

                # Pobieramy pozostałe wartości
                b = contingency_table.loc[('Cancer', fok), 'CT']  # Cancer, fok, CT
                c = contingency_table.loc[('Cancer', fok), 'TT']  # Cancer, fok, TT
                e = contingency_table.loc[('Healthy', fok), 'CT']  # Healthy, fok, CT
                f = contingency_table.loc[('Healthy', fok), 'TT']  # Healthy, fok, TT

                # Obliczamy odds ratio
                odds_ratio = (a * f) / (b * d)
                results[f'{fok}-{bsm}'] = odds_ratio

            except KeyError:
                # Jeżeli tabela nie zawiera danych dla podanych genotypów
                results[f'{fok}-{bsm}'] = None

    # Wyświetlanie wyników
    st.write("Wyniki Odds Ratio:")
    for key, value in results.items():
        st.write(f"Kombinacja {key} - Odds Ratio: {value}")



def hw(data, locus):
    """
    Funkcja wykonuje analizę Hardy'ego-Weinberga.
    """
    # Definiowanie genotypów na podstawie locus
    if locus == "VDR FokI":
        genotypes = ["AA", "AG", "GG"]
    else:
        genotypes = ["CC", "CT", "TT"]

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


def hw_analysis(data):
    """
    Funkcja analizuje dane pod kątem HWE dla każdego locus i każdej grupy.
    """
    for locus in ['VDR FokI', 'BSM']:
        for group in ['Cancer', 'Control']:

            genotypes = data[data['Grupa'] == group][locus].tolist()
            hw(genotypes, locus)
      

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



"""    # Obliczanie Odds Ratio między grupą "Cancer" a "Control"
    for locus in ['VDR', 'FokI', 'BSM']:
        table = pd.crosstab(data['Grupa'], data[locus])
        print(f"\nOdds Ratio dla locus {locus}:")
        for genotype in table.columns:
            oddsratio = Table2x2(table[[genotype]]).oddsratio
            print(f"  Genotyp {genotype}: OR = {oddsratio:.4f}")"""