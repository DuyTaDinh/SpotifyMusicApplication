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

    ## Trending Music
    st.subheader(":chart_with_upwards_trend: Trending Music")
    st.markdown(
        "Stay in the loop with the latest musical trends! Explore our 'Top Trending' section to discover the hottest tracks "
        "making waves around the globe. Whether it's chart-toppers or hidden gems, we've got your finger on the pulse of the "
        "music scene."
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
    