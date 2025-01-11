import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

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


    

        


def hw_analysis(data):
    """
    Funkcja wykonująca analizę Hardy'ego-Weinberga na danych.
    """
    st.title("Hardy-Weinberg Analysis")

    # Tworzenie tabeli kontyngencji
    contingency_table = pd.crosstab(data["Grupa"], data["VDR FokI"])

    # Obliczanie częstości alleli
    # Liczymy liczbę alleli dominujących (GG) i recesywnych (AG, AA)
    observed_GG = contingency_table.loc['Cancer', 'GG']
    observed_AG = contingency_table.loc['Cancer', 'AG']
    observed_AA = contingency_table.loc['Cancer', 'AA']

    total_genotypes = observed_GG + observed_AG + observed_AA

    # Częstość allelu G (dominującego)
    p = (2 * observed_GG + observed_AG) / (2 * total_genotypes)
    # Częstość allelu A (recesywnego)
    q = 1 - p

    # Obliczanie oczekiwanych liczby genotypów na podstawie częstości alleli
    expected_GG = p**2 * total_genotypes
    expected_AG = 2 * p * q * total_genotypes
    expected_AA = q**2 * total_genotypes

    # Obliczanie różnicy procentowej między obserwowanymi a oczekiwanymi wartościami
    diff_GG = abs(observed_GG - expected_GG) / expected_GG * 100
    diff_AG = abs(observed_AG - expected_AG) / expected_AG * 100
    diff_AA = abs(observed_AA - expected_AA) / expected_AA * 100

    # Wyświetlanie wyników
    st.markdown("### Wyniki analizy:")
    st.write(f"**Częstość allelu G (p):** {p:.3f}")
    st.write(f"**Częstość allelu A (q):** {q:.3f}\n")
    st.write(f"**Oczekiwana liczba GG:** {expected_GG:.2f}")
    st.write(f"**Oczekiwana liczba AG:** {expected_AG:.2f}")
    st.write(f"**Oczekiwana liczba AA:** {expected_AA:.2f}\n")

    # Wyświetlanie różnic procentowych
    st.write(f"**Różnica procentowa GG:** {diff_GG:.2f}%")
    st.write(f"**Różnica procentowa AG:** {diff_AG:.2f}%")
    st.write(f"**Różnica procentowa AA:** {diff_AA:.2f}%")

    # Interpretacja wyników
    if diff_GG < 5 and diff_AG < 5 and diff_AA < 5:
        st.write("**Interpretacja:** Dane są zgodne z równowagą Hardy'ego-Weinberga.")
    else:
        st.write("**Interpretacja:** Dane wskazują na brak równowagi Hardy'ego-Weinberga.")

    # Przygotowanie danych do wykresu
    labels = ['GG', 'AG', 'AA']
    observed = [observed_GG, observed_AG, observed_AA]
    expected = [expected_GG, expected_AG, expected_AA]
    
    # Wykres słupkowy
    width = 0.35  # Szerokość słupków

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, observed, width, label='Obserwowane', color='skyblue')
    ax.bar(labels, expected, width, bottom=observed, label='Oczekiwane', color='lightgreen')

    # Dodanie tytułu i etykiet osi
    ax.set_title('Porównanie obserwowanych i oczekiwanych liczby genotypów')
    ax.set_xlabel('Genotyp')
    ax.set_ylabel('Liczba')
    ax.legend()

    st.pyplot(fig)
    
