# Libraries
import streamlit as st
import pandas as pd
import plot_utils
from PIL import Image

# Config
st.set_page_config(page_title='Research Dashboard',
                   page_icon=':bar_chart:', layout='wide')

st.markdown("<h1 style='text-align: center; color: #014b94 ;font-size:50px'>AMCS FACULTY RESEARCH ANALYTICS</h1><hr>",
            unsafe_allow_html=True)

with open('frontend\style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

faculty_info = pd.read_csv('data/faculty_info.csv',header=0)
faculty_data = pd.read_csv('data/faculty_research.csv',header=0,encoding='latin')
faculty_research_domains_data = pd.read_csv('data/faculty_research_areas.csv',header=0)

st.title('FACULTY RESEARCH VISUALS')
st.markdown("<hr>",unsafe_allow_html=True)

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

def display_images():
    st.markdown("<hr>",unsafe_allow_html=True)
    st.header("Word Cloud of the keywords")
    st.markdown("<hr>",unsafe_allow_html=True)
    image = Image.open('images\wordcloud.png')
    st.image(image,caption="Wordcloud")
    st.markdown("<hr>",unsafe_allow_html=True)
    st.header("Cosine Similarity between faculty")
    st.markdown("<hr>",unsafe_allow_html=True)
    image = Image.open('images\cosinesimilarity.png')
    st.image(image,caption="Wordcloud")


faculty_name_list = list(faculty_data['Name'].values)
st.header("Faculty Stats")
display_charts()
display_images()

