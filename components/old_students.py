import streamlit as st
import sqlite3
import pandas as pd

st.title("📋 Registered Students")

conn = sqlite3.connect("data/attendance.db")

df = pd.read_sql_query(
    "SELECT * FROM students",
    conn
)

conn.close()

st.dataframe(df, use_container_width=True)

st.write(f"Total Students: {len(df)}")