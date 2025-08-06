import streamlit as st
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
api_url = os.getenv("BASE_URL")

#create_account url
create_account_endpoint = '/create-account'
create_account_url = api_url+create_account_endpoint 

#deposit url
deposit_endpoint = '/deposit'
deposit_url = api_url+deposit_endpoint

#withdraw url
withdraw_endpoint = '/withdraw'
withdraw_url = api_url+withdraw_endpoint



if 'initial_deposit' not in st.session_state:
    st.session_state.initial_deposit = 0

def handle_initial_deposit():
    st.session_state.initial_deposit = st.session_state.initial_deposit



st.title("Shiv Bank")

st.subheader("What would you want to do:")

option = st.selectbox("PLEASE SELECT",('CLICK HERE','CREATE ACCOUNT', 'DEPOSIT', 'WITHDRAW', 'GET BALANCE', 'VIEW TRANSACTION'))

st.markdown("------------------------------------------")

# st.write(st.session_state.initial_deposit)  



if option == 'CLICK HERE':
    st.subheader("Hlo, user wlc to shiv bank")



if option == 'CREATE ACCOUNT':
    
    holder_name = st.text_input("Enter Your Name:")
    account_type = st.selectbox("Enter Account Type", options=["Savings", "Current"])
    initial_deposit = st.number_input("Enter Amount", key= "initial_deposit", on_change= handle_initial_deposit)
    
    if st.button("CREATE"):
        
        if not holder_name:
            st.error("Please enter name first")
            
        elif initial_deposit <= 0:
            st.error("Please enter valid amount")
        
        else:
            
            account_data = {
                "holder_name" : holder_name,
                "account_type" : account_type,
                "initial_deposit" : initial_deposit
                }
            
            try:
                
                response = requests.post(create_account_url, json=account_data)
                result = response.json()
                ot = result['account_number']
                st.success(f"Account Created Successfully, Your account number: {ot}")
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
        



if option == 'DEPOSIT':
    
    account_number = st.number_input("Enter your account number",min_value=1,step=1)
    amount = st.number_input("Enter amount")
    
    if st.button("DEPOSIT"):
        
        if not account_number:
            st.error("Please Enter account number")
        
        elif account_number <=0:
            st.error("Please Enter valid account number")
            
        elif not amount :
            st.error("Please enter amount")
        
        elif amount <=0:
            st.error("Please enter valid amount")
            
        else:
            
            deposit_data = {
                "account_number" : account_number,
                "amount" : amount
            }
            
            try:
                
                response = requests.put(deposit_url, json=deposit_data)
                result = response.json()
                ot1 = response.status_code
                
                if ot1 == 404:
                    st.error("Account not found")
                
                else:
                    st.success(f"Deposit Successfully")
                    
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
                


if option == 'WITHDRAW':
    
    account_number = st.number_input("Enter your account number",min_value=1, step=1)
    amount = st.number_input("Enter amount")
    
    if st.button("WITHDRAW"):
        
        if not account_number:
            st.error("Please Enter account number")
        
        elif account_number <=0:
            st.error("Please Enter valid account number")
            
        elif not amount :
            st.error("Please enter amount")
        
        elif amount <=0:
            st.error("Please enter valid amount")
            
        else:
            
            withdraw_data = {
                "account_number" : account_number,
                "amount" : amount
            }
            
            try:
                
                response = requests.put(withdraw_url, json=withdraw_data)
                result = response.json()
                ot = result['status_code']
                
                if ot == 404:
                    st.error("Account not found")
                else:
                    st.success(f"Withdraw Successfully")
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
                
