import streamlit as st

from database import customer_login


def login():

    st.title("🔐 ATM Login")

    st.divider()

    account_no = st.text_input("Account Number")

    pin = st.text_input("pin",type="password",max_chars=4)

    if st.button("Login"):

        if account_no == "":
            st.error("Please enter account number")

        elif not account_no.isdigit():
            st.error("Account number must contain numbers only")

        elif pin == "":
            st.error("please enter pin")

        elif not pin.isdigit():
            st.error("pin must contain numbers only")

        elif len(pin) != 4:
            st.error("pin must be 4 digits")

        else:
            customer = customer_login(int(account_no),pin)

            if customer:
                st.session_state.logged_in = True
                st.session_state.account_no = int(account_no)

                st.success("login successful")

                st.rerun()

            else:
                st.error("invalid account number or pin")