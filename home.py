import streamlit as st
from firebase_admin import firestore
from streamlit_option_menu import option_menu
from itertools import cycle
from datetime import datetime
from models import Post
import pandas as pd
import polarplot
import songrecommendations
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID= 'YOUR SPOTIPY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET='YOUR SPOTIPY_CLIENT_SECRET'


auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_post():
    return [
        Post.date.value,
        Post.user_name.value,
        Post.track_name.value,
        Post.message.value,
    ]

@st.cache_resource
def get_db():
    db = firestore.client()
    return db

@st.cache_data(ttl=30)
def get_all_posts():
    db = get_db()
    all_posts = db.collection("Posts").order_by(Post.date.value).stream()
    df = pd.DataFrame([m.to_dict() for m in all_posts])
    if df.empty:
       return df
    return df[get_post()]

def post_message(db, user_name, track_name, input_message):
    payload = {
        Post.user_name.value: user_name,
        Post.track_name.value: track_name,
        Post.message.value: input_message,
        Post.date.value: datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    }
    doc_ref = db.collection("Posts").document()
    doc_ref.set(payload)
    return


def app():
    st.markdown("<h1 style='text-align: center;'><i class='fas fa-cog'></i>Home Page</h1>", unsafe_allow_html=True)
    if 'username' in st.session_state:
        st.text('Hello '+st.session_state.username)

    if 'menuSelect' not in st.session_state:
        st.session_state.menuSelect = "Explore"

    def on_change(key):
        st.session_state.menuSelect = st.session_state[key]
        
    menuHeader = option_menu(None, ["Explore", "Search", "Recommend", 'Analysis'],
                        icons=['compass', 'search', "cpu", 'emoji-smile'],
                        on_change=on_change, key='menu_5', orientation="horizontal")

    if st.session_state.menuSelect == "Explore":
        if 'db' not in st.session_state:
            st.session_state.db = ''
        db=firestore.client()
        st.session_state.db=db

        if 'username' not in st.session_state or st.session_state.username=='':
            st.write('Login to be able to post!')
        else: 
            if 'btn_post' not in st.session_state:
                st.session_state.btn_post = False
            def click_button():
                st.session_state.btn_post = not st.session_state.btn_post
            st.button('Share Your Favorite Songs!', on_click=click_button)
            if st.session_state.btn_post:
                with st.form(key="form", clear_on_submit=True):
                    tract_name = st.text_input("Track Name")
                    input_message = st.text_area(label="Your message",height=None, max_chars=500)
                    if st.form_submit_button("Submit") and st.session_state.username:
                        post_message(db, st.session_state.username , tract_name, input_message)
                        st.success("Your message was posted!")
                        st.balloons()

        st.header('Posts')
        all_posts = get_all_posts()
        st.dataframe(all_posts, use_container_width=True, hide_index=True)

    if st.session_state.menuSelect == "Search":
        search_keyword = st.text_input("Search songs, albums, artists, playlists")
        filteredImages = []
        listUrl = []
        caption = []
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            if st.button('Songs'):
                if search_keyword is not None and len(str(search_keyword)) > 0:
                    tracks = sp.search(q='track:'+ search_keyword,type='track', limit=10)
                    tracks_list = tracks['tracks']['items']
                    if len(tracks_list) > 0:
                        for track in tracks_list:
                            filteredImages.append(track['album']['images'][1]['url'])
                            listUrl.append(track['external_urls']['spotify'])
                            caption.append(track['name'] + " - " + track['artists'][0]['name'])
                    else:
                        st.warning('Not found')
                else:
                    st.warning('Please enter keyword!')
        with col2:
            if st.button('Albums') and search_keyword is not None and len(str(search_keyword)) > 0:
                albums = sp.search(q='album:'+ search_keyword,type='album', limit=10)
                albums_list = albums['albums']['items']
                if len(albums_list) > 0:
                    for album in albums_list:
                        filteredImages.append(album['images'][1]['url'])
                        listUrl.append(album['external_urls']['spotify'])
                        caption.append(album['name'] + " - " + album['artists'][0]['name'])
                else:
                    st.warning('Not found')     
        with col3:
            if st.button('Artists') and search_keyword is not None and len(str(search_keyword)) > 0:
                artists = sp.search(q='artist:'+ search_keyword,type='artist', limit=20)
                artists_list = artists['artists']['items']
                if len(artists_list) > 0:
                    for artist in artists_list:
                        filteredImages.append(artist['images'][1]['url'])
                        listUrl.append(artist['external_urls']['spotify'])
                        caption.append(artist['name'])
                else:
                    st.warning('Not found')
        with col4:
            if st.button('Playlists'):
                st.warning('Service not support')

        cols = cycle(st.columns(2))
        for idx, filteredImage in enumerate(filteredImages):
            sourceImg = filteredImage.strip('"')
            url = listUrl[idx]
            with next(cols):
                st.code(caption[idx], language='python')
                st.markdown(f"[![Foo]({sourceImg})]({url})")
                

    if st.session_state.menuSelect == 'Recommend':
        search_keyword = st.text_input("Enter keywords")
        track_id = None
        filteredImages = []
        listUrl = []
        caption = []
        if st.button('Search'):
            if search_keyword is not None and len(str(search_keyword)) > 0:
                tracks = sp.search(q='track:'+ search_keyword,type='track', limit=10)
                tracks_list = tracks['tracks']['items']
                if len(tracks_list) > 0:
                    track_id = tracks_list[0]['id']
                    filteredImages.append(tracks_list[0]['album']['images'][1]['url'])
                    listUrl.append(tracks_list[0]['external_urls']['spotify'])
                    caption.append(tracks_list[0]['name']+ " - " + tracks_list[0]['artists'][0]['name'])
                else:
                    st.warning('Not found')
            else:
                st.warning('Please enter keyword!')
        if track_id is not None:
            token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
            similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
            recommendation_list = similar_songs_json['tracks']
            recommendation_list_df = pd.DataFrame(recommendation_list)
            recommendation_df = recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
            st.dataframe(recommendation_df)
            # songrecommendations.song_recommendation_vis(recommendation_df)
            for track_recommendation in recommendation_list:
                # print(track_recommendation)
                str_temp = track_recommendation['name'] + " - " + track_recommendation['artists'][0]['name']
                filteredImages.append(track_recommendation['album']['images'][1]['url'])
                listUrl.append(track_recommendation['external_urls']['spotify'])
                caption.append(str_temp)
            cols = cycle(st.columns(2))
            for idx, filteredImage in enumerate(filteredImages):
                sourceImg = filteredImage.strip('"')
                if idx >= len(listUrl):
                    break
                url = listUrl[idx]
                with next(cols):
                    st.code(caption[idx], language='python')
                    st.markdown(f"[![Foo]({sourceImg})]({url})")

    if st.session_state.menuSelect == 'Analysis':
        tracks = []
        search_results = []
        track_id = None
        selected_track_choice = None 
        search_keyword = st.text_input("Enter song/track to analysis:")
        if search_keyword is not None and len(str(search_keyword)) > 0:
            tracks = sp.search(q='track:'+ search_keyword,type='track', limit=20)
            tracks_list = tracks['tracks']['items']
            if len(tracks_list) > 0:
                for track in tracks_list:
                    search_results.append(track['name'] + " - " + track['artists'][0]['name'])
        selected_track = st.selectbox("Select your song/track: ", search_results)
        if selected_track is not None and len(tracks) > 0:
            tracks_list = tracks['tracks']['items']
            if len(tracks_list) > 0:
                for track in tracks_list:
                    str_temp = track['name'] + " - " + track['artists'][0]['name']
                    if str_temp == selected_track:
                        track_id = track['id']           
            if track_id is not None:
                track_features  = sp.audio_features(track_id) 
                df = pd.DataFrame(track_features, index=[0])
                df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                st.dataframe(df_features, hide_index=True)
                polarplot.feature_plot(df_features)
            else:
                st.write("Please select a track from the list")  

