#importing basic packages
import streamlit as st
st.set_page_config(
    page_title="GLOBE GURU",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)
#body of home page
def main():
    st.sidebar.subheader("MENU")
    st.sidebar.image("logo.jpg",use_column_width=True)
    title_template = """
    <div style="background-color:#333333; padding:5px;">
    <h1 style="color:cyan">GLOBE GURU</h1>
    </div>
    """
    st.markdown(title_template, unsafe_allow_html=True)
    st.subheader("WELCOME TO OUR SMART TRAVEL PLANNER")
    
    st.write("""
    **Globe Guru** is your ultimate companion for planning your next adventure! Whether you're a seasoned traveler or embarking on your first journey, Globe Guru has got you covered.
    
    **Explore Destinations:** Get insights about possible destinations for you to travel, handpicked by our **experts** based on your **personal interests** and **budget**.
    
    **Build Your Itinerary:** Create a personalized travel itinerary tailored to your **interests**, **budget**, and **duration of stay**. Also select from a wide list of Experts for helping you Plan your **Dream Trip**. 
    
    **Connect with Us:** Have questions or feedback? We're here to help! Reach out to us through the Contact Us section.
    
    **READ OUR ABOUT SECTION TO KNOW MORE**         
    
    Ready to start your journey? Choose an option from the menu above to get started!
    """)

if __name__=="__main__":
    main()