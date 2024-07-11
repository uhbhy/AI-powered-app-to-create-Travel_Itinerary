import streamlit as st
st.set_page_config(
    page_title="Contact Us: GLOBE GURU",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

import base64
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

def contact_us_page():
    title_template = """
    <div style="background-color:#2f3e46; padding:5px;">
    <h1 style="color:#cad2c5">GLOBE GURU</h1>
    </div>
    """
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpg",use_column_width=True)
    st.markdown(title_template,unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.header("Have questions, feedback, or need assistance? We're here to help! Reach out to us through any of the following channels:")
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("""
    <div style="font-size: 25px;">
    <b>Email:</b> <a href="mailto:abhirupbasu30@gmail.com">abhirupbasu30@gmail.com</a>
    <b>Phone:</b> +91 8235026220
    </div>
    """,unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("""
    <div style="font-size: 25px;">
    Our dedicated team is committed to providing prompt and helpful assistance to all our users. We pride ourselves on our speedy responses and our ability to resolve issues as soon as possible.
    <br>
    Your feedback is invaluable to us. If you encounter any issues or have suggestions for improving the app, please don't hesitate to report them to us. By working together, we can make Globe Guru even better and ensure a seamless user experience for everyone.
    <br>
    Thank you for choosing Globe Guru! We look forward to hearing from you and assisting you on your travel journey.
    </div>
    """,unsafe_allow_html=True)

if __name__ == "__main__":
    contact_us_page()
