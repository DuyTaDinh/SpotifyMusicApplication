import streamlit as st
from firebase_admin import firestore
from streamlit_option_menu import option_menu
from itertools import cycle
import songrecommendations
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID='e18fafeb60a949d2a9b7d1efccabe69a'
SPOTIPY_CLIENT_SECRET='739bbbed49864382a64a64ccd64ecdcc'


auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)
selection = "Explore"

def app():
    st.markdown("<h1 style='text-align: center;'><i class='fas fa-cog'></i>Home Page</h1>", unsafe_allow_html=True)

    if 'menuSelect' not in st.session_state:
        st.session_state.menuSelect = "Explore"

    def on_change(key):
        st.session_state.menuSelect = st.session_state[key]
        
    menuHeader = option_menu(None, ["Explore", "Search", "Trending", 'Moods & genres'],
                        icons=['compass', 'search', "graph-up-arrow", 'emoji-smile'],
                        on_change=on_change, key='menu_5', orientation="horizontal")

    if st.session_state.menuSelect == "Explore":
        if 'db' not in st.session_state:
            st.session_state.db = ''
        db=firestore.client()
        st.session_state.db=db
        # ph = ''
        # if st.session_state.username=='':
        #     ph = 'Login to be able to post!!'
        # else:
        #     ph='Post your thought'    
        # post=st.text_area(label=' :orange[+ New Post]',placeholder=ph,height=None, max_chars=500)
        # if st.button('Post',use_container_width=20):
        #     if post!='':
        #         info = db.collection('Posts').document(st.session_state.username).get()
        #         if info.exists:
        #             info = info.to_dict()
        #             if 'Content' in info.keys():
                    
        #                 pos=db.collection('Posts').document(st.session_state.username)
        #                 pos.update({u'Content': firestore.ArrayUnion([u'{}'.format(post)])})
        #                 # st.write('Post uploaded!!')
        #             else:
                        
        #                 data={"Content":[post],'Username':st.session_state.username}
        #                 db.collection('Posts').document(st.session_state.username).set(data)    
        #         else:
                        
        #             data={"Content":[post],'Username':st.session_state.username}
        #             db.collection('Posts').document(st.session_state.username).set(data)
        #         st.success('Post uploaded!!')
        st.header(':violet[Tracks Favorite] ')
        docs = db.collection('Tracks').get()      
        for doc in docs:
            d=doc.to_dict()
            try:
                st.text_area(label=':green[Posted by:] '+':orange[{}]'.format(d['Username']),value=d['Content'][-1],height=20)
            except: pass
        st.header(':violet[Posts] ')
        docs = db.collection('Posts').get()    
        for doc in docs:
            d=doc.to_dict()
            try:
                with st.chat_message("user"):
                    st.text_area(label=':green[User:] ' + ':orange[{}]'.format(d['Username']), value=d['Content'][-1],height=20)
                # with st.chat_message(d['Username']):
                #     st.write(d['Content'][-1])
            except: pass
    if st.session_state.menuSelect == "Search":
        search_keyword = st.text_input("Search songs, albums, artists, playlists")
        filteredImages = []
        listUrl = []
        caption = []
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            if st.button('Songs') and search_keyword is not None and len(str(search_keyword)) > 0:
                tracks = sp.search(q='track:'+ search_keyword,type='track', limit=10)
                tracks_list = tracks['tracks']['items']
                if len(tracks_list) > 0:
                    for track in tracks_list:
                        filteredImages.append(track['album']['images'][1]['url'])
                        listUrl.append(track['external_urls']['spotify'])
                        caption.append(track['name'] + " - " + track['artists'][0]['name'])
                else:
                    st.warning('Not found')
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
                

    if st.session_state.menuSelect == 'Trending':
        Trending()
    if st.session_state.menuSelect == 'Moods & genres':
        Moods()

       
def Explore():
    st.write('explore')

def Trending():
    st.write('Trending')

def Moods():
    st.write('Moods & genres')