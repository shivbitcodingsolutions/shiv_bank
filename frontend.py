import streamlit as st
from dotenv import load_dotenv
import requests
import json
import os
from time import sleep
import pandas as pd

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

#get-balance url
get_balance_endpoint = '/get-balance'  
get_balance_url = api_url+get_balance_endpoint

#transaction url
get_transaction_endpoint = '/view-transaction' 
get_transaction_url = api_url+get_transaction_endpoint




st.title("Shiv Bank")

st.subheader("What would you want to do:")

option = st.selectbox("PLEASE SELECT",('CLICK HERE','CREATE ACCOUNT', 'DEPOSIT', 'WITHDRAW', 'GET BALANCE', 'VIEW TRANSACTION'))

st.markdown("------------------------------------------")




if option == 'CLICK HERE':
    st.subheader("Hlo, user wlc to shiv bank")


if option == 'CREATE ACCOUNT':
    
    holder_name = st.text_input("Enter Your Name:")
    account_type = st.selectbox("Enter Account Type", options=["Savings", "Current"])
    initial_deposit = st.number_input("Enter Amount", min_value=0)
    
    if st.button("CREATE"):
        
        if not holder_name:
            st.error("Please enter name first")
            
        elif not holder_name.isalpha():
            st.error("Please enter valid name")
            
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
                # sleep(0.7)
                # st.rerun()
                
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
        


if option == 'DEPOSIT':
    
    account_number = st.number_input("Enter your account number",min_value=0,step=1)
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
                    sleep(0.7)
                    st.rerun()
                    
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
                

if option == 'WITHDRAW':
    
    account_number = st.number_input("Enter your account number",min_value=0,step=1)
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
                ot1 = response.status_code
                
                if ot1 == 404:
                    st.error("Account not found")
                    
                elif ot1 == 400:
                    st.error("Insufficient balance")
                
                else:
                    st.success(f"Withdraw Successfully")
                    sleep(0.7)
                    st.rerun()
                    
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
                

if option == 'GET BALANCE':
    
    account_number = st.number_input("Enter your account number",min_value=0,step=1)
    
    if st.button("SHOW BALANCE"):
        
        if not account_number:
            st.error("Please Enter account number")
            
        elif account_number <=0:
            st.error("Please Enter valid account number")
            
        else:
            
            balance_data = {
                "view_balance_module" : account_number
            }
            
            try:
                response = requests.get(get_balance_url, params=balance_data)
                result = response.json()
                ot1 = response.status_code
                
                if ot1 == 404:
                    st.error("Account not found")
                    
                else:
                    st.success(f"Your Account balance : {result['Your Account balance']}")
                    # sleep(0.7)
                    # st.rerun()
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
                

if option == 'VIEW TRANSACTION':
    
    account_number = st.number_input("Enter your account number",min_value=0,step=1)
    
    if st.button("SHOW TRANSACTION"):
        
        if not account_number:
            st.error("Please Enter account number")
            
        elif account_number <=0:
            st.error("Please Enter valid account number")
            
        else:
            
            transaction_data = {
                "view_transaction_module" : account_number
            }
            
            try:
                response = requests.get(get_transaction_url, params=transaction_data)
                result = response.json()
                ot1 = response.status_code
                
                if ot1 == 404:
                    st.error("Account not found")
                    
                else:
                    df = pd.DataFrame(result)
                    df[['Time-date', 'Transaction-type', 'Amount']] = df['Transaction History'].str.split(' - ', expand=True)
                    df_new = df.drop('Transaction History', axis=1) 
                    # st.dataframe(df_new)
                    st.table(df_new)
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server")
