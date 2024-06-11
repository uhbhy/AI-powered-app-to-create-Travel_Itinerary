#importing packages
import streamlit as st
st.set_page_config(
    page_title="Destination_Insights: GLOBE GURU",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)
from openai import OpenAI

#function to get response from gpt
def generate_options(interests, place_type, budget, travel_origin, travel_type, continents, api_key):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Define the system message template
    system_message = ("You are a smart travel assistant, who helps people decide where they would like to go based on their "
                      "[budget], [interests], who are currently residing in [travel_origin], [travel_type:domestic/international], "
                      "[continents] and [place_type], give 3 options to the user and make sure to take into account the budget of the user"
                      "in context with the travel_origin, and what kind of places they will be able to go with their budget"
                      )
    
    # Create the user message
    user_message = (f"\n interests: {interests} \n place_type: {place_type} \n budget: {budget} \n "
                    f"travel_origin: {travel_origin} \n travel_type: {travel_type} \n continents: {continents}")
    
    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.9,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Extract and return the response content
    return response.choices[0].message.content

#main body of the page
def Insight_page():
    api_key=""
    title_template = """
    <div style="background-color:#333333; padding:5px;">
    <h1 style="color:cyan">GLOBE GURU</h1>
    </div>
    """
    st.sidebar.subheader("MENU")
    st.sidebar.image("logo.jpg",use_column_width=True)
    st.markdown(title_template,unsafe_allow_html=True)
    st.write("")
    st.header("DON'T HAVE A FIXED DESTINATION IN MIND?")
    st.subheader("WE ARE HERE TO HELP...")
    next_line_space="""

    """
    #getting interest of users using multiselectbox
    st.write(next_line_space)
    interests = st.multiselect('Select your interests:',
    ['Art', 'History', 'Culture', 'Heritage', 'Culinary Experiences', 'Adventure', 'Nature & Wildlife', 'Outdoor Activities', 'Architecture', 'Music & Performing Arts', 'Sports & Recreation', 'Wellness & Spa', 'Shopping & Markets', 'Nightlife & Entertainment', 'Festivals & Events', 'Photography', 'No preferences'])
    
    #getting the kind of place they want to visit from user
    place_type = st.multiselect(
    'What type of place do you want to visit?',
    ['Beach Area', 'Mountain Area', 'Countryside', 'City'])

    #Currency Selection
    currency = st.selectbox(
        'Choose your currency:',
        ['USD - Dollars', 'EUR - Euros', 'GBP - Pounds', 'INR - Indian Rupees']
    )

    # Set budget ranges based on the selected currency
    if currency == 'USD - Dollars':
        min_budget = 100
        max_budget = 25000
        default_budget = 1000
        step = 100
    elif currency == 'EUR - Euros':
        min_budget = 100
        max_budget = 25000
        default_budget = 1000
        step = 100
    elif currency == 'GBP - Pounds':
        min_budget = 100
        max_budget = 25000
        default_budget = 1000
        step = 100
    elif currency == 'INR - Indian Rupees':
        min_budget = 5000
        max_budget = 1000000
        default_budget = 10000
        step = 5000

    # Create slider for users to enter their budget
    budget = st.slider(
        f'Select your budget in {currency.split(" - ")[1]}:',
        min_value=min_budget,
        max_value=max_budget,
        value=default_budget,
        step=step
    )

    # Store the budget along with the currency in a single variable
    budget_with_currency = {'budget': budget, 'currency': currency.split(" - ")[1]}

    #getting input of where the user is travelling from
    travel_origin = st.text_input('Where are you traveling from?')

    # Travel preference: Domestic or International
    travel_type = st.radio(
    'Do you want to travel domestic or international?',
    ['Domestic', 'International'])

    # If the user selects international, show a multiselect box for continents
    if travel_type == 'International':
        continents = st.multiselect(
            'Select the continents you would like to visit:',
            ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Australia', 'Antarctica'])
    else:
        continents='N/A'
    
    #Calling the generate_options function
    if st.button('Get Travel Options'):
        if interests and place_type and budget and currency and travel_origin and travel_type and continents:
            with st.spinner('Generating Options...'):
                try:
                    answer = generate_options(interests, place_type, budget_with_currency, travel_origin, travel_type, continents, api_key)
                    st.write('### HERE ARE A FEW OPTIONS')
                    st.write(answer)
                    st.write("If you like any of these options feel free to navigate to the **Build_Itinerary** page to get a customized Itinerary based on your preferences")
                    st.write("If you are not happy with the options provided, feel free to change your parameters and re-submitting to get more **insights**")
                except:
                    st.error("We Ran into issues fetching options for you... \n\n Please Try again later...")
        else:
            st.error('Please provide all the required inputs.')
        
if __name__=="__main__":
    Insight_page()