import streamlit as st
import altair as alt
import pandas as pd

df = st.session_state.get("df")

st.title("Spending Dashboard")

if df is not None:
    st.write("### Spending by Category")
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="category",
            y="amount:Q"
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.write("### Total Spent: ", df["amount"].sum())
