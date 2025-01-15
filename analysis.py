import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
from statsmodels.stats.contingency_tables import Table2x2

def CHI2(data, group_col, value_col):

    # Normalizacja danych: zamiana "TC" na "CT"
    if value_col == "BSM":
        data[value_col] = data[value_col].replace("TC", "CT")

    # Przygotowanie tabeli kontyngencji
    table = pd.crosstab(data[group_col], data[value_col])
    
    # Obliczenie Chi-Square (ręczne)
    observed = table.values
    row_totals = observed.sum(axis=1)
    col_totals = observed.sum(axis=0)
    total = observed.sum()

    expected = np.outer(row_totals, col_totals) / total
    chi2_stat = ((observed - expected) ** 2 / expected).sum()

    # Obliczenie p-wartości (przybliżenie przy użyciu rozkładu chi-kwadrat)
    dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    p_value = 1 - chi2.cdf(chi2_stat, dof)

    return p_value, chi2_stat, table



def HW(data, locus):

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

    plot = visualise(genotypes, observed, expected)
    return p, q, observed, expected, plot


def OR(data, locus):

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
    con_table = pd.DataFrame({
        'Cancer': [A_cancer, B_cancer],
        'Control': [A_control, B_control]
    }, index=['Allele A', 'Allele B'])

    # Obliczanie odds ratio
    OR_value = Table2x2(con_table.values).oddsratio
    OR_confint = Table2x2(con_table.values).oddsratio_confint()

    return OR_value, OR_confint, con_table


def visualise(genotype, observed, expected):

    # Wykres słupkowy
    width = 0.35  # Szerokość słupków

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(genotype, observed, width, label='Obserwowane', color='skyblue')
    ax.bar(genotype, expected, width, bottom=observed, label='Oczekiwane', color='lightgreen')

    # Dodanie tytułu i etykiet osi
    ax.set_title('Porównanie obserwowanych i oczekiwanych liczby genotypów')
    ax.set_xlabel('Genotyp')
    ax.set_ylabel('Liczba')
    ax.legend()
    return fig


def OR_analysis(data):
    """
    Funkcja wykonuje analizę odds ratio 
    dla dwóch loci: 'VDR FokI' oraz 'BSM'.
    Oznaczenie: A - allel dominujący, 
                B - allel recesywny.
    Argumenty:
        data (DataFrame): Zestaw danych zawierający
          informacje o genotypach.

    Zwraca:
        tuple: Iloraz szans (OR) oraz przedział ufności (CI) 
        dla każdego analizowanego locus.

    """
    for locus in ['VDR FokI', 'BSM']:
        OR_value, OR_confint, con_table = OR(data, locus)

        st.write(f"### Analiza dla locus: {locus}")
        st.write("#### Tabela 2x2:")
        st.write(con_table)

        # Wyświetlanie wyników
        st.write(f"Odds Ratio: {OR_value:.2f}")
        st.write(f"95% Confidence Interval: ({OR_confint[0]:.2f}, {OR_confint[1]:.2f})")
    
    return OR_value, OR_confint


def HW_analysis(data):
    """
    Analiza równowagi Hardy’ego-Weinberga (HWE) 
    dla każdego określonego locus i grupy w zestawie danych.
    Obliczenie częstości alleli oraz porównanie zaobserwowanych
    i oczekiwanych liczb genotypów.

    Argumenty:
        data (DataFrame): Zestaw danych zawierający 
        informacje o genotypach i przynależności do grup.

    Zwraca:
        tuple: Krotka zawierająca obliczone 
        częstości alleli (p, q), zaobserwowane liczby genotypów 
        oraz oczekiwane liczby genotypów dla danej grupy i locus.
    """
    st.markdown(f"### Wyniki analizy Hardy'ego-Weinberga\n\n")

    col1, col2 = st.columns([1,1])
    for locus in ['VDR FokI', 'BSM']:
        for group in ['Cancer', 'Control']:

            genotypes = data[data['Grupa'] == group][locus].tolist()
            p, q, observed, expected, plot = HW(genotypes, locus)
            
            with col1:
                st.markdown("  \n")
                st.markdown(f"  \n**Grupa:** {group}  \n**Czynnik:** {locus}")
                st.markdown(f"Częstość allelu p i q:\n**p:** {p:.2f}, **q:** {q:.2f}")

                results_df = pd.DataFrame({
                    "Genotyp": ["AA", "AB", "BB"],
                    "Obserwowana": observed,
                    "Oczekiwana": [f"{e:.2f}" for e in expected]
                })
                st.dataframe(results_df)

            with col2:  
                st.pyplot(plot)
                st.markdown("  \n")
            
    return p, q, observed, expected

def CHI2_analysis(data):

    """
    Test Chi-kwadrat dla wybranych kolumn w zestawie danych.
    Argumenty:
        data (DataFrame): Zestaw danych zawierający
        wartości kategoryczne.
    Zwraca:
        tuple: p-wartość i wartość statystyki Chi-kwadrat.
    """
    st.title("Chi-Square Test")
    # Użytkownik wybiera kolumny do testu
    group_col = st.selectbox("Select the group column", data.columns)
    value_col = st.selectbox("Select the value column", [col for col in data.columns if col != group_col])
    p_value, chi2_value, table = CHI2(data, group_col, value_col)

    st.write("#### Tabela kontyngencji")
    st.dataframe(table)
    # Wyświetlenie wyników
    st.write("#### Chi-Square Test Results")
    st.write(f"**Chi-Square Statistic:** {chi2_value:.4f}")
    st.write(f"**p-value:** {p_value:.4f}")

    # Interpretacja
    alpha = 0.05
    if p_value < alpha:
        st.write(f"The result is statistically significant (Reject H₀). The p-value is {p_value:.4f}, which is less than 0.05.")
    else:
        st.write(f"The result is not statistically significant (Fail to reject H₀). The p-value is {p_value:.4f}, which is greater than or equal to 0.05.")
    
    return p_value, chi2_value
