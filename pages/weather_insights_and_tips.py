import streamlit as st
import requests
from datetime import datetime, timedelta
from openai import OpenAI

st.set_page_config(
    page_title="Destination_Insights: GLOBE GURU",
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
opacity: 0.94;  
}}
</style>
'''
# Inject CSS into Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Custom CSS to control the width of the widgets
st.markdown("""
    <style>
    .stSlider [data-baseweb=slider]{
        width: 525px;
    }
    .stTextInput {
        width: 525px;
    }
    .stMultiSelect [data-baseweb="select"] {
        width: 525px;
    }
    .stSelectbox [data-baseweb="select"] {
        width: 525px;
    }    
    </style>
    """, unsafe_allow_html=True)


#Initializing a list to contain all of the image_urls generated by DALL-E
image_urls = []

#Function to get packing essentials
def packing_essentials(city,start_month_name, end_month_name, api_key):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    if(start_month_name==end_month_name):
        # Define the system message template
        system_message = ("You are a local resident of [city] who helps travelers with packing essential items for their trip"
                          "in your city in the month of [start_month_name]. Your goal is to advise them on essential items"
                          "they should pack depending on the weather during the duration of their trip"
                          "that might come in handy during their travels.")
                            
        # Create the user message for few-shot prompting
        user_message_tuning=("city:Kolkata \n start_month_name:July")
        
        #Create assistant response for user_message_tuning
        assistant_message_tuning=("""
                                    **ESSENTIAL PACKING LIST:**

                                    **Clothing:**

                                    Lightweight, breathable, and quick-drying clothes.
                                    Waterproof jacket or raincoat.
                                    Extra pairs of socks and underwear.

                                    **Footwear:**

                                    Waterproof shoes or sandals.
                                    Comfortable walking shoes that dry quickly.

                                    **Weather-Specific Gear:**

                                    Umbrella or a sturdy rain poncho.
                                    Waterproof bags or covers for your belongings.
                                """)
    
        #Create the user message for generating itinerary
        user_message=(f"city:{city} \n start_month_name:{start_month_name}")
    else:
        # Define the system message template
        system_message = ("You are a local resident of [city] who helps travelers with packing essential items for their trip"
                          "in your city between the months of [start_month_name] and [end_month_name].Your goal is to advise them on essential items"
                          "they should pack depending on the weather during the duration of their trip"
                          "that might come in handy during their travels.")
                            
        # Create the user message for few-shot prompting
        user_message_tuning=("city:Kolkata \n start_month_name:December \n end_month_name:January")
        
        #Create assistant response for user_message_tuning
        assistant_message_tuning=("""
                                    **ESSENTIAL PACKING LIST:**

                                    **Clothing:**

                                    Light sweaters or jackets for the cooler evenings and mornings.
                                    Long-sleeved shirts and T-shirts.
                                    Comfortable pants and jeans.
                                    Light and breathable fabrics for daytime.
                                  
                                    **Footwear:**

                                    Comfortable walking shoes or sneakers.
                                    Sandals or flip-flops for casual outings.
                                    Weather-Specific Gear:

                                    Umbrella or a light raincoat (just in case of unexpected showers).
                                """)
    
        #Create the user message for generating itinerary
        user_message=(f"city:{city} \n start_month_name:{start_month_name} \n end_month_name: {end_month_name}")

    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.6,
        n=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response content
    result=response.choices[0].message.content
    return result
#Function to get packing essentials
def packing_non_essentials(city,start_month_name, end_month_name, api_key):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    if(start_month_name==end_month_name):
        # Define the system message template
        system_message = (  "You are a local resident of [city] who helps travelers with packing non-essential but useful items for their trip"
                            "in your city for the month of [start_month_name]. Your goal is to advise them on items that might come in handy"
                            "during their travels, considering the weather and local conditions.")
                            
        # Create the user message for few-shot prompting
        user_message_tuning=("city:Kolkata \n start_month_name:July")
        
        #Create assistant response for user_message_tuning
        assistant_message_tuning=("""
                                    **NON-ESSENTIAL BUT USEFUL ITEMS:**

                                    **Travel Gadgets:**

                                    Power bank for your electronic devices.
                                    Waterproof phone case or pouch.

                                    **Comfort Items:**

                                    Insect repellent to protect against mosquitoes.
                                    Light scarf or shawl for sudden temperature changes indoors.

                                    **Activity Gear:**

                                    A good book or e-reader for rainy days.
                                    Camera or smartphone for capturing the unique monsoon scenes.
                                """)
    
        #Create the user message for generating itinerary
        user_message=(f"city:{city} \n start_month_name:{start_month_name}")
    else:
        # Define the system message template
        system_message = ( "You are a local resident of [city] who helps travelers with packing non-essential but useful items for their trip"
                            "in your city for the months of [start_month_name] and [end_month_name]. Your goal is to advise"
                            "them on items that might come in handy during their travels,"
                            "considering the weather and local conditions.")
                            
        # Create the user message for few-shot prompting
        user_message_tuning=("city:Kolkata \n start_month_name:December \n end_month_name:January")
        
        #Create assistant response for user_message_tuning
        assistant_message_tuning=("""
                                     **NON-ESSENTIAL BUT USEFUL ITEMS:**

                                    **Travel Gadgets:**

                                    Power bank for your electronic devices.
                                    Waterproof phone case or pouch.

                                    **Comfort Items:**

                                    Insect repellent to protect against mosquitoes.
                                    Light scarf or shawl for sudden temperature changes indoors.

                                    **Activity Gear:**

                                    A good book or e-reader for rainy days.
                                    Camera or smartphone for capturing the unique monsoon scenes.
                                """)
    
        #Create the user message for generating itinerary
        user_message=(f"city:{city} \n start_month_name:{start_month_name} \n end_month_name: {end_month_name}")

    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.6,
        n=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response content
    result=response.choices[0].message.content
    return result

# Function to get forecast for date range
def get_weather_forecast(city, start_month_name, end_month_name, api_key):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    if(start_month_name==end_month_name):
        # Define the system message template
        system_message = ("You are a weather expert who provides travelers with accurate and probable weather forecasts"
                          "for [city] in the month of [start_month_name]. Your goal is to give users a general idea of the"
                          "expected weather for the duration of their trip.")
                            
        # Create the user message for few-shot prompting
        user_message_tuning=("city:Kolkata \n start_month_name:July")
        
        #Create assistant response for user_message_tuning
        assistant_message_tuning=("""
                                    **WEATHER FORECAST FOR KOLKATA (July):**

                                    **Temperature:**

                                    Average Highs: 30°C to 33°C (86°F to 91°F)
                                    Average Lows: 25°C to 27°C (77°F to 81°F)

                                    **Precipitation:**

                                    High chances of rainfall due to the monsoon season. Expect frequent heavy showers and thunderstorms.

                                    **Humidity:**

                                    Very high humidity, making the weather feel hotter and more oppressive.

                                    **Notable Weather Patterns:**

                                    Monsoon season brings heavy and frequent rain. Overcast skies and occasional flooding in low-lying areas.
                                """)
    
        #Create the user message for generating itinerary
        user_message=(f"city:{city} \n start_month_name:{start_month_name}")
    else:
        # Define the system message template
        system_message = ("You are a weather expert who provides travelers with accurate and probable weather forecasts"
                          "for [city] in the month of [start_month_name]. Your goal is to give users a general idea of the"
                          "expected weather for the duration of their trip.")
                            
        # Create the user message for few-shot prompting
        user_message_tuning=("city:Kolkata \n start_month_name:December \n end_month_name:January")
        
        #Create assistant response for user_message_tuning
        assistant_message_tuning=("""
                                    **WEATHER FORECAST FOR KOLKATA (December to January):**

                                    **Temperature:**

                                    Average Highs: 23°C to 26°C (73°F to 79°F)
                                    Average Lows: 12°C to 15°C (54°F to 59°F)
                                  
                                    **Precipitation:**

                                    Generally dry with low chances of rainfall. Occasional light showers are possible.
                                    
                                    **Humidity:**

                                    Moderate to high humidity, but more comfortable compared to the summer months.
                                    
                                    **Notable Weather Patterns:**

                                    Pleasant and cool weather, especially in the evenings and early mornings. Days are usually sunny with clear skies.
                                """)
    
        #Create the user message for generating itinerary
        user_message=(f"city:{city} \n start_month_name:{start_month_name} \n end_month_name: {end_month_name}")

    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.6,
        n=1,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response content
    result=response.choices[0].message.content

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
    {
    "role": "system",
    "content":"You are a helpful assistant that creates DALL-E prompts based on"
              "a weather forecast.The prompts should be short but creative."
              "Create 3 prompts for 3 images, The DALL-E prompt should be separated by \"|\"."
    },
    {
    "role": "user",
    "content": result
    }
    ],
    temperature=0.9,
    max_tokens=1024,
    top_p=1,
    n=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    dalle_prompts_list = response.choices[0].message.content.split('|')
    for prompt in dalle_prompts_list:
        response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
        )
        image_urls.append(response.data[0].url)
    return result

# Main function
def main():
    # OpenAI API key
    api_key = ""
    title_template = """
    <div style="background-color:#2f3e46; padding:5px;">
    <h1 style="color:#cad2c5">GLOBE GURU</h1>
    </div>
    <hr>
    """
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpg", use_column_width=True)
    st.markdown(title_template, unsafe_allow_html=True)
    st.header("Get **Weather Forecast** for your trip in just a few clicks...")
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("**Disclaimer**: For privacy purposes we do not store any user data")
    st.write("""
             
             """)
    col1, col2, col3 = st.columns([1,1,1])
    get=False
    with col1:
        # Getting inputs from user
        city = st.text_input("Enter the city:")
        start_date = st.date_input("Start date:")
        end_date = st.date_input("End date:")
        # Convert the month digit to month name
        start_month_name = start_date.strftime("%B")
        end_month_name = end_date.strftime("%B")
        if st.button("Get Weather Forecast"):
            get=True

    if get:
        st.markdown("<hr>",unsafe_allow_html=True)
        if city and start_date and end_date:
            if start_date <= end_date:
                with st.spinner("Fetching weather details..."):
                    try:
                        forecast_data = get_weather_forecast(city, start_month_name, end_month_name, api_key)
                        packing_essentials_data=packing_essentials(city, start_month_name, end_month_name, api_key)
                        packing_non_essentials_data=packing_non_essentials(city, start_month_name, end_month_name, api_key)

                        col1,col2,col3=st.columns(3)
                        
                        if forecast_data and packing_essentials_data and packing_non_essentials_data:
                                with col1:
                                    st.write(forecast_data)
                                with col2:
                                    st.write(packing_essentials_data)
                                with col3:
                                    st.write(packing_non_essentials_data)

                                st.markdown("<hr>",unsafe_allow_html=True)
                                col4,col5,col6=st.columns(3)
                                with col4:
                                    st.image(image_urls[0], use_column_width=True)
                                with col5:
                                    st.image(image_urls[1], use_column_width=True)
                                with col6:
                                    st.image(image_urls[2], use_column_width=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("Start date must be before or the same as end date.")
        else:
            st.error("Please fill all fields.")

if __name__ == "__main__":
    main()
