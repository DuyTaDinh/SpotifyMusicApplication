import streamlit as st

def app():
    # Header
    st.markdown("<h1 style='text-align: center;'><i class='fas fa-cog'></i> Musicfy App 🎧</h1>", unsafe_allow_html=True)


    # Mission Section
    st.header(":sunglasses: Our Mission")
    st.markdown(
        "At Musicfy, we believe that music has the power to inspire, connect, and elevate the human experience. "
        "Our mission is to provide music enthusiasts with a seamless and personalized listening experience, making it easy for "
        "you to discover, share, and enjoy the music you love."
    )

    ## Intelligent Recommendations
    st.subheader("🦾 Intelligent Recommendations")
    st.markdown(
        "Our cutting-edge recommendation algorithm learns your musical preferences over time, ensuring that every song suggestion "
        "is tailored to your unique taste. Say goodbye to endless scrolling and let us be your musical guide."
    )

    ## Analysis Feature
    st.subheader("🎵 Song Analysis and Visualization")
    st.markdown(
        "Dive deeper into the world of music with our analysis feature! Musicfy allows you to explore the intricate details of "
        "your favorite songs, including key signatures, tempo, energy levels, and more. Visualize these characteristics in an "
        "engaging way, providing you with a richer understanding of the music you love."
    )

    ## Social Sharing
    st.subheader("🌐 Social Sharing")
    st.markdown(
        "Share the love for your favorite tunes with the world! Connect with friends, family, and fellow music enthusiasts by "
        "easily sharing your favorite songs and playlists. Music is better when shared, and we've made it simple for you to spread the joy."
    )

    # Footer
    st.markdown("Happy listening!")
    st.markdown('Created by: [Duy Ta](https://github.com/DuyTaDinh)')
    st.markdown('Contact via mail: [ElonMusk@gmail.com]')
    