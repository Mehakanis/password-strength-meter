import streamlit as st
import re
import string
import random

st.set_page_config(page_title="Password Strength Checker", page_icon="🔐")

st.title("🔐 Password Strength Checker")
st.markdown("### Check your password strength and see how long it takes to crack! 🔍")

password = st.text_input("Enter your password", type="password")

# Function to estimate password crack time
def estimate_crack_time(password, score):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26 #small letters hain to 26 add hojayega charset mai
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'\d', password): charset += 10
    if re.search(r'[^\w\s]', password): charset += 32  # Special characters

#Total number of possible combinations for the given password.
    guesses = charset ** len(password)
    attempts_per_sec = 1e9  # ~1 billion guesses per second

    #Calculates the estimated crack time in seconds.
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
    chars = string.ascii_letters + string.digits + "!@#$%^&*" #Creates a list of letters (A-Z, a-z), numbers (0-9), and special characters.

    #''. join Combines the selected characters into a single password string.

    return ''.join(random.choice(chars) for _ in range(12)) #Picks 12 random characters from the list.


# Password Strength Checking
if password:
    score = sum([
        len(password) >= 8,
        bool(re.search(r'[A-Z]', password) and re.search(r'[a-z]', password)),
        bool(re.search(r'\d', password)),
        bool(re.search(r'[^\w\s]', password))
    ])

    # Strength Bar
    st.progress(score / 4)

    # Strength Messages
    if score == 4:
        st.success("✅ Your password is **strong!** 🎉")
    elif score == 3:
        st.warning("⚠️ Your password is **moderate**. Try improving it.")
    else:
        st.error("❌ Your password is **weak**. Change it now!")

    # Crack Time Estimation (Only "Nearly unbreakable" for strong passwords)
    st.markdown(f"**⏳ Estimated Crack Time:** {estimate_crack_time(password, score)}")

    # Strong Password Suggestion
    if score < 3:
        st.info(f"💡 Try this **stronger** password: `{generate_strong_password()}`")

else:
    st.info("🔑 Enter your password to check its strength!")
