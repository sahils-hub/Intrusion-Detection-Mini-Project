import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

# --- Configuration & Setup ---
st.set_page_config(page_title="Intrusion Detection System", page_icon="🛡️")

LOG_FILE = "logs.csv"

def init_log_file():
    """Ensures the log file exists with appropriate headers."""
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        df = pd.DataFrame(columns=["timestamp", "username", "status"])
        df.to_csv(LOG_FILE, index=False)

def log_attempt(username, status):
    """Saves a login attempt to the CSV log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame({
        "timestamp": [timestamp], 
        "username": [username if username else "UNKNOWN"], 
        "status": [status]
    })
    new_entry.to_csv(LOG_FILE, mode='a', header=False, index=False)

def check_brute_force():
    """Checks if the last 5 log entries are failed attempts and within the 30-second lockout period."""
    try:
        df = pd.read_csv(LOG_FILE)
        if len(df) >= 5:
            recent_logs = df.tail(5)
            # Check if all of the last 5 attempts are failures
            if (recent_logs["status"] == "failed").sum() >= 5:
                # Get the time of the most recent failed attempt
                last_attempt_str = recent_logs.iloc[-1]["timestamp"]
                last_attempt_time = datetime.strptime(last_attempt_str, "%Y-%m-%d %H:%M:%S")
                
                # Lockout duration: 30 seconds
                time_since_last_fail = (datetime.now() - last_attempt_time).total_seconds()
                if time_since_last_fail < 30:
                    return True
    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError, KeyError):
        pass
    return False

def send_telegram_alert():
    """Sends an alert message to a Telegram chat using Streamlit secrets."""
    try:
        # Fetch credentials from Streamlit Secrets
        bot_token = st.secrets["bot_token"]
        chat_id = st.secrets["chat_id"]
        
        message = "⚠️ *Intrusion Detected!*\nMultiple failed login attempts have been recorded on the system."
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id, 
            "text": message,
            "parse_mode": "Markdown"
        }
        
        # Send the request to Telegram API
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        # If secrets are missing or network fails, we catch the error to prevent app crash
        print(f"Failed to send Telegram alert: {e}")

# Initialize the log file on app startup
init_log_file()

# --- UI Layout ---
st.title("🛡️ Intrusion Detection System (Mini Project)")
st.markdown("### Cloud-Based Brute Force Attack Detection")
st.write("Welcome to the Intrusion Detection System demonstrator.")

# --- Intrusion Detection Alert ---
# Initialize session state for the alert to prevent spamming
if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False

# We check this before the login so it persists if the page reloads, 
# but it will update dynamically after a login attempt.
brute_force_detected = check_brute_force()

if brute_force_detected:
    # Send alert only once per attack
    if not st.session_state.alert_sent:
        send_telegram_alert()
        st.session_state.alert_sent = True
        
    st.error("⚠️ **Possible Brute Force Attack Detected!** Account is temporarily locked for 30 seconds.")
else:
    # Reset alert state so the next attack can trigger a new alert
    st.session_state.alert_sent = False

# --- Login Section ---
st.subheader("Login Portal")
st.info("💡 **Hint:** Use Username `admin` and Password `1234` for a successful login.")

with st.form("login_form", clear_on_submit=True):
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Login")

if submit_button:
    if brute_force_detected:
        st.error("🔒 **Account Locked:** Please wait 30 seconds before trying again.")
    else:
        if username_input.strip() == "admin" and password_input.strip() == "1234":
            st.success(f"✅ Login Successful! Welcome, {username_input.strip()}.")
            log_attempt(username_input.strip(), "success")
        else:
            st.error("❌ Login Failed! Invalid credentials.")
            log_attempt(username_input.strip(), "failed")
            
        # Re-check brute force status after the new attempt
        if check_brute_force() and not brute_force_detected:
            st.rerun()

st.divider()

# --- Display Logs ---
st.subheader("Login Activity Dashboard")
try:
    logs_df = pd.read_csv(LOG_FILE)
    if not logs_df.empty:
        # --- Metrics Row ---
        total_attempts = len(logs_df)
        success_count = len(logs_df[logs_df['status'] == 'success'])
        failed_count = len(logs_df[logs_df['status'] == 'failed'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Attempts", total_attempts)
        col2.metric("✅ Successful", success_count)
        col3.metric("❌ Failed", failed_count)
        
        st.write("") # Spacer
        
        # --- Visual Analytics & Data Table ---
        col_chart, col_data = st.columns([1, 1.2])
        
        with col_chart:
            st.markdown("#### 📊 Statistics")
            # Create a dataframe for the chart to enable colors
            chart_data = pd.DataFrame({
                "Status": logs_df['status'].value_counts().index,
                "Count": logs_df['status'].value_counts().values
            })
            st.bar_chart(chart_data, x="Status", y="Count", color="Status")
            
        with col_data:
            st.markdown("#### 📝 Recent Logs")
            st.dataframe(logs_df.iloc[::-1], use_container_width=True, hide_index=True, height=320)
    else:
        st.info("No logs available yet.")
except (FileNotFoundError, pd.errors.EmptyDataError):
    st.info("No logs available yet.")
