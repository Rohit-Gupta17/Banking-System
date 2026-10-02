import streamlit as st

from database import (
    get_customer,
    change_pin
)


def setting_page():

    account_no = st.session_state.account_no
    customer = get_customer(account_no)

    st.title("⚙️ Account Settings")

    st.divider()
    
    st.subheader("👤 Account Details")
    st.write(f"**Account Number:** {customer[1]}")
    st.write(f"**Name:** {customer[2]}")
    st.write(f"**Email:** {customer[3]}")
    st.write(f"**Mobile:** {customer[4]}")
    st.write(f"**Balance:** ₹ {customer[6]:,.2f}")

    st.divider()

    st.subheader("🔑 Change PIN")

    old_pin = st.text_input("Old Pin",type="password",max_chars=4)

    new_pin = st.text_input("New PIN",type="password",max_chars=4)

    confirm_pin = st.text_input("Confirm New PIN",type="password",max_chars=4)

    if st.button("Change PIN"):

        if old_pin == "":
            st.error("Please enter old PIN")

        elif not old_pin.isdigit():
            st.error("Old PIN must contain numbers only")

        elif len(old_pin) != 4:
            st.error("Old PIN must be 4 digits")

        elif new_pin == "":
            st.error("Please enter new PIN")

        elif not new_pin.isdigit():
            st.error("New PIN must contain numbers only")

        elif len(new_pin) != 4:
            st.error("New PIN must be 4 digits")

        elif confirm_pin == "":
            st.error("Please confirm new PIN")
        elif not confirm_pin.isdigit():
            st.error("Confirm PIN must contain numbers only")

        elif len(confirm_pin) != 4:
            st.error("Confirm PIN must be 4 digits")

        elif new_pin != confirm_pin:
            st.error("New PIN and Confirm PIN do not match")

        else:
            success = change_pin(account_no,old_pin,new_pin)

            if success:
                st.success("PIN changed successfully")
            else:
                st.error("Old PIN is incorrect")