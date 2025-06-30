import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie-Recommender-System')

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

import gdown
import os

if not os.path.exists('similarity.pkl'):
    url = 'https://drive.google.com/uc?id=1djK1zKPd9QlJ89a6AFmV7ZZQ4VbbnrDW'
    gdown.download(url, 'similarity.pkl', quiet=False)
similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/'
                 '{}?api_key=YOUR_API_KEY'
                 '&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[0:20]

    recommended_movies=[]
    posters=[]
    for j in movies_list:
        recommended_movies.append(movies.iloc[j[0]].title)
        #fetch posters from api
        posters.append(fetch_poster(movies.iloc[j[0]].movie_id))
    return recommended_movies,posters

selected_movie_name=st.selectbox("Search For Movies",movies['title'].values)

if st.button('Recommend'):
    recommendations,posters=recommend(selected_movie_name)

    for i in range(0,3):
        col,col2,col3=st.columns(3)
        with col:
            st.text(recommendations[3*i])
            st.image(posters[3*i])
        with col2:
            st.text(recommendations[3*i+1])
            st.image(posters[3*i+1])
        with col3:
            st.text(recommendations[3*i+2])
            st.image(posters[3*i+2])

st.subheader("itsroh")



