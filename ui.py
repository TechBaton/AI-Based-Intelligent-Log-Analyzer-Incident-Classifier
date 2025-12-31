import streamlit as st
import pandas as pd
from collections import defaultdict

from log_parser import parse_logs
from severity import infer_severity, build_incident_index, frequency_boost
from analytics import (
    generate_executive_summary,
    rank_incidents
)


# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(page_title="AI Log Analyzer", layout="wide")

st.title("🧠 AI-Powered Log Analysis System")
st.write("Upload a log file to analyze incidents, severity, and summaries.")

# --------------------------------------------------
# File upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload log file",
    type=["log", "txt"]
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp.log", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Log file uploaded successfully.")

    # --------------------------------------------------
    # Parse logs
    # --------------------------------------------------
    logs = parse_logs("temp.log")

    if len(logs) == 0:
        st.warning("No valid log entries found.")
        st.stop()

    df = pd.DataFrame(logs)

    st.subheader("📄 Parsed Logs (Preview)")
    st.dataframe(df.head(30))
    # --------------------------------------------------
    # Executive summary
    # --------------------------------------------------
    st.subheader("📌 Executive Summary")

    summary = generate_executive_summary(logs)
    st.info(summary)


    # --------------------------------------------------
    # Severity analysis
    # --------------------------------------------------
    st.subheader("Severity Classification")

    severities = []
    for log in logs:
        severity = infer_severity(log["clean_message"])
        severities.append(severity)

    df["severity"] = severities

    severity_counts = df["severity"].value_counts()

    st.bar_chart(severity_counts)

    # --------------------------------------------------
    # Incident summaries
    # --------------------------------------------------
    st.subheader("🧾 Incident Summaries")

    summary_mode = st.radio(
        "Choose summary style:",
        ["Human-readable", "Technical"]
    )

    incident_map = defaultdict(list)

    for log in logs:
        key = (log["service"], log["clean_message"])
        incident_map[key].append(log["timestamp"])

    summaries = []

    for (service, clean_message), timestamps in incident_map.items():
        count = len(timestamps)

        if count < 2:
            continue

        start_time = min(timestamps)
        end_time = max(timestamps)

        if summary_mode == "Human-readable":
            summary_text = (
                f"There were {count} similar issues in the {service} service "
                f"between {start_time} and {end_time}."
            )
        else:
            summary_text = (
                f"{count} occurrences in {service} "
                f"between {start_time} and {end_time} | "
                f"{clean_message[:120]}"
            )

        summaries.append({
            "service": service,
            "count": count,
            "start_time": start_time,
            "end_time": end_time,
            "summary": summary_text
        })

    if summaries:
        summary_df = pd.DataFrame(summaries)
        st.dataframe(summary_df)
    else:
        st.info("No repeated incidents detected.")
     
    # --------------------------------------------------
    # 🎯 What Should I Look At First?
    # --------------------------------------------------
    st.subheader("🎯 What Should I Look At First?")

    ranked = rank_incidents(logs)

    if ranked:
        for i, incident in enumerate(ranked[:3], start=1):
            st.markdown(
                f"**{i}. {incident['service']}**  \n"
                f"Occurrences: {incident['frequency']}  \n"
                f"Last seen: {incident['last_seen']}  \n"
                f"Message: {incident['message']}"
            )
    else:
        st.info("No significant incidents detected.")

    st.success("✅ Analysis complete.")
