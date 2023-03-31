# Libraries
import streamlit as st
import pandas as pd

# Config
st.set_page_config(page_title='Research Dashboard',
                   page_icon=':bar_chart:', layout='wide')

st.markdown("<h1 style='text-align: center; color: #014b94 ;font-size:50px'>AMCS FACULTY RESEARCH ANALYTICS</h1><hr>",
            unsafe_allow_html=True)

with open('frontend\style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

faculty_data = pd.read_csv('data/faculty_info.csv',header=0)
faculty_research_data = pd.read_csv('data/faculty_research.csv',header=0,encoding='latin')
faculty_research_domains_data = pd.read_csv('data/faculty_research_areas.csv',header=0)

def display_faculty_stats(selected_faculty):
    faculty_info = faculty_data[faculty_data['Name']==selected_faculty]
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total No. of Journals Published",faculty_info['No. of Journals'].sum(),0)
    with col2:
        st.metric("Total No. of Citations Received",faculty_info['Citations_All'].sum(),0)
    with col3:
        st.metric("Total H-Index",faculty_info['H-Index_All'].sum(),0)

def display_research_papers(selected_faculty):
    research_data = faculty_research_data[faculty_research_data['Name']==selected_faculty]
    for i in range(len(research_data)):
        st.write(str(i+1)+". "+research_data.iloc[i]['Journals'])
        with st.expander('See Description'):
            st.write(research_data.iloc[i]['Journal Description'])

def faculty_research_domains(selected_faculty):
    research_domains = faculty_research_domains_data[faculty_research_domains_data['Name']==selected_faculty]
    st.header("Research Area Domains")
    for i in research_domains['Research Areas'].values:
        st.markdown("- {}".format(i))

st.title('FACULTY WISE DATA')
st.markdown("<hr>",unsafe_allow_html=True)

faculty_name_list = list(faculty_data['Name'].values)
selected_faculty= st.selectbox('Select a faculty',faculty_name_list)
st.markdown("<hr>",unsafe_allow_html=True)
st.header("Faculty Stats")
st.text("")
display_faculty_stats(selected_faculty)
st.markdown("<hr>",unsafe_allow_html=True)
faculty_research_domains(selected_faculty)
if selected_faculty in faculty_data['Name'].values:
    st.header("Research Papers Published")
    st.markdown("<hr>",unsafe_allow_html=True)
    display_research_papers(selected_faculty)
