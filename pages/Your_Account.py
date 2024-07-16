import streamlit as st
# Set the page configuration
st.set_page_config(
    page_title="Home: GLOBE GURU",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)
import base64
import sqlite3
import smtplib
import random
import string
import re
from session_state import SessionState, get_session_state
import os
from pages import Home

# Function to encode image to base64
@st.cache_data
def get_base64_image(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your image
img_file = os.path.join("images","styling.jpg")
img_base64 = get_base64_image(img_file)

# Custom CSS for watermark effect
page_bg_img = f'''
<style>
body {{
background-image: url("data:image/png;base64,{img_base64}");
background-size: cover;
background-repeat: no-repeat;
opacity: 0.94;  
}}
</style>
'''

# Inject CSS into Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT UNIQUE,
            is_verified INTEGER DEFAULT 0,
            otp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def send_otp(email, otp):
    # Configure your email details here
    sender_email = "abhirupbasu30@gmail.com"
    sender_password = "uiwq yyca kaas jtbv"
    receiver_email = email
    subject = "Your OTP Verification Code"
    body = f"Your OTP is: {otp}"
    message = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    except Exception as e:
        st.error("Failed to send email. Check your email settings.")

def generate_otp():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, password, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
    conn.commit()
    conn.close()

def update_otp(username, otp):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET otp = ? WHERE username = ?', (otp, username))
    conn.commit()
    conn.close()

def verify_otp(username, otp):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND otp = ?', (username, otp))
    user = cursor.fetchone()
    if user:
        cursor.execute('UPDATE users SET is_verified = 1 WHERE username = ?', (username,))
        conn.commit()
    conn.close()
    return user

def reset_password(username, new_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()

class EmailNotValidError(Exception):
    pass

def validate_email(email):
    # Basic pattern for validating an email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise EmailNotValidError("Invalid email address")
    return email

# Update the main function to check login status and handle redirection

def main(session_state):
    # Initialize session state variables if not present
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

    if 'otp_sent' not in st.session_state:
        st.session_state['otp_sent'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ""

    # Show content only if logged in
    if st.session_state['is_logged_in']:
        st.sidebar.title("MENU")
        st.sidebar.image(os.path.join("images","logo.jpg"), use_column_width=True)
        st.markdown("""
            <div style="background-color:#2f3e46; padding:5px;">
            <h1 style="color:#cad2c5">GLOBE GURU</h1>
            </div>
            """, unsafe_allow_html=True)
        
        st.warning("Remember To Logout After You are done with your Session")
        if st.button("Logout"):
            st.session_state['is_logged_in'] = False
            st.info("You Have Been Logged out Successfully!")
        # Show Home page content
        st.write("Welcome to the Home Page")
        # You can include Home page content or other logic here

    else:
        title_template = """
        <div style="background-color:#2f3e46; padding:5px;">
        <h1 style="color:#cad2c5">GLOBE GURU</h1>
        </div>
        """
        st.sidebar.title("MENU")
        st.sidebar.image(os.path.join("images","logo.jpg"), use_column_width=True)
        st.markdown(title_template, unsafe_allow_html=True)

        # Navigation
        menu = ["Login", "SignUp", "Reset Password"]
        choice = st.selectbox("Menu", menu)
        st.markdown("<hr>", unsafe_allow_html=True)

        if choice == "Login":
            username = st.text_input("User Name")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                st.markdown("<hr>", unsafe_allow_html=True)
                with st.spinner("Please wait"):
                    user = validate_user(username, password)
                    if user:
                        otp = generate_otp()
                        update_otp(username, otp)
                        send_otp(user[3], otp)
                        st.session_state['otp_sent'] = True
                        st.session_state['username'] = username
                        st.success("OTP sent to your email address. Please verify.")
                    else:
                        st.error("Invalid Username or Password")

            if st.session_state['otp_sent']:
                otp_input = st.text_input("Enter OTP", max_chars=6)
                if st.button("Verify OTP"):
                    st.markdown("<hr>", unsafe_allow_html=True)
                    verified_user = verify_otp(st.session_state['username'], otp_input)
                    if verified_user:
                        st.success(f"Welcome {st.session_state['username']}")
                        st.session_state['otp_sent'] = False
                        st.session_state['is_logged_in'] = True
                        st.switch_page("pages/Home.py")
                    else:
                        st.error("Invalid OTP. Please try again.")
            st.markdown("<hr>", unsafe_allow_html=True)

        elif choice == "SignUp":
            st.subheader("Create New Account")
            username = st.text_input("User Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')
            password_confirmation = st.text_input("Confirm Password", type='password')

            if password != password_confirmation:
                st.warning("Passwords do not match")

            if st.button("SignUp"):
                st.markdown("<hr>", unsafe_allow_html=True)
                try:
                    validate_email(email)
                    create_user(username, password, email)
                    st.success("Account created successfully")
                    st.info("Go to the Login Menu to login")
                except EmailNotValidError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        elif choice == "Reset Password":
            st.subheader("Reset Password")
            username = st.text_input("User Name")
            new_password = st.text_input("New Password", type='password')
            password_confirmation = st.text_input("Confirm New Password", type='password')

            if new_password != password_confirmation:
                st.warning("Passwords do not match")

            if st.button("Reset Password"):
                st.markdown("<hr>", unsafe_allow_html=True)
                if new_password == password_confirmation:
                    reset_password(username, new_password)
                    st.success("Password reset successfully")
                else:
                    st.error("Password reset failed. Please try again.")


if __name__ == "__main__":
    init_db()
    main(SessionState)
