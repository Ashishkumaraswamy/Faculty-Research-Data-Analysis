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
research_paper_topic_data=pd.read_csv('data/faculty_research_paper_keywords.csv',header=0)
faculty_research_area=pd.read_csv('data/faculty_research_areas.csv',header=0)

def preprocessing():
    research_paper_topic_matrix=research_paper_topic_data.drop(['Citations_All','H-Index_All','i10-Index_All','Journal Description','No. of Journals','Title And Description','Word Count'],axis=1)
    faculty_topic = research_paper_topic_matrix.set_index('Name').drop('Journals',axis=1)
    faculty_topic = faculty_topic.sum(level=0)
    return faculty_topic

def search_by_keywords():
    topics = list(faculty_topic.columns)
    selected_keyword = st.selectbox("Select Keyword",topics)
    matched_faculty=[]
    for idx,row in faculty_topic.iterrows():
        if row[selected_keyword]>0:
            matched_faculty.append(idx)
    df=pd.DataFrame()
    df['Faculty Match']=matched_faculty
    st.dataframe(df)

def search_by_domain():
    research_areas=set(faculty_research_area['Research Areas'].values)
    selected_domain = st.selectbox("Select Domain", research_areas)
    matched_faculty = []
    for idx,row in faculty_research_area.iterrows():
        if row['Research Areas']==selected_domain:
            matched_faculty.append(row['Name'])
    df=pd.DataFrame()
    df['Faculty Match']=matched_faculty
    st.dataframe(df)


faculty_topic= preprocessing()
print(faculty_topic.head())
st.title('FACULTY SEARCH')
st.markdown("<hr>",unsafe_allow_html=True)
selected_feature=st.radio('Search by',['Keywords','Research Domain'])
if selected_feature=='Keywords':
    search_by_keywords()
else:
    search_by_domain()