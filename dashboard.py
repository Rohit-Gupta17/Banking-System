import streamlit as st

from database import (
    get_customer,
    deposite,
    withdraw,
    transaction_history
)


def atm_dashboard():
    account_no = st.session_state.account_no

    customer = get_customer(account_no)
    

    st.title("🏦 ATM Dashboard")

    st.write(f"### Welcome, {customer[2]}")

    st.write(f"Account Number: **{customer[1]}**")

    st.divider()

    st.metric("Current Balance",f"₹ {customer[6]:,.2f}")

    st.divider()

    menu = st.sidebar.radio(
        "Select ATM Service",
        [
            "Check Balance",
            "Deposit",
            "Withdraw",
            "Transaction History"
        ]
    )

    if menu == "Check Balance":

        customer = get_customer(account_no)

        st.subheader("Check Balance")
        st.success(f"Available Balance: ₹ {customer[6]:,.2f}")

    elif menu == "Deposit":

        st.subheader("Deposit Money")

        amount = st.number_input("Enter Deposit Amount",min_value=1.0,step=100.0)

        if st.button("Deposit Money"):

            success = deposite(account_no,amount)

            if success:
                st.success(f"₹ {amount:,.2f} deposited successfully!")

                st.rerun()

            else:
                st.error("Deposit failed")

    elif menu == "Withdraw":

        st.subheader("Withdraw Money")

        amount = st.number_input("Enter Withdrawal Amount",min_value=1.0,step=100.0)

        if st.button("Withdraw Money"):

            success, message = withdraw(account_no,amount)

            if success:

                st.success(f"₹ {amount:,.2f} withdrawn successfully!")

                st.rerun()

            else:
                st.error(message)


    elif menu == "Transaction History":

        st.subheader("Transaction History")

        transactions =transaction_history(account_no)

        if transactions:
            transaction_data=[]
            for transaction in transactions:
                transaction_data.append({
                    "Transaction Type": transaction[0],
                    "Amount": f"₹ {transaction[1]:,.2f}",
                    "Balance": f"₹ {transaction[2]:,.2f}",
                    "Date": transaction[3]
                })
            
            st.dataframe(transaction_data,use_container_width=True,hide_index=True)
        # if transactions:
            
        #     for transaction in transactions:
        #         transaction_type = transaction[0]
        #         amount = transaction[1]
        #         balance = transaction[2]
        #         date = transaction[3]

        #         st.write(f"**{transaction_type}**")
        #         st.write(f"Amount: ₹ {amount:,.2f}")
        #         st.write(f"Balance: ₹ {balance:,.2f}")
        #         st.write(f"Date: {date}")
                
                

        #         st.divider()

        else:
            st.info("No transactions found")

    st.divider()

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.account_no = None

        st.rerun()