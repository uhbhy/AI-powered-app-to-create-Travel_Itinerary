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


import json
import sqlite3
from datetime import datetime
import requests
import pandas as pd
import certifi

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

# Function to fetch flight offers from Amadeus API using access token
def fetch_flight_offers(access_token, origin, destination, departure_date, adults, children, currency, return_date=None):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "currencyCode": currency,
        "adults": adults,
        "children": children,
        "max": 5
    }
    if return_date:
        params["returnDate"] = return_date
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, params=params, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching flight offers: {response.text}")
        return None

# Function to parse and store flight data in SQLite database
def store_flight_data(flight_data):
    # Clear the database first
    clear_database()
    # Connect to SQLite database
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS flight_offers (
            id TEXT PRIMARY KEY,
            source TEXT,
            instantTicketingRequired BOOLEAN,
            nonHomogeneous BOOLEAN,
            oneWay BOOLEAN,
            isUpsellOffer BOOLEAN,
            lastTicketingDate TEXT,
            numberOfBookableSeats INTEGER,
            price_currency TEXT,
            price_total REAL,
            price_base REAL,
            price_grandTotal REAL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS itineraries (
            flight_offer_id TEXT,
            duration TEXT,
            FOREIGN KEY(flight_offer_id) REFERENCES flight_offers(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS segments (
            flight_offer_id TEXT,
            departure_iataCode TEXT,
            departure_terminal TEXT,
            departure_time TEXT,
            arrival_iataCode TEXT,
            arrival_terminal TEXT,
            arrival_time TEXT,
            carrierCode TEXT,
            flight_number TEXT,
            aircraft_code TEXT,
            duration TEXT,
            numberOfStops INTEGER,
            blacklistedInEU BOOLEAN,
            FOREIGN KEY(flight_offer_id) REFERENCES flight_offers(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS traveler_pricings (
            traveler_id TEXT,
            flight_offer_id TEXT,
            fareOption TEXT,
            travelerType TEXT,
            price_currency TEXT,
            price_total REAL,
            price_base REAL,
            FOREIGN KEY(flight_offer_id) REFERENCES flight_offers(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS fare_details (
            segment_id INTEGER,
            traveler_id TEXT,
            cabin TEXT,
            fareBasis TEXT,
            brandedFare TEXT,
            brandedFareLabel TEXT,
            class TEXT,
            includedCheckedBags_quantity INTEGER,
            FOREIGN KEY(segment_id) REFERENCES segments(id),
            FOREIGN KEY(traveler_id) REFERENCES traveler_pricings(traveler_id)
        )
    ''')

    # Insert data into tables
    for offer in flight_data['data']:
        c.execute('''
            INSERT OR REPLACE INTO flight_offers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            offer['id'],
            offer['source'],
            offer['instantTicketingRequired'],
            offer['nonHomogeneous'],
            offer['oneWay'],
            offer['isUpsellOffer'],
            offer['lastTicketingDate'],
            offer['numberOfBookableSeats'],
            offer['price']['currency'],
            offer['price']['total'],
            offer['price']['base'],
            offer['price']['grandTotal']
        ))

        for itinerary in offer['itineraries']:
            c.execute('''
                INSERT OR REPLACE INTO itineraries VALUES (?, ?)
            ''', (
                offer['id'],
                itinerary['duration']
            ))

            for segment in itinerary['segments']:
                c.execute('''
                    INSERT OR REPLACE INTO segments (
                        flight_offer_id, departure_iataCode, departure_terminal, departure_time,
                        arrival_iataCode, arrival_terminal, arrival_time, carrierCode,
                        flight_number, aircraft_code, duration, numberOfStops, blacklistedInEU
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    offer['id'],
                    segment['departure']['iataCode'],
                    segment['departure'].get('terminal'),
                    segment['departure']['at'],
                    segment['arrival']['iataCode'],
                    segment['arrival'].get('terminal'),
                    segment['arrival']['at'],
                    segment['carrierCode'],
                    segment['number'],
                    segment['aircraft']['code'],
                    segment['duration'],
                    segment['numberOfStops'],
                    segment['blacklistedInEU']
                ))

        for traveler in offer['travelerPricings']:
            c.execute('''
                INSERT OR REPLACE INTO traveler_pricings VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                traveler['travelerId'],
                offer['id'],
                traveler['fareOption'],
                traveler['travelerType'],
                traveler['price']['currency'],
                traveler['price']['total'],
                traveler['price']['base']
            ))

            for fare_detail in traveler['fareDetailsBySegment']:
                c.execute('''
                    INSERT OR REPLACE INTO fare_details (
                        segment_id, traveler_id, cabin, fareBasis, brandedFare,
                        brandedFareLabel, class, includedCheckedBags_quantity
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    fare_detail['segmentId'],
                    traveler['travelerId'],
                    fare_detail['cabin'],
                    fare_detail['fareBasis'],
                    fare_detail['brandedFare'],
                    fare_detail['brandedFareLabel'],
                    fare_detail['class'],
                    fare_detail['includedCheckedBags']['quantity']
                ))

    # Commit the transaction
    conn.commit()
    conn.close()

# Function to clear all records from the database
def clear_database():
    # Connect to SQLite database
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()

    # Delete all records from tables
    c.execute('DELETE FROM flight_offers')
    c.execute('DELETE FROM itineraries')
    c.execute('DELETE FROM segments')
    c.execute('DELETE FROM traveler_pricings')
    c.execute('DELETE FROM fare_details')

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Function to handle button click
def show_segment(row_ID):
    st.session_state['row_ID'] = row_ID

# Function to query the database and display the flight
def display_flight_data():
    # Connect to SQLite database
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()

    # Query flight offers data
    c.execute('''
        SELECT id, lastTicketingDate, price_currency, price_total
        FROM flight_offers
    ''')
    flight_offers = c.fetchall()

    # Query segments data
    c.execute('''
        SELECT 
            flight_offer_id, 
            departure_iataCode, 
            departure_terminal, 
            departure_time, 
            arrival_iataCode, 
            arrival_terminal, 
            arrival_time, 
            carrierCode, 
            flight_number, 
            aircraft_code, 
            duration
        FROM segments
    ''')
    segments = c.fetchall()

    # Convert to pandas DataFrame for tabular display
    flight_offers_df = pd.DataFrame(flight_offers, columns=[
        'ID', 'Last Ticketing Date', 'Price Currency', 'Price Total'])

    segments_df = pd.DataFrame(segments, columns=[
        'Flight Offer ID', 'Departure IATA Code', 'Departure Terminal', 'Departure Time', 
        'Arrival IATA Code', 'Arrival Terminal', 'Arrival Time', 'Carrier Code', 'Flight Number', 
        'Aircraft Code', 'Duration'])

    # Display data in tabular format
    st.write('### Flight Offers')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.write('ID')
    col2.write('Last Ticketing Date')
    col3.write('Price Currency')
    col4.write('Price Total')
    # Iterate over the DataFrame and create buttons for each row
    for index, row in flight_offers_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(row['ID'])
        col2.write(row['Last Ticketing Date'])
        col3.write(row['Price Currency'])
        col4.write(row['Price Total'])
        button_label = f'Show Segments {row["ID"]}'
        if col5.button(button_label, key=f"button_{row['ID']}"):
            st.session_state['row_ID'] = row['ID']
    st.markdown("<hr>",unsafe_allow_html=True)
    # Check if a button was clicked and display the corresponding segments
    if 'row_ID' in st.session_state:
        selected_offer_id = st.session_state['row_ID']
        st.write(f'Segments for Flight Offer ID: {selected_offer_id}')
        if selected_offer_id in segments_df['Flight Offer ID'].values:
            selected_segments_df = segments_df[segments_df['Flight Offer ID'] == selected_offer_id]
            st.table(selected_segments_df)

    conn.close()

# Main body of the page
def Build_Page():
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
    st.header("Get **Flight options** in just a few clicks...")
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write("**Disclaimer**: For privacy purposes we do not store any user data")
    col1,col2,col3=st.columns(3)
    with col1:
        # Getting the city that user wants to travel to
        place = st.text_input("Enter your Destination")

        # Getting input of where the user is travelling from
        travel_origin = st.text_input('Where are you traveling from?')
        departure_date = st.date_input('Enter Departure Date:')
        return_date = st.date_input('Enter Return Date (optional):', None)
    
    with col2:
        number_of_adults = st.text_input("Enter Number of Adults travelling")
        number_of_children = st.text_input("Enter number of children travelling")

        # Currency Selection
        currency = st.selectbox("Choose the currency for your flights", ["USD", "PKR", "EURO", "CAD"])

    # Top-level button to display the Flight Data
    if 'show_flights' not in st.session_state:
        st.session_state['show_flights'] = False
    if st.button("Get Flights"):
        st.session_state['show_flights']=True
        st.markdown("<hr>",unsafe_allow_html=True)

    if st.session_state['show_flights']:
        # Only execute if all required fields are provided
        if place and travel_origin and departure_date and number_of_adults:
            departure_date_str = departure_date.strftime('%Y-%m-%d')
            return_date_str = return_date.strftime('%Y-%m-%d') if return_date else None
            access_token = get_access_token(api_key, api_secret)
            with st.spinner("Fetching flights for you..."):
                if access_token:
                    flight_data = fetch_flight_offers(
                        access_token, travel_origin, place, departure_date_str, number_of_adults, number_of_children, currency, return_date_str
                    )
                    if flight_data:
                        store_flight_data(flight_data)
                        display_flight_data()
                    else:
                        st.error("Failed to fetch flight data.")
        else:
            st.error("Please provide all required information.")

# Function to generate buttons as HTML
def make_button(id):
    return f'<button onclick="alert(\'Button {id} clicked\')">Button {id}</button>'

if __name__ == "__main__":
    Build_Page()
