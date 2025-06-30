import streamlit as st
import json
import os

# --- Load credentials ---
def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

# --- Authenticate user ---
def login(username, password, creds):
    return username in creds and creds[username]["password"] == password

# --- Load reports ---
def load_report(report_filename):
    with open(os.path.join("reports", report_filename), "r") as f:
        return f.read()

# --- Main App ---
def main():
    st.set_page_config(page_title="Client Security Dashboard", layout="centered")

    creds = load_credentials()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Client Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password, creds):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials.")
    else:
        st.title(f"🔍 Welcome, {st.session_state.username}")

        report_options = {
            "Web Scan Summary": "webreport1.md",
            "Vulnerability Timeline": "report2.md",
            "Top Exploitable Paths": "report3.md",
            "Remediation Recommendations": "report4.md"
        }

        selected = st.selectbox("Select a report to view:", list(report_options.keys()))
        report_content = load_report(report_options[selected])
        st.markdown(report_content, unsafe_allow_html=True)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
