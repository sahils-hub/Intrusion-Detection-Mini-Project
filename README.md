# Cloud-Based Brute Force Attack Detection System

This is a minimal and beginner-friendly mini project demonstrating Cybersecurity (intrusion detection) and Cloud Computing (deployment) concepts.

## Files included
* `app.py`: The main Streamlit application code.
* `logs.csv`: The CSV file used to store all login attempts.
* `requirements.txt`: The Python dependencies required to run the project.

## How to Run Locally

1. **Install Dependencies:**
   Open your terminal/command prompt, navigate to this directory, and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   Start the Streamlit development server using the following command:
   ```bash
   streamlit run app.py
   ```

3. **Access the App:**
   Your default web browser should open automatically. If it doesn't, navigate to `http://localhost:8501`.

4. **Testing:**
   * **Successful Login:** Try logging in with Username `admin` and Password `1234`.
   * **Failed Login:** Try any other combination. 
   * **Intrusion Detection:** Deliberately fail the login 5 times in a row. A brute force warning will appear.

## How to Deploy on Streamlit Cloud

1. **Upload to GitHub:**
   * Create a new repository on [GitHub](https://github.com/).
   * Upload all the files (`app.py`, `logs.csv`, and `requirements.txt`) to your repository.

2. **Deploy the App:**
   * Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
   * Click on **"New app"**.
   * Select your repository, the main branch, and specify `app.py` as the Main file path.
   * Click **"Deploy"**.

3. **Live URL:**
   Once the deployment process completes, you will receive a public URL to share your Cloud-Based Intrusion Detection System!
