import streamlit as st
st.set_page_config(
    page_title="Destination_Insights: GLOBE GURU",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)
from openai import OpenAI
from fpdf import FPDF

#Function to get itinerary from gpt
def generate_itinerary(interests, place, days, budget, travel_origin, expert, api_key):

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Define the system message template
    system_message = ("You are a [expert], who helps people plan a travel itinerary based on their "
                      "[budget], [interests], from [travel_origin] to [city] for [days] days,make sure to take into account the budget of the user"
                      "in context with the travel_origin, and what kind of places they will be able to go with their budget, create a detailed"
                      "itinerary and be creative while keeping it concise, give a day by day analysis on what they can do during the day"
                    )
    
    # Create the user message for few-shot prompting
    user_message_tuning=("\n interests: Art,Culture,History \n days:3 \n expert:Professional Travel Planner \n budget: 3000$ \n "
                            "travel_origin: New York \n place: Paris \n")
    
    #Create assistant response for user_message_tuning
    assistant_message_tuning=("""
                                As a professional travel planner, I've crafted three detailed 3-day travel itineraries for your trip from New York to Paris with a budget of $3000. These itineraries focus on your interests in art, culture, and history. Each option includes a day-by-day analysis to help you make the most of your time in the City of Light.

                                Option 1: Classic Paris Experience

                                Day 1: Arrival and Montmartre
                                - Morning: Arrive in Paris, transfer to your hotel.
                                - Afternoon: Explore Montmartre, visit the Sacré-Cœur Basilica. Wander through the charming streets and artist studios of Place du Tertre.
                                - Evening: Enjoy dinner at a local bistro in Montmartre, soaking in the bohemian atmosphere.

                                Day 2: Louvre and Historical Paris
                                - Morning: Visit the Louvre Museum, see iconic artworks like the Mona Lisa and Venus de Milo.
                                - Afternoon: Walk through the Tuileries Garden and visit Place de la Concorde. Head to Île de la Cité to visit Notre-Dame Cathedral and Sainte-Chapelle.
                                - Evening: Seine River Cruise for a romantic view of Paris by night, followed by dinner in the Latin Quarter.

                                Day 3: Versailles Day Trip
                                - Morning: Take a train to Versailles, explore the Palace and Gardens of Versailles.
                                - Afternoon: Continue exploring the gardens, visit the Trianon Palaces and Marie-Antoinette’s Estate.
                                - Evening: Return to Paris, have a leisurely dinner near your hotel.

                                Option 2: Hidden Gems of Paris

                                Day 1: Arrival and Le Marais
                                - Morning: Arrive in Paris, transfer to your hotel.
                                - Afternoon: Explore Le Marais, visit the Place des Vosges and the Picasso Museum. Wander through hidden courtyards and discover boutique shops.
                                - Evening: Dinner at a historic bistro in Le Marais, enjoying the vibrant nightlife.

                                Day 2: Latin Quarter and Art Nouveau
                                - Morning: Visit the Cluny Museum for medieval art and artifacts. Explore the Latin Quarter, visit hidden churches like Saint-Étienne-du-Mont.
                                - Afternoon: Walk along the Seine, visit Shakespeare and Company bookstore. Head to the 16th arrondissement to admire Art Nouveau architecture.
                                - Evening: Dinner at a cozy restaurant in the Latin Quarter, followed by a visit to a local jazz club.

                                Day 3: Modern Art and Culture
                                - Morning: Explore the Pompidou Centre, admire modern and contemporary art.
                                - Afternoon: Visit the Musée d'Orsay for Impressionist and Post-Impressionist art. Take a stroll through the beautiful Musée Rodin gardens.
                                - Evening: Dinner in the Marais, visit a rooftop bar for panoramic views.

                                Option 3: Luxurious Paris with Historical Insights

                                Day 1: Arrival and Saint-Germain-des-Prés
                                - Morning: Arrive in Paris, transfer to a luxury hotel.
                                - Afternoon: Explore Saint-Germain-des-Prés, visit the Abbey of Saint-Germain-des-Prés and the nearby cafés.
                                - Evening: Dinner at a Michelin-starred restaurant, enjoying exquisite French cuisine.

                                Day 2: Versailles with Private Guide
                                - Morning: Private guided tour of the Palace of Versailles, including the Hall of Mirrors and the Royal Apartments.
                                - Afternoon: Explore the gardens and Trianon Palaces with your guide, picnic by the Grand Canal.
                                - Evening: Return to Paris, Seine River Dinner Cruise for a luxurious experience.

                                Day 3: Montmartre and Historical Landmarks
                                - Morning: Private tour of Montmartre, visit the Sacré-Cœur Basilica and explore artist studios.
                                - Afternoon: VIP tour of the Louvre Museum, focusing on masterpieces and historical insights.
                                - Evening: Dinner at a famous Montmartre restaurant, enjoy the artistic and lively ambiance.

                                Budget Considerations
                                - Flights: Approx. $700-$1000 round-trip from New York to Paris.
                                - Accommodation: Depending on your choice, $100-$300 per night.
                                - Meals: Average $30-$100 per day.
                                - Activities: Museum passes, guided tours, and transportation within the city.

                                Each option offers a unique blend of Parisian art, culture, and history, ensuring a memorable and enriching experience within your budget.
                                """)
 
    #Create the user message for generating itinerary
    user_message=(f"\n interests: {interests} \n days:{days} \n expert:{expert} \n budget: {budget} \n "
                    f"travel_origin: {travel_origin} \n place: {place} \n")

    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.9,
        n=3,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Extract and store all three response contents
    responses = [choice.message.content for choice in response.choices]

    # Return the list of all three responses
    return responses

#function to generate the PDF
def text_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = text, ln = True, align = 'C')
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

#main body of the page
def Build_Page():
    api_key=""
    title_template = """
    <div style="background-color:#333333; padding:5px;">
    <h1 style="color:cyan">GLOBE GURU</h1>
    </div>
    """
    st.sidebar.subheader("MENU")
    st.sidebar.image("logo.jpg",use_column_width=True)
    st.markdown(title_template,unsafe_allow_html=True)
    st.header("Get your **Itinerary** in just a few clicks...")
    st.write("**Disclaimer**: For privacy purposes we do not store any user data")

    #getting the city that user wants to travel to
    place=st.text_input("Enter your Destination")

    #getting the number of days
    days=st.text_input("Enter the number of days you plan to travel for")

    #getting interest of users using multiselectbox
    next_line_space=""
    st.write(next_line_space)
    interests = st.multiselect('Select your interests:',
    ['Art', 'History', 'Culture', 'Heritage', 'Culinary Experiences', 'Adventure', 'Nature & Wildlife', 'Outdoor Activities', 'Architecture', 'Music & Performing Arts', 'Sports & Recreation', 'Wellness & Spa', 'Shopping & Markets', 'Nightlife & Entertainment', 'Festivals & Events', 'Photography', 'No preferences'])

    #Currency Selection
    currency = st.selectbox(
        'Choose your currency:',
        ['USD - Dollars', 'EUR - Euros', 'GBP - Pounds', 'INR - Indian Rupees']
    )

    # Set budget ranges based on the selected currency
    if currency == 'USD - Dollars':
        min_budget = 100
        max_budget = 10000
        default_budget = 1000
        step = 100
    elif currency == 'EUR - Euros':
        min_budget = 100
        max_budget = 100000
        default_budget = 1000
        step = 100
    elif currency == 'GBP - Pounds':
        min_budget = 100
        max_budget = 100000
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

    #Store the budget along with the currency in a single variable
    budget_with_currency = {'budget': budget, 'currency': currency.split(" - ")[1]}

    #Getting input of where the user is travelling from
    travel_origin = st.text_input('Where are you traveling from?')

    #Selecting from our wide range of experts
    expert = st.selectbox('Select your expert', ["Seasoned Traveler", "Local Tour Guide", "Travel Enthusiast", "Luxury Travel Consultant", "Local Insider", "Experienced Travel Planner", "Professional Travel Guide"])

    pdf_text = ""  # Initialize pdf_text variable

    #Calling the generate_options function
    if st.button('Get Travel Options'):
        if interests and place and budget and currency and travel_origin and days and expert:
            with st.spinner('Generating Options...'):
                try:
                    answer = generate_itinerary(interests, place, days, budget_with_currency, travel_origin, expert, api_key)
                    st.write('### HERE ARE A FEW OPTIONS')
                    for i in answer:
                        st.info(i)
                        st.write("\n")
                    st.write("If you like any of these options feel free to download a PDF of your Itinerary")
                    st.write("If you are not happy with the options provided, feel free to change your parameters and re-submitting to get more **insights**")
                    if(st.button("Generate PDF")):
                        response_index=st.multiselect("Choose responses you want to download",[1,2,3])
                        for i in response_index:
                            pdf_text += answer[i-1] + "\n\n"  # Append each selected response to pdf_text
                        # Convert text to PDF
                        pdf_output = text_to_pdf(pdf_text)
                        #Download link
                        st.download_button(label="Download Itinerary", data=pdf_output, file_name="Itinerary.pdf", mime="application/pdf")
                except:
                    st.error("We Ran into issues fetching options for you... \n\n Please Try again later...")
        else:
            st.error('Please provide all the required inputs.')

if __name__=="__main__":
    Build_Page()