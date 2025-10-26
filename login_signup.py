import streamlit as st
import pandas as pd
import os

# ---------- SESSION STATE INIT ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Virtual Fashion Stylist - Login/Sign Up", page_icon="👗", layout="centered")

# ---------- CSV FILE SETUP ----------
if not os.path.exists("users.csv"):
    df = pd.DataFrame(columns=["username", "password", "gender", "style", "body_type", "skin_tone"])
    df.to_csv("users.csv", index=False)

# ---------- FUNCTION TO ADD USER ----------
def add_user(username, password, gender, style, body_type, skin_tone):
    df = pd.read_csv("users.csv")
    if username in df['username'].values:
        st.warning("⚠️ Username already exists! Please choose another.")
        return False
    new_user = pd.DataFrame([[username, password, gender, style, body_type, skin_tone]], columns=df.columns)
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv("users.csv", index=False)
    st.success("🎉 Account created successfully! Please login now.")
    return True

# ---------- FUNCTION TO VERIFY USER ----------
def verify_user(username, password):
    try:
        df = pd.read_csv("users.csv")
        if df.empty:
            return False
    except pd.errors.EmptyDataError:
        return False
    user = df[(df['username'] == username) & (df['password'] == password)]
    return not user.empty

# ---------- PAGE SELECTION ----------
page = st.sidebar.radio("Navigation", ["Login", "Sign Up"])

# ---------- LOGIN PAGE ----------
if page == "Login":
    st.title("👗 Virtual Fashion Stylist")
    st.subheader("Welcome Back! Log in to continue ✨")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_user(username.strip(), password.strip()):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username.strip()
            st.success("✅ Login successful! You can now access the main app.")
            st.info("Click here to go to your dashboard 👉 [Open App](./app.py)")
        else:
            st.error("❌ Invalid username or password. Please try again.")

# ---------- SIGN UP PAGE ----------
elif page == "Sign Up":
    st.title("🛍️ Create Your Fashion Profile")
    st.subheader("Join the Virtual Fashion Stylist Family 💕")

    username = st.text_input("Choose Username")
    password = st.text_input("Create Password", type="password")
    gender = st.selectbox("Select Gender", ["Female", "Male"])
    style = st.selectbox("Style Preference", ["Casual", "Party", "Formal", "Traditional"])
    body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Curvy", "Plus-size"])
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dusky", "Deep"])

    if st.button("Create Account"):
        if username.strip() and password.strip():
            add_user(username.strip(), password.strip(), gender, style, body_type, skin_tone)
        else:
            st.warning("⚠️ Please fill all fields before creating an account.")
