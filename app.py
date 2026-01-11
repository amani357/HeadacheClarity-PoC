import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Headache Clarity", layout="centered")
st.title("Headache Clarity")

DATA_FILE = "headache_data.csv"

# Load existing data
try: 
    df = pd.read_csv(DATA_FILE, parse_dates=['date'])
except FileNotFoundError:
    df = pd.DataFrame(columns=['date', 'sleep_hours', 'stress_level', 'headache_intensity'])

tab1, tab2, tab3 = st.tabs(["Log Entry", "Insights & Trends", "Data"])

with tab1:
    st.subheader("New Headache Entry")

    with st.form("entry_form"):
        entry_date = st.date_input("Date", value=date.today())
        sleep_hours = st.slider("Sleep hours", 0.0, 12.0, 7.0, 0.1)
        stress_level = st.slider("Stress level (0–10)", 0, 10, 5)
        headache_intensity = st.slider("Headache intensity (0–10)", 0, 10, 3)
        submitted = st.form_submit_button("Save entry")
    
    if submitted:
        new_row = {
            "date": entry_date,
            "sleep_hours": sleep_hours,
            "stress_level": stress_level,
            "headache_intensity": headache_intensity
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry saved!")

