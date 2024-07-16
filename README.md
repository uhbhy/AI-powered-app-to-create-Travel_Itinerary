# AI-powered-app-to-create-Travel_Itinerary
**About**
Explore the world with ease using Globe Guru, a Streamlit-powered travel itinerary generator. Simply input your destination, interests, budget, and travel details, and let Globe Guru suggest personalized itineraries tailored to your preferences. Whether you're a seasoned traveler or planning your first adventure, Globe Guru makes trip planning effortless and enjoyable.

**Features**
- Input your destination, interests, budget, and travel details.
- Receive personalized itineraries tailored to your preferences.
- Effortless trip planning in minutes.
- Explore a variety of destinations and activities.
- Not sure about where you want to travel? We can help you choose a place depending on the kind of place you prefer.
- User-friendly interface for seamless navigation.

**Technologies Used**
- Python
- Streamlit
- OpenAI API
- FPDF

**How it Works?**
- User Input: Users provide their preferences using sliders, multiselect boxes, and text inputs, which are formatted as JSON objects and stored in variables.
- OpenAI API Interaction: The application calls the OpenAI API using chat.completions.create() endpoint and passes a prompt with placeholder tokens and the JSON objects 
  entered by users.
- Model Processing: The API sends the request to the Language Model (LLM), which parses through the prompt and JSON objects to generate a response tailored to the user's input.
- Response Generation: The generated responses, which include personalized travel itineraries, are returned by the API and made available for download as a PDF format for the user's convenience.

**HERE'S A LINK TO THE APP**

[![Streamlit APP](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-powered-app-to-create-travelitinerary-uhbhy.streamlit.app/)

**DISCLAIMER**: This app is created solely for educational and testing purposes,hence the API keys and API secrets have been revoked and when the website calls the API and error message is displayed. Kindly note that it is not available for general use, as accessing the APIs require purchasing tokens from the providers.
