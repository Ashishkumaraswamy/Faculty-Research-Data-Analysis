# Libraries
import streamlit as st
import pandas as pd
import plot_utils

# Config
st.set_page_config(page_title='Research Dashboard',
                   page_icon=':bar_chart:', layout='wide')

st.markdown("<h1 style='text-align: center; color: #014b94 ;font-size:50px'>AMCS FACULTY RESEARCH ANALYTICS</h1><hr>",
            unsafe_allow_html=True)
# Style
with open('frontend\style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
faculty_info=pd.read_csv('data/faculty_info.csv',header=0)

def display_metrics():
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total No. of Journals Published",faculty_info['No. of Journals'].sum(),0)
    with col2:
        st.metric("Total No. of Citations Received",faculty_info['Citations_All'].sum(),0)
    with col3:
        st.metric("Total H-Index",faculty_info['H-Index_All'].sum(),0)
    faculty_metric_col1,faculty_metric_col2,faculty_metric_col3=st.columns(3)
    with faculty_metric_col1:
        st.metric('Total No. of Faculties published Journals',len(faculty_info),0)
    with faculty_metric_col2:
        st.metric('Avg no. of Journals Published by a faculty',round(faculty_info['No. of Journals'].sum()/len(faculty_info)),0)
    with faculty_metric_col3:
        st.metric('Faculties published more than 15 journals',len(faculty_info[faculty_info['No. of Journals']>=15]),0)

def display_charts():
    st.markdown("<hr>",unsafe_allow_html=True)
    st.header("No. of Journals Published By Faculty")
    fig = plot_utils.bargraph(faculty_info['Name'],
                              faculty_info['No. of Journals'], 'No. of Journals', 'Name', 'Journals')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.header("H-Index of Faculties")
    fig1= plot_utils.bargraph(faculty_info['Name'],
                              faculty_info['H-Index_All'], 'H-Index', 'Name', 'H-Index')
    st.plotly_chart(fig, use_container_width=True)

def display_faculty_info_table():
    faculty_info_props=faculty_info.drop('Research Areas',axis=1)
    st.table(faculty_info_props)

st.title('FACULTY RESEARCH DASHBOARD')
st.markdown("<hr>",unsafe_allow_html=True)
st.header("FACULTY LIST AND DETAILS")
st.markdown("<hr>",unsafe_allow_html=True)
display_faculty_info_table()
st.markdown("<hr>",unsafe_allow_html=True)
st.header("AMCS RESEARCH STATISTICS")
st.markdown("<hr>",unsafe_allow_html=True)
display_metrics()
display_charts()