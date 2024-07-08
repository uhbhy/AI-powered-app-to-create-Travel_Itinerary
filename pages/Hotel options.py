import requests
import certifi
import streamlit as st
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
img_file = r"D:\travel_app\styling.jpg"
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

# Custom CSS to control the width of the widgets
st.markdown("""
    <style>
    .stSlider [data-baseweb=slider]{
        width: 500px;
    }
    .stTextInput label {
        font-size: 20px; /* Adjust the font size as needed */
    }
    .stTextInput {
        width: 1000px,
    }
    .stMultiSelect [data-baseweb="select"] {
        width: 500px;
    }
    .stSelectbox [data-baseweb="select"] {
        width: 500px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to get the access token from Amadeus API
def get_access_token(api_key, api_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error(f"Error fetching access token: {response.text}")
        return None

# Function to fetch hotels by city
def fetch_hotels_by_city(access_token, city_code, radius=5, radius_unit='KM', amenities=None, ratings=None):
  url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
  params = {
    "cityCode": city_code,
    "radius": radius,
    "radiusUnit": radius_unit,
    "ratings": ",".join(ratings) if ratings else None,
    "amenities": ",".join(amenities) if amenities else None
  }
  headers = {
    "Authorization": f"Bearer {access_token}"
  }
  response = requests.get(url, params=params, headers=headers, verify=False)
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Error fetching hotel offers: {response.status_code} - {response.text}")
    return None

# Function to display hotel data with price
def display_hotel_data(hotel_data):
  if 'data' in hotel_data:
    hotels = hotel_data['data'][:10]  # Limit to the first 10 hotels
    if not hotels:
      st.write("No hotels found.")
      return

    for hotel in hotels:
      name = hotel['name']
      if "TEST PROPERTY" in name:  # Filter out test properties
        continue

      distance = hotel['distance']['value']
      distance_unit = hotel['distance']['unit']
      country_code = hotel['address']['countryCode']
      latitude = hotel['geoCode']['latitude']
      longitude = hotel['geoCode']['longitude']

      # Extract and format price information (assuming price is present in a field named 'total_price')
      if 'offers' in hotel and hotel['offers']:
        offer = hotel['offers'][0]  # Assuming the first offer contains the price
        currency = offer['price']['currency']
        amount = offer['price']['amount']
        price_text = f"{amount} {currency}"
      else:
        price_text = "Price unavailable"

      st.write(f"**{name}** ({price_text})")
      st.write(f"Distance from city centre: {distance} {distance_unit}")
      st.write(f"Country Code: {country_code}")
      st.write(f"Latitude: {latitude}, Longitude: {longitude}")
      st.write("---")
  else:
    st.write("No hotels found.")

def main():
    api_key = ""
    api_secret = ""
    title_template = """
    <div style="background-color:#2f3e46; padding:5px;">
    <h1 style="color:#cad2c5">GLOBE GURU</h1>
    </div>
    <hr>
    """
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpg", use_column_width=True)
    st.markdown(title_template, unsafe_allow_html=True)
    st.header("Get **Hotel options** in just a few clicks...")
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("**Disclaimer**: For privacy purposes we do not store any user data")
    st.write("""

             """)
    access_token = get_access_token(api_key, api_secret)
    if access_token:
        col1,col2,col3=st.columns(3)
        with col1:
          city_code = st.text_input("Enter City Code (e.g., PAR for Paris)")
          radius = st.number_input("Radius (default is 5 km)", min_value=1, value=5)
          radius_unit = st.selectbox("Radius Unit", ["KM", "MILE"])
        with col2:
          amenities = st.multiselect("Select Amenities", [
              "SWIMMING_POOL", "SPA", "FITNESS_CENTER", "AIR_CONDITIONING", "RESTAURANT", "PARKING", 
              "PETS_ALLOWED", "AIRPORT_SHUTTLE", "BUSINESS_CENTER", "DISABLED_FACILITIES", "WIFI", 
              "MEETING_ROOMS", "NO_KID_ALLOWED", "TENNIS", "GOLF", "KITCHEN", "ANIMAL_WATCHING", 
              "BABY_SITTING", "BEACH", "CASINO", "JACUZZI", "SAUNA", "SOLARIUM", "MASSAGE", 
              "VALET_PARKING", "BAR", "LOUNGE", "KIDS_WELCOME", "NO_PORN_FILMS", "MINIBAR", 
              "TELEVISION", "WI-FI_IN_ROOM", "ROOM_SERVICE", "GUARDED_PARKG", "SERV_SPEC_MENU"
          ])
          ratings = st.multiselect("Select Ratings", ["1", "2", "3", "4", "5"])

        if st.button("Search Hotels"):
            with st.spinner("Fetching Hotel Data..."):
                st.markdown("<hr>",unsafe_allow_html=True)
                if not city_code:
                    st.error("Please enter a city code.")
                    return

                hotel_data = fetch_hotels_by_city(access_token, city_code, radius, radius_unit, amenities, ratings)
                if hotel_data:
                    display_hotel_data(hotel_data)

if __name__ == "__main__":
    main()
