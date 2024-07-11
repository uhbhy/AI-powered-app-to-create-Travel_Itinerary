import streamlit as st
import base64
st.set_page_config(
    page_title="About us: GLOBE GURU",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to encode image to base64
@st.cache_data
def get_base64_image(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your image
img_file = "styling.jpg"
img_base64 = get_base64_image(img_file)

# Custom CSS for watermark effect
page_bg_img = f'''
<style>
body {{
background-image: url("data:image/png;base64,{img_base64}");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
opacity: 0.9;  
}}
</style>
'''

# Inject CSS into Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

def about_page():
    title_template = """
    <div style="background-color:#2f3e46; padding:5px;">
    <h1 style="color:#cad2c5">GLOBE GURU</h1>
    </div>
    <hr>
    """
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpg",use_column_width=True)
    st.markdown(title_template,unsafe_allow_html=True)
    st.header("Welcome to **Globe Guru** - Your Passport to Boundless Adventures and Unforgettable Experiences!")
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("""
    <div style="font-size: 25px;">
    <b>Features</b>:
    <br>
    <b>Destination Insights</b>: Discover curated destinations based on your personal interests and budget, handpicked by our experts.
    <br>
    <b>Build Your Itinerary</b>: Create personalized travel itineraries tailored to your interests, budget, and duration of stay.
    <br>
    <b>Weather Forecast</b>: Get accurate weather forecasts for the duration of your trip, ensuring you're prepared for any climate conditions.
    <br>
    <b>Packing Tips</b>: Receive expert tips on what to pack based on the weather and local customs, ensuring a comfortable and hassle-free journey.
    <br>
    <b>Connect with Us</b>: Have questions or feedback? Reach out to us through the Contact Us section.
    </div>
    """,unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("""
    <div style="font-size: 25px;">
    <b>Our Mission</b>:
    <br>
    At <b>Globe Guru</b>, we're on a mission to redefine travel by connecting explorers with unique destinations that celebrate the rich tapestry of our world's cultural heritage. We believe that every journey is an opportunity to immerse yourself in the stories, traditions, and wonders of the places you visit.
    <br>
    Through our innovative platform, we curate a handpicked selection of off-the-beaten-path destinations that capture the essence of local culture and heritage. From hidden gems tucked away in ancient cities to remote villages steeped in centuries-old traditions, we invite you to uncover the hidden treasures of our planet.
    </div>
    """,unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("""
    <div style="font-size: 25px;">
    <b>Travel Planning Made Easy</b>:
    <br>
    <b>Weather Forecasts</b>: Whether you're exploring a tropical paradise or a snowy mountain retreat, our detailed weather forecasts ensure you're prepared for your journey ahead.
    <br>
    <b>Packing Essentials</b>: Pack smart with our essential packing list tailored to your destination and season. From clothing recommendations to travel accessories, we've got you covered.
    <br>
    <b>Travel Tips</b>: Navigate local customs and etiquette with ease, enhancing your travel experience with insider tips from our seasoned travelers.
    <br><br>
    No worries if you prefer famous tourist destinations; we cater to all preferences with insights into iconic landmarks, vibrant cities, and breathtaking natural wonders. Our diverse team of experts ensures you receive personalized recommendations that align with your travel style.
    </div>
    """,unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("""
    <div style="font-size: 25px;">
    Join us as we embark on a journey of discovery, where every path leads to a deeper understanding of the world and its people. With Globe Guru, the adventure of a lifetime awaits around every corner.
    </div>
    """,unsafe_allow_html=True)

if __name__ == "__main__":
    about_page()
