import streamlit as st
import re
import string
import random

st.set_page_config(page_title="Password Strength Checker", page_icon="🔐")

st.title("🔐 Password Strength Checker")
st.markdown("### Check your password strength and see how long it takes to crack! 🔍")

password = st.text_input("Enter your password", type="password")

feedback = []  # List to store suggestions

# Function to estimate password crack time
def estimate_crack_time(password, score):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'\d', password): charset += 10
    if re.search(r'[^\w\s]', password): charset += 32  # Special characters

    guesses = charset ** len(password)
    attempts_per_sec = 1e9  # ~1 billion guesses per second
    time_sec = guesses / attempts_per_sec

    if score == 4:  
        return "🟩 **Nearly unbreakable! 🔒**"  # Only for strong passwords
    elif time_sec < 60: 
        return "⚠️ Cracked in **seconds**!"
    elif time_sec < 3600: 
        return "🟡 Cracked in **minutes**!"
    elif time_sec < 86400: 
        return "🟠 Cracked in **hours**!"
    else: 
        return "🟢 Cracked in **years**!"

# Function to generate a strong password
def generate_strong_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(12))

# Password Strength Checking
if password:
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least **8 characters** long.")

    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("🔤 Password should contain **both upper and lower case letters**.")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("🔢 Password should contain **at least one digit**.")

    if re.search(r'[^\w\s]', password):  
        score += 1
    else:
        feedback.append("🔣 Password should contain **at least one special character** (e.g., !@#$%^&*).")

    # Strength Bar
    st.progress(score / 4)

    # Strength Messages
    if score == 4:
        st.success("✅ Your password is **strong!** 🎉")
    elif score == 3:
        st.warning("⚠️ Your password is **moderate**. Try improving it.")
    else:
        st.error("❌ Your password is **weak**. Change it now!")

    # Crack Time Estimation
    st.markdown(f"**⏳ Estimated Crack Time:** {estimate_crack_time(password, score)}")

    # Display Improvement Suggestions
    if feedback:
        st.markdown("### 🛠️ Improvement Suggestions")
        for tip in feedback:
            st.write(tip)

    # Strong Password Suggestion
    if score < 3:
        st.info(f"💡 Try this **stronger** password: `{generate_strong_password()}`")

else:
    st.info("🔑 Enter your password to check its strength!")
