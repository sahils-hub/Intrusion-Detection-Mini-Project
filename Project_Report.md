# Project Report: Cloud-Based Brute Force Attack Detection System

## 1. Project Overview
The **Cloud-Based Brute Force Attack Detection System** is a lightweight, interactive web application designed to demonstrate fundamental Cybersecurity and Cloud Computing concepts. It simulates a secure login portal that actively monitors, records, and analyzes user login attempts to detect and mitigate automated password-guessing attacks (Brute Force attacks).

## 2. Problem Statement
In modern web applications, unauthorized access attempts through brute force attacks are a significant threat. Attackers use automated scripts to rapidly guess passwords until they find the correct one. This project aims to demonstrate how such attacks can be detected in real-time and how simple mitigation strategies (like account lockouts) can protect a system.

## 3. Technology Stack
The project is built entirely in Python, utilizing the following libraries and platforms:
* **Frontend/UI:** Streamlit (Provides a rapid, interactive web-based user interface)
* **Data Processing:** Pandas (Used for parsing, filtering, and analyzing log data)
* **Storage:** CSV (Comma-Separated Values) file used as a lightweight database (`logs.csv`)
* **Deployment (Cloud):** Streamlit Community Cloud (Platform-as-a-Service for hosting the application globally)

## 4. Core Features

### A. Logging & Auditing
Every login attempt—whether successful or failed—is recorded in a permanent log file (`logs.csv`). The system captures:
* **Timestamp:** The exact date and time of the attempt.
* **Username:** The username entered by the user (automatically stripped of accidental spaces).
* **Status:** Whether the attempt resulted in a 'success' or a 'failed' login.

### B. Real-Time Intrusion Detection
The core logic of the system analyzes the log file on every interaction. If the system detects **5 consecutive failed login attempts**, it flags this behavior as a "Possible Brute Force Attack." 

### C. Time-Based Account Lockout Mechanism
As a defensive countermeasure, once a brute force attack is detected, the system immediately **locks the login portal for 30 seconds**. During this lockout period:
* The system refuses to process any passwords.
* No further failed attempts are logged, preventing attackers from overloading the database.
* A warning message is displayed to the user.
* Once the 30 seconds expire, the system automatically unlocks.

### D. Visual Analytics Dashboard
The application features an interactive dashboard that reads the log data and generates a real-time Bar Chart. This provides administrators with a visual representation of login statistics (e.g., comparing the volume of failed attempts vs. successful logins).

## 5. System Workflow
1. **User Input:** The user enters credentials into the web form.
2. **Pre-Check (Security):** Before processing, the system reads the last 5 entries in `logs.csv` and checks the timestamps. If 5 consecutive failures occurred within the last 30 seconds, the system halts and displays a Lockout Warning.
3. **Authentication:** If the system is unlocked, it verifies the credentials against the hardcoded database (Username: `admin`, Password: `1234`).
4. **Logging:** The result (Success/Fail) is appended to `logs.csv`.
5. **UI Update:** The page dynamically updates the Visual Analytics chart and the Recent Logs table to reflect the new entry.

## 6. Concepts Demonstrated
* **Cybersecurity (Intrusion Detection):** Demonstrates heuristic-based threat detection (identifying patterns of malicious behavior rather than specific known threats).
* **Cybersecurity (Mitigation):** Demonstrates rate-limiting and account lockout defenses.
* **Cloud Computing (SaaS/PaaS):** Demonstrates how a local Python script can be packaged, uploaded to GitHub, and continuously deployed as a Cloud service accessible via a public URL.

## 7. Future Scope
While this is a mini-project, the architecture can be expanded into a production-ready system by:
1. Replacing the CSV file with a robust Cloud Database (e.g., PostgreSQL or Firebase).
2. Implementing IP Address tracking and Geo-location mapping.
3. Adding Email or SMS alerts to notify administrators the moment an attack is detected.
4. Integrating password hashing (e.g., bcrypt) instead of plaintext password verification.
