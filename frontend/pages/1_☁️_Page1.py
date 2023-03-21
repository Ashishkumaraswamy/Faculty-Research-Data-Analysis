# Libraries
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Page 1',
                   page_icon=':bar_chart:', layout='wide')

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
