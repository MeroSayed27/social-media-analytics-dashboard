import streamlit as st
import requests
import pandas as pd

st.title("📊 Social Media Analytics Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    st.write("Uploading to FastAPI...")

    files = {"file": uploaded_file.getvalue()}

    response = requests.post(
        "http://127.0.0.1:8000/upload-csv",
        files={"file": uploaded_file}
    )

    if response.status_code == 200:
        data = response.json()

        st.subheader("📌 Basic Info")
        st.write(f"Rows: {data['rows']}")
        st.write(f"Columns: {data['columns']}")

        st.subheader("📊 Analytics")
        st.json(data["analytics"])

        st.subheader("🤖 ML Prediction")
        st.json(data["ml_prediction"])

    else:
        st.error("Backend error")