import streamlit as st
import os
from datetime import datetime
from GOD_OF_DETECTION import analyze_master_log
from GOD_OF_CHAT import ask
import json

WATCH_DIR = "/data_to_monitor"
MASTER_FILE = "/app/storage/master_log.txt"
RESULT_FILE = "/app/storage/detection_results.json"
HISTORY_DIR = "/app/storage/chat_history"

os.makedirs(HISTORY_DIR, exist_ok=True)

st.set_page_config(page_title="SOC AI Analyst", layout="wide")

st.title("🛡️ AI SOC Log Analyst")

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# Load logs
# ---------------------------

files = []

if os.path.exists(WATCH_DIR):
    for root, _, filenames in os.walk(WATCH_DIR):
        for filename in filenames:
            files.append(os.path.join(root, filename))

selected = st.multiselect("Select log files", files)

# ---------------------------
# Start monitoring
# ---------------------------

if st.button("Start Monitoring"):

    with open(MASTER_FILE, "w") as master:

        for file in selected:

            with open(file, "r", errors="ignore") as f:

                for line in f:
                    master.write(line)

    st.success("Logs loaded to master_log.txt")

# ---------------------------
# CHAT
# ---------------------------

st.subheader("AI SOC Chat")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask about the logs"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Analyzing logs..."):

        data = analyze_master_log(MASTER_FILE)

        reply = ask(
            prompt,
            data,
            st.session_state.history
        )

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
