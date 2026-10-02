
import streamlit as st

from database import bank_table
from registration import reg

from login import login

from dashboard import atm_dashboard

from setting import setting_page



st.set_page_config(
    page_title="ATM Banking System",
    page_icon="🏦",
    layout="wide"
)


bank_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account_no" not in st.session_state:
    st.session_state.account_no = None

if not st.session_state.logged_in:
    st.sidebar.title("ATM Banking")

    menu = st.sidebar.radio("Menu",["Login","Registration"])

    if menu == "Login":
        st.image("image\image_login.avif",width="stretch")
        login()

    elif menu == "Registration":
        
            st.image("image\image_bank.avif",width="stretch", caption="Personal Bank")
            reg()

else:

    st.sidebar.title("ATM Banking")

    menu = st.sidebar.radio("Menu",["ATM Dashboard","Settings"])

    if menu == "ATM Dashboard":
        atm_dashboard()

    elif menu == "Settings":
        setting_page()