import streamlit as st
import re

from database import register_acc

def reg():
    
    st.title("🖋CREATE BANK ACCOUNT")
    
    st.divider()
    
    name=st.text_input("enter ther customer name")
    email=st.text_input("enter the custoner email")
    mobile=st.text_input("enter mobile number",max_chars=10)
    pin=st.text_input("enetr the pin",type="password",max_chars=4)
    confirm_pin=st.text_input("enter the confirm pin",type="password",max_chars=4)
    
    st.subheader("opening deposite")
    
    amount=st.number_input("enter deposite amount",min_value=500,value=500,step=100)
    
    st.divider()
    
    if st.button("Generated Account"):
        
        if name == "":
            st.error("please enter name")
        
        elif not all(word.isalpha() for word in name.split()):
            st.error("Name must contain only letters and spaces")
            
        elif email=="":
            st.error("please enter email")
        elif not re.match(r"^[A-Za-z0-9._%+-]+@gmail\.com$",email):
            st.error("Please enter a valid Gmail address")
        
        elif mobile=="":
            st.error("please enter mobile number")
        elif not mobile.isdigit():
            st.error("only number use")
        elif len(mobile)!=10:
            st.error("Mobile number must be exactly 10 digits")
            
        elif pin == "":
            st.error("please enter pin")
        elif not pin.isdigit():
            st.error("pin must contain only numbers")
        elif len(pin) != 4:
            st.error("pin must be exactly 4 digits")


        elif confirm_pin == "":
            st.error("please confirm your pin")
        elif not confirm_pin.isdigit():
            st.error("confirm pin must contain only numbers")
        elif len(confirm_pin) != 4:
            st.error("Confirm PIN must be exactly 4 digits")

        elif pin != confirm_pin:
            st.error("PIN and Confirm PIN do not match")


        elif amount < 500:
            st.error("Minimum opening deposit is ₹500")

        else:
            success, result = register_acc(name,email,mobile,pin,amount)

            if success:

                st.success("account created successfully!")

                st.success(f"your Account Number: {result}")

                st.success(f"opening Balance: ₹{amount:,.2f}")

                st.info("please save your account number for login.")

            else:

                st.error(result)