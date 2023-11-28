import streamlit as st
from streamlit_option_menu import option_menu
import home, account, about

st.set_page_config(
        page_title="Musicfy",
        page_icon="play-circle"
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:        
            with st.sidebar:
                app = option_menu(
                    menu_title='Musicfy', 
                    menu_icon='music-note-beamed',
                    options=['Home','Account','About'],
                    icons=['house-fill','person-circle','info-circle-fill'],
                    default_index=0
                    )
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()    
        if app == 'About':
            about.app()       
    run()      

