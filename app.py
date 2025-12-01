import streamlit as st
import pandas as pd
from processing.cleaning import load_statement
from processing.categorize import categorize_df
from model.classifier import merchant_memory, save_memory

st.title("Expense Categorizer")

uploaded = st.file_uploader("Upload your statement CSV")

if uploaded:
    df = load_statement(uploaded)
    df = categorize_df(df)

    st.write("### Review & Fix Categories")

    for i, row in df.iterrows():
        new_cat = st.selectbox(
            f"{row['merchant']}",
            options=df["category"].unique().tolist(),
            index=df["category"].unique().tolist().index(row["category"])
        )

        # if user changed category → update memory
        if new_cat != row["category"]:
            merchant_memory[row["merchant_clean"]] = new_cat
            save_memory()
            df.at[i, "category"] = new_cat

    st.write("### Final Classified Data")
    st.dataframe(df)

    # Next step: dashboard
    if st.button("Show Dashboard"):
        st.session_state["df"] = df
        st.switch_page("dashboard.py")
