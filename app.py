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

with tab2:
    st.subheader("Insights & Trends")

    if len(df) < 5:
        st.info("Add at least a few entries to generate insights.")
    else:
        # Correlations
        sleep_corr = df["sleep_hours"].corr(df["headache_intensity"])
        stress_corr = df["stress_level"].corr(df["headache_intensity"])

        st.write(f"Correlation (sleep vs intensity): **{sleep_corr:.2f}**")
        st.write(f"Correlation (stress vs intensity): **{stress_corr:.2f}**")

        # Plot: sleep vs headache
        fig1 = plt.figure()
        plt.scatter(df["sleep_hours"], df["headache_intensity"], alpha=0.6)
        plt.xlabel("Sleep hours")
        plt.ylabel("Headache intensity")
        plt.title("Sleep hours vs headache intensity")
        plt.grid(True)
        st.pyplot(fig1)

        # Plot: stress vs headache
        fig2 = plt.figure()
        plt.scatter(df["stress_level"], df["headache_intensity"], alpha=0.6)
        plt.xlabel("Stress level (0–10)")
        plt.ylabel("Headache intensity")
        plt.title("Stress level vs headache intensity")
        plt.grid(True)
        st.pyplot(fig2)

        # Rule-based insights
        high_stress_days = df[df["stress_level"] >= 7]
        low_sleep_days = df[df["sleep_hours"] < 6]

        insights = []
        if len(low_sleep_days) > 0 and low_sleep_days["headache_intensity"].mean() > df["headache_intensity"].mean():
            insights.append("Headaches tend to be more intense after nights with less than **6 hours** of sleep.")
        if len(high_stress_days) > 0 and high_stress_days["headache_intensity"].mean() > df["headache_intensity"].mean():
            insights.append("Headaches tend to be more intense on **high-stress** days (stress ≥ 7).")

        st.markdown("### Personalised insights (rule-based)")
        if insights:
            for i in insights:
                st.write(f"- {i}")
        else:
            st.write("No strong patterns detected in this sample yet.")

with tab3:
    st.subheader("Your entries")
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="headache_data.csv",
        mime="text/csv"
    )