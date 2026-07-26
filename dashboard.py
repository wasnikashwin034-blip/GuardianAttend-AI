import streamlit as st
import pandas as pd

st.title("AI Smart Attendance System")

df = pd.read_csv(
    "attendance.csv",
    names=["Name", "Time", "Date"]
)

st.dataframe(df)

st.metric(
    "Total Attendance Records",
    len(df)
)
