import streamlit as st
from broker import get_balance

st.title("Algo Trading Dashboard")

balance = get_balance()

st.metric("Account Balance",balance)