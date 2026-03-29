import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time

model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Predictive Maintenance", layout="wide")

st.markdown("<h1 style='text-align: center; color: cyan;'>🔧 Smart Predictive Maintenance System</h1>", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []

mode = st.selectbox("🌍 Select Use Case", ["Factory Machine", "Irrigation Pump"])

machine = st.selectbox("🏭 Select Machine", ["Machine A", "Machine B", "Machine C"])

col1, col2, col3 = st.columns([1, 1, 1.2])

with col1:
    st.subheader("⚙️ Machine Inputs")

    temp = st.slider("🌡️ Temperature (°C)", 0, 100, 50)
    vibration = st.slider("📳 Vibration Level", 0, 100, 20)
    pressure = st.slider("🔩 Pressure", 0, 300, 100)
    rpm = st.slider("⚙️ RPM", 0, 5000, 1500)

with col2:
    st.subheader("📊 Prediction Output")

    if st.button("🚀 Analyze Machine"):
        data = np.array([[temp, vibration, pressure, rpm]])
        st.session_state.result = model.predict(data)[0]
        score = max(0, 100 - (vibration + temp/2))
        st.session_state.history.append(score)

    if st.session_state.result is not None:
        score = max(0, 100 - (vibration + temp/2))

        st.markdown("### 🏭 Machine Status")
        if st.session_state.result == 0:
            st.success("🟢 Machine is Healthy")
        else:
            st.error("🔴 High Risk of Failure!")

        st.metric("💡 Health Score", f"{score}%")
        st.progress(score / 100)

        st.markdown("### 🧠 Decision System")
        if score < 40:
            st.error("🚨 ACTION: Stop machine immediately")
        elif score < 70:
            st.warning("⚠️ ACTION: Schedule maintenance")
        else:
            st.success("✅ ACTION: Safe to operate")

        if vibration > 70:
            st.warning("⚠️ High vibration detected!")
        if temp > 80:
            st.warning("🔥 Temperature too high!")

        st.markdown("### 🛠️ Recommendations")
        if vibration > 70:
            st.write("🔧 Check bearings and alignment")
        if temp > 80:
            st.write("❄️ Improve cooling system")
        if pressure > 250:
            st.write("⚠️ Inspect pressure valves")

        if st.session_state.result == 1:
            st.error("⏳ Estimated failure in 2–3 days")

        st.markdown("### 💰 Cost Saving Estimate")
        downtime_cost = 5000
        saved = downtime_cost * 5
        st.write(f"Estimated cost saved: ₹{saved}")

        st.info("🤖 Prediction based on temperature, vibration, pressure, and RPM patterns.")

        if len(st.session_state.history) > 3:
            if st.session_state.history[-1] < st.session_state.history[-2]:
                st.warning("📉 Machine health is declining over time!")

with col3:
    st.subheader("📈 Live Data")

    if st.session_state.result is not None:
        chart_data = pd.DataFrame({
            "Temperature": [],
            "Vibration": []
        })

        chart = st.line_chart(chart_data)

        for i in range(20):
            new_data = pd.DataFrame({
                "Temperature": [temp + np.random.randint(-5, 5)],
                "Vibration": [vibration + np.random.randint(-3, 3)]
            })

            chart.add_rows(new_data)
            time.sleep(0.1)
    else:
        st.info("Click 'Analyze Machine' to start")

st.markdown("---")
st.subheader("📊 Machine Health History")

if len(st.session_state.history) > 0:
    st.line_chart(st.session_state.history)
else:
    st.write("No data yet")

st.markdown("---")
st.markdown("<p style='text-align: center;'>🔧 Smart Industrial Monitoring System</p>", unsafe_allow_html=True)