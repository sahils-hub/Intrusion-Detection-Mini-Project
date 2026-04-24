import streamlit as st
import pandas as pd
from datetime import datetime
import os

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

# Initialize the log file on app startup
init_log_file()

# --- UI Layout ---
st.title("🛡️ Intrusion Detection System (Mini Project)")
st.markdown("### Cloud-Based Brute Force Attack Detection")
st.write("Welcome to the Intrusion Detection System demonstrator.")

# --- Intrusion Detection Alert ---
# We check this before the login so it persists if the page reloads, 
# but it will update dynamically after a login attempt.
brute_force_detected = check_brute_force()

if brute_force_detected:
    st.error("⚠️ **Possible Brute Force Attack Detected!** Account is temporarily locked for 30 seconds.")

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
st.subheader("Login Activity Logs")
try:
    logs_df = pd.read_csv(LOG_FILE)
    if not logs_df.empty:
        # --- Visual Analytics Dashboard ---
        st.markdown("#### 📊 Login Statistics")
        status_counts = logs_df['status'].value_counts()
        st.bar_chart(status_counts)
        
        # Display logs in reverse order (newest first)
        st.markdown("#### 📝 Recent Logs")
        st.dataframe(logs_df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("No logs available yet.")
except (FileNotFoundError, pd.errors.EmptyDataError):
    st.info("No logs available yet.")
