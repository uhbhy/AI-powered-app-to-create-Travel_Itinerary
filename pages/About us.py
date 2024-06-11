import streamlit as st
st.set_page_config(
    page_title="About us: GLOBE GURU",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)

def about_page():
    title_template = """
    <div style="background-color:#333333; padding:5px;">
    <h1 style="color:cyan">GLOBE GURU</h1>
    </div>
    """
    st.sidebar.subheader("MENU")
    st.sidebar.image("logo.jpg",use_column_width=True)
    st.markdown(title_template,unsafe_allow_html=True)
    st.subheader("About Globe Guru")
    st.write("""
    Welcome to **Globe Guru** - your passport to boundless adventures and unforgettable experiences!


    **Features:**

    - **Destination Insights:** Get insights on destinations for you to travel, handpicked by our experts based on your **personal interests** and **budget**.
    - **Build Your Itinerary:** Create **personalized** travel itineraries tailored to your **interests**, **budget**, and **duration of stay**.
    - **Connect with Us:** Have questions or feedback? Reach out to us through the **Contact Us** section.

    **Our Mission:**

    At Globe Guru, we're on a mission to redefine travel by connecting explorers with unique destinations that celebrate the rich tapestry of our world's cultural heritage. We believe that every journey is an opportunity to immerse yourself in the stories, traditions, and wonders of the places you visit.

    Through our innovative platform, we curate a handpicked selection of off-the-beaten-path destinations that capture the essence of local culture and heritage. From hidden gems tucked away in ancient cities to remote villages steeped in centuries-old traditions, we invite you to uncover the hidden treasures of our planet.

    No worries if you don't want to travel to off-the-beaten-path places and are one of those people who like to go to famous and touristy destinations. We have a wide range of experts to suggest you other kinds of places. Whether you're seeking iconic landmarks, vibrant cities, or breathtaking natural wonders, we've got you covered.

    Our team of expert travelers and cultural enthusiasts scours the globe to unearth the most authentic and immersive experiences, ensuring that each destination we recommend is a testament to the diversity and resilience of human civilization.

    Join us as we embark on a journey of discovery, where every path leads to a deeper understanding of the world and its people. With Globe Guru, the adventure of a lifetime awaits around every corner.

    """)

if __name__ == "__main__":
    about_page()
