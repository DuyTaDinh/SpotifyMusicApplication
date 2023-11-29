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

    def run(self):
        with st.sidebar:        
            app = option_menu(
                menu_title='Musicfy', 
                menu_icon='music-note-beamed',
                options=['Home','Account','About'],
                icons=['house-fill','person-circle','info-circle-fill'],
                default_index=0
            )

        for app_info in self.apps:
            if app_info["title"] == app:
                app_info["function"]()

if __name__ == "__main__":
    multi_app = MultiApp()

    # Add your apps here
    multi_app.add_app("Home", home.app)
    multi_app.add_app("Account", account.app)
    multi_app.add_app("About", about.app)

    # Run the selected app
    multi_app.run()
