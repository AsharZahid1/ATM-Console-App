import streamlit as st
import time

# Account class to handle user data and operations
class Account:
    def __init__(self, account_number, pin, balance):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

    def validate_pin(self, entered_pin):
        return self.pin == entered_pin

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def get_balance(self):
        return self.balance

# Predefined accounts
accounts = [
    Account("12345", "1111", 1500.50),
    Account("67890", "2222", 300.00)
]

# Session state for persistent login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.account = None

st.title("🏧 Console ATM (Streamlit Version)")

def loading_animation(text="Loading"):
    with st.spinner(text + "..."):
        time.sleep(1.5)

# Login form
if not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("🔐 Login")
        acc_num = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            for acc in accounts:
                if acc.account_number == acc_num and acc.validate_pin(pin):
                    st.session_state.logged_in = True
                    st.session_state.account = acc
                    loading_animation("Logging in")
                    st.success("Login successful!")
                    st.experimental_rerun()
            st.error("Invalid account number or PIN.")

# Main menu
else:
    st.success("You are logged in!")
    st.subheader("💳 ATM Menu")
    option = st.radio("Choose an option:", ("Check Balance", "Deposit", "Withdraw", "Logout"))

    if option == "Check Balance":
        st.info(f"💰 Current Balance: ${st.session_state.account.get_balance():.2f}")

    elif option == "Deposit":
        deposit_amt = st.number_input("Enter amount to deposit:", min_value=0.01, step=0.01)
        if st.button("Deposit"):
            st.session_state.account.deposit(deposit_amt)
            st.success("Deposit successful!")

    elif option == "Withdraw":
        withdraw_amt = st.number_input("Enter amount to withdraw:", min_value=0.01, step=0.01)
        if st.button("Withdraw"):
            if st.session_state.account.withdraw(withdraw_amt):
                st.success("Withdrawal successful!")
            else:
                st.error("Insufficient funds.")

    elif option == "Logout":
        loading_animation("Logging out")
        st.session_state.logged_in = False
        st.session_state.account = None
        st.success("Logged out successfully.")
        st.experimental_rerun()
