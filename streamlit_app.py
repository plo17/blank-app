import streamlit as st
import pandas as pd
import numpy as np

# Streamlit app title
st.title("Chi-Square Test App")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    # Load the uploaded file
    data = pd.read_csv(uploaded_file)
    st.write("## Data Preview")
    st.dataframe(data.head())

    # User selects columns for the test
    group_col = st.selectbox("Select the group column", data.columns)
    value_col = st.selectbox("Select the value column", [col for col in data.columns if col != group_col])

    # Prepare contingency table
    contingency_table = pd.crosstab(data[group_col], data[value_col])
    st.write("## Contingency Table")
    st.dataframe(contingency_table)

    # Chi-Square calculation (manual)
    observed = contingency_table.values
    row_totals = observed.sum(axis=1)
    col_totals = observed.sum(axis=0)
    total = observed.sum()

    expected = np.outer(row_totals, col_totals) / total

    chi_square_stat = ((observed - expected) ** 2 / expected).sum()

    # p-value calculation (approximation using chi-square distribution)
    from scipy.stats import chi2
    dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    p_value = 1 - chi2.cdf(chi_square_stat, dof)

    # Display results
    st.write("## Chi-Square Test Results")
    st.write(f"Chi-Square Statistic: {chi_square_stat:.4f}")
    st.write(f"p-value: {p_value:.4f}")

    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        st.write(f"### Result: The result is statistically significant (Reject H₀). The p-value is {p_value:.4f}, which is less than 0.05.")
    else:
        st.write(f"### Result: The result is not statistically significant (Fail to reject H₀). The p-value is {p_value:.4f}, which is greater than or equal to 0.05.")
