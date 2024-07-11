import streamlit as st
import base64

# Set the page configuration
st.set_page_config(
    page_title="Home: GLOBE GURU",
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
opacity: 0.94;  
}}
</style>
'''

# Inject CSS into Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)


# Body of the home page
def main():
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpg", use_column_width=True)
    
    title_template = """
    <div style="background-color:#2f3e46; padding:5px;">
    <h1 style="color:#cad2c5">GLOBE GURU</h1>
    </div>
    <hr>
    """
    st.markdown(title_template, unsafe_allow_html=True)
    
    st.write("""
             <h1>Welcome to Globe Guru- Your Ultimate Companion for Planning Your Next Adventure!</h1>
             """,unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    feature_text = """
        <div style="font-size: 25px;">
        <b>Explore Destinations</b>: Discover insights about possible destinations tailored to your personal interests and budget, handpicked by our expert travelers.
        <br><br>
        <b>Build Your Itinerary</b>: Create a personalized travel itinerary that suits your interests, budget, and duration of stay. Consult with our experts to plan your dream trip.
        <br><br>
        <b>Weather Forecast</b>: Stay informed with accurate weather forecasts for the duration of your trip. Be prepared for any climate conditions to make the most of your journey.
        <br><br>
        <b>Packing Tips</b>: Receive expert tips on what to pack based on your destination and season. From essential items to local customs, we ensure you're well-prepared for your adventure.
        <br><br>
        <b>Essential Travel Considerations</b>: Learn about important factors such as local etiquette, safety tips, and cultural insights to enhance your travel experience.
        <br><br>
        <b>Connect with Us</b>: Have questions or feedback? Reach out to us through the Contact Us section.
        <br><br>
        <b>READ OUR ABOUT SECTION TO KNOW MORE</b>
        <br><br>
        Ready to start your journey? Choose an option from the menu to get started!
        </div>
        """

    st.markdown(feature_text, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<h1>Travellers have planned amazing trips to</h1>', unsafe_allow_html=True)
    
    # Create a 3x2 grid for the collage
    cols = st.columns(3)
    image_paths = [
        "4.jpg",
        "2.jpg",
        "3.jpg",
        "7.jpg",
        "5.jpg",
        "6.jpg"
    ]
    
    # Display the images in a collage format
    for i, img_path in enumerate(image_paths):
        with cols[i % 3]:
            st.image(img_path, use_column_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h1>OUR STORIES</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        template1 = """
            <hr>
            <h3>Kara and Nate's Romantic Paris Getaway</h3>
        """
        st.markdown(template1, unsafe_allow_html=True)
        with st.expander(""):
            st.write("""
                    <div style="font-size:20px;">
                    <strong>A Parisian Dream</strong>
                    <br>
                    Nate and I recently took an unforgettable trip to Paris, a city that had always been on our bucket list. As soon as we landed, the excitement was palpable; we were finally in the City of Lights!
                    <br>
                    We started our adventure with a leisurely stroll along the Seine, catching the sunset's golden glow over the water and historic buildings. Hand in hand, we made our way to the Eiffel Tower, reaching the top just in time to see the city sparkle. It was a moment I’ll cherish forever.
                    <br>
                    The next morning, we enjoyed croissants and café au lait at a charming café in Montmartre. We wandered through narrow, cobblestone streets, discovering hidden art galleries and quirky boutiques. We found a small park and sat for a while, soaking in the city's vibrant yet peaceful ambiance.
                    <br>
                    One highlight was our visit to the Louvre. We spent hours admiring masterpieces like the Mona Lisa and the Venus de Milo. We played a game, picking our favorite piece in each room and explaining why it spoke to us, making the experience even more special.
                    <br>
                    In the evenings, we explored Paris's culinary delights. We dined at a cozy bistro, trying escargot for the first time (Nate was braver than I was!). Another evening, we splurged on a dinner cruise along the Seine, enjoying the breathtaking view of Notre-Dame illuminated against the night sky.
                    <br>
                    A memorable day was our bike ride through the gardens of Versailles. We packed a picnic and found a quiet spot by the Grand Canal. As we lounged on the grass, sipping wine and nibbling on cheese, I felt a deep sense of contentment and happiness.
                    <br>
                    Our trip to Paris was everything I had hoped for and more. It was a perfect blend of romance, adventure, and discovery. We left with our hearts full, already planning our next adventure together. Paris, with its timeless charm and endless wonders, will always hold a special place in our hearts.
                    </div>
                    """, unsafe_allow_html=True)
    with col2:
        template2 = """
            <hr>
            <h3>Emily's Solo backpacking Trip</h3>
        """
        st.markdown(template2, unsafe_allow_html=True)
        with st.expander(""):
            st.write("""
                    <div style="font-size:20px;">
                    <strong>Finding Myself</strong>
                    <br>
                    I recently embarked on an unforgettable solo backpacking trip across Europe, a journey I had always dreamed of but never thought I’d have the courage to undertake. The idea of traveling alone was daunting, and I didn't know where to start with planning. That's when Globe Guru came to my rescue.
                    <br>
                    Globe Guru helped me map out my entire trip, providing detailed itineraries, packing tips, and essential travel considerations. With its guidance, I felt more confident and prepared to step into the unknown.
                    <br>
                    My journey began in Paris, where I marveled at the Eiffel Tower and wandered through the art-filled halls of the Louvre. Despite my initial fears, I quickly adapted to the rhythm of solo travel, finding joy in my own company.
                    <br>
                    Next, I traveled to Amsterdam, where I biked along the canals and visited the Anne Frank House. The freedom of making spontaneous decisions and discovering hidden gems was exhilarating. In Berlin, I explored the remnants of history at the Berlin Wall and experienced the city's vibrant nightlife.
                    <br>
                    One of the most spiritual parts of my journey was in the Swiss Alps. Hiking through the breathtaking landscapes, I felt a deep connection with nature and a sense of peace that I had never known before. It was in these quiet moments that I began to truly find myself.
                    <br>
                    In Italy, I wandered the ancient streets of Rome, stood in awe before the Colosseum, and savored the rich flavors of authentic Italian cuisine. Each city brought new experiences and self-discoveries, making me feel more alive and aware than ever.
                    <br>
                    Barcelona was another highlight, with its unique architecture and lively atmosphere. I spent my days exploring Gaudí’s masterpieces and my nights enjoying tapas and flamenco shows. The vibrant culture of the city was contagious, and I felt myself letting go of old fears and embracing the adventure.
                    <br>
                    Throughout my trip, Globe Guru was my trusty companion, guiding me and offering invaluable advice. Thanks to its help, what started as a scary and overwhelming endeavor turned into the most refreshing and transformative journey of my life.
                    <br>
                    I returned home feeling like a completely new person. The fears that once held me back were replaced with a newfound confidence and a deep sense of accomplishment. My solo backpacking trip across Europe was not just a physical journey but a spiritual one, helping me discover who I truly am and who I aspire to be.
                    <br>
                    This adventure taught me that the world is full of wonders waiting to be explored, and sometimes, the best way to find yourself is to get lost in its beauty.
                    </div>
                    """,unsafe_allow_html=True)
        
    with col3:
        template3 = """
            <hr>
            <h3>Carlos' Boys Trip</h3>
        """
        st.markdown(template3, unsafe_allow_html=True)
        with st.expander(""):
            st.write("""
                    <div style="font-size:20px;">
                    <strong>The Trip Of a Lifetime</strong>
                    <br>
                    My friends and I recently took an unforgettable trip to Bali, a destination that had always been on our bucket list. As soon as we landed, the excitement was palpable; we were finally on the Island of the Gods!
                    <br>
                    We started our adventure with a relaxing day at Seminyak Beach, catching the sunset's golden glow over the ocean. With toes in the sand and the sound of waves crashing, we toasted to our friendship and the adventures ahead.
                    <br>
                    The next morning, we enjoyed breakfast at a local café, indulging in fresh tropical fruits and Balinese coffee. We spent the day exploring the bustling streets of Ubud, discovering hidden temples and vibrant markets. We found a serene rice terrace and took in the breathtaking views while chatting and laughing.
                    <br>
                    One highlight was our visit to the Sacred Monkey Forest Sanctuary. We spent hours wandering among the playful monkeys and lush greenery. We even had a game of who could take the best selfie with a monkey—needless to say, the results were hilarious!
                    <br>
                    In the evenings, we explored Bali's culinary delights. We dined at a beachfront restaurant, trying traditional dishes like Nasi Goreng and Babi Guling. Another evening, we attended a sunset seafood barbecue at Jimbaran Bay, enjoying the stunning view and delicious food.
                    <br>
                    A memorable day was our hike up Mount Batur to catch the sunrise. We started early, and the trek was challenging but worth it. As we reached the summit and saw the sun rise over the horizon, a deep sense of accomplishment and camaraderie washed over us.
                    <br>
                    Our trip to Bali was everything I had hoped for and more. It was a perfect blend of adventure, relaxation, and discovery. We left with our hearts full, already planning our next adventure together. Bali, with its vibrant culture and natural beauty, will always hold a special place in our hearts.
                    </div>
                    """,unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    col1,col2=st.columns([0.75,1.25])
    with col1:
        st.write("""
                 <div>
                 <h1>Plan your trip<br>end to end with Expert<br>Travelers</h1>
                 """,unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.write("""
                 <div>
                 <h3>Experienced travelers will help you personalise the entire trip...</h3>
                 """,unsafe_allow_html=True)
    with col2:
         # Create a 3x2 grid for the collage
        cols = st.columns(2)
        image_paths = [
            "expert1.jpg",
            "expert2.jpg",
            "expert3.jpg",
            "expert_4.jpg"
        ]
        
        # Display the images in a collage format
        for i, img_path in enumerate(image_paths):
            with cols[i % 2]:
                st.image(img_path, use_column_width=True)

if __name__ == "__main__":
    main()
