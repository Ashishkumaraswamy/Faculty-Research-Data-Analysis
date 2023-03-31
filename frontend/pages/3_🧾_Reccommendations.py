# Libraries
import streamlit as st
import pandas as pd
import numpy as np

# Config
st.set_page_config(page_title='Research Dashboard',
                   page_icon=':bar_chart:', layout='wide')

st.markdown("<h1 style='text-align: center; color: #014b94 ;font-size:50px'>AMCS FACULTY RESEARCH ANALYTICS</h1><hr>",
            unsafe_allow_html=True)

with open('frontend\style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

faculty_data = pd.read_csv('data/faculty_info.csv',header=0)
research_paper_topic_data=pd.read_csv('data/faculty_research_paper_keywords.csv',header=0)

def cosine_similarity_matrix(df):
    data = df.to_numpy()
    m, n = df.shape
    distances = np.zeros((m,m))
    for i in range(m):
        for j in range(m):
            distances[i,j] = np.dot(data[i,:],data[j,:])/(np.linalg.norm(data[i,:])*np.linalg.norm(data[j,:]))
    return distances

def preprocessing(df):
    research_paper_topic_matrix=research_paper_topic_data.drop(['Citations_All','H-Index_All','i10-Index_All','Journal Description','No. of Journals','Title And Description','Word Count'],axis=1)
    faculty_topic = research_paper_topic_matrix.set_index('Name').drop('Journals',axis=1)
    faculty_topic = faculty_topic.sum(level=0)
    return faculty_topic

def get_common_keywords(df,idx1,idx2):
    column_names=[df.columns]
    common_cols=[]
    for i in column_names:
        if df.loc[idx1,i]==1 and df.loc[idx2,i]==1:
            common_cols.append(i)
    print(common_cols)
    return common_cols

def print_cosine_similarity_reccommendation(selected_faculty):
    faculty_topic = preprocessing(research_paper_topic_data)
    faculty_list = list(faculty_topic.index)
    print(faculty_list)
    cosine_distances = cosine_similarity_matrix(faculty_topic)
    faculty_index = faculty_list.index(selected_faculty)
    similarity={}
    for j in range(len(cosine_distances)):
        if j!=faculty_index and cosine_distances[faculty_index][j]>0:
            similarity[faculty_list[j]]=cosine_distances[faculty_index][j]
    similarity=sorted(similarity.items(),key=lambda x:x[1],reverse=True)
    similarity_df=pd.DataFrame(similarity,columns=['Name','Similarity Score']).iloc[:6,:]
    # for i in list(df.columns):
    #     df[i]=df[i].apply(lambda x: True if x>0 else False)
    st.table(similarity_df)

def euclid_dist(t1, t2):
    distance = np.linalg.norm(t1 - t2)
    return distance

def k_closest(sim_df,k):
    result1 = []
    k_closest = []
    i = 0
    j = 0
    for i, row1 in sim_df.iterrows():
        result = []
        for j, row2 in sim_df.iterrows():
            if i == j:
                distance = 10000
            else:
                distance = euclid_dist(row1,row2)
            result.append(distance)
        k_closest.append(np.argsort(result)[:k])
    return k_closest

def get_k_nearest_faculty(k_closest, faculty_names):
    return [faculty_names[x] for x in k_closest]

def k_nearest_neighbour_recommendation(selected_faculty):
    faculty_topic = preprocessing(research_paper_topic_data)
    for i in list(faculty_topic.columns):
        faculty_topic[i]=faculty_topic[i].apply(lambda x: 1 if x>0 else 0)
    print(faculty_topic.head())
    faculty_list = list(faculty_topic.index)
    K_nearest = k_closest(faculty_topic,5)
    faculty_index = faculty_list.index(selected_faculty)
    for i in get_k_nearest_faculty(K_nearest[faculty_index],faculty_list):
        st.write(i)

st.title('FACULTY RECOMMENDATION')
st.markdown("<hr>",unsafe_allow_html=True)

faculty_name_list = list(faculty_data['Name'].values)
selected_faculty= st.selectbox('Select a faculty',faculty_name_list)
st.markdown("<hr>",unsafe_allow_html=True)
st.header("Cosine Similarity")
print_cosine_similarity_reccommendation(selected_faculty)
st.header("K Nearest Neighbors Recommendation")
st.write("Since you wished to see {} you might also like ....".format(selected_faculty))
k_nearest_neighbour_recommendation(selected_faculty)