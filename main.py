import streamlit as st
import requests
import streamlit_folium
import folium

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")


# Function to generate a list of countries
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    return countries_dict


# Function to generate a list of states for a selected country
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    return states_dict


# Function to generate a list of cities for a selected state and country
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    return cities_dict


# Function to create a map based on latitude and longitude
def map_creator(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)
    folium_static(m)


# Rest of your Streamlit app code, including the main logic and UI elements, comes after these function definitions

# Select location category
category = st.selectbox("Select location category",
                        ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"])

if category == "By City, State, and Country":
    # Method a: Select country, state, and city
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = [i["country"] for i in countries_dict["data"]]
        country_selected = st.selectbox("Select a country", options=countries_list)

        if country_selected:
            states_dict = generate_list_of_states(country_selected)
            states_list = [i["state"] for i in states_dict["data"]]
            state_selected = st.selectbox("Select a state", options=states_list)

            if state_selected:
                cities_dict = generate_list_of_cities(state_selected, country_selected)
                cities_list = [i["city"] for i in cities_dict["data"]]
                city_selected = st.selectbox("Select a city", options=cities_list)

                if city_selected:
                    aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                    aqi_data_dict = requests.get(aqi_data_url).json()

                    if aqi_data_dict["status"] == "success":
                        # Display weather and air quality data
                        st.write(f"## Weather and Air Quality in {city_selected}, {state_selected}, {country_selected}")
                        st.write(f"Temperature: {aqi_data_dict['data']['current']['weather']['tp']}°C")
                        st.write(f"Humidity: {aqi_data_dict['data']['current']['weather']['hu']}%")
                        st.write(f"Air Quality Index (AQI): {aqi_data_dict['data']['current']['pollution']['aqius']}")
                        # Display map
                        map_creator(aqi_data_dict['data']['location']['coordinates']['latitude'],
                                    aqi_data_dict['data']['location']['coordinates']['longitude'])
                    else:
                        st.warning("No data available for this location.")
                else:
                    st.warning("Please select a city.")
            else:
                st.warning("Please select a state.")
        else:
            st.warning("Please select a country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")

elif category == "By Nearest City (IP Address)":
    # Method b: Nearest city based on IP address
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":
        # Display weather and air quality data
        st.write(f"## Weather and Air Quality in Nearest City")
        st.write(f"Temperature: {aqi_data_dict['data']['current']['weather']['tp']}°C")
        st.write(f"Humidity: {aqi_data_dict['data']['current']['weather']['hu']}%")
        st.write(f"Air Quality Index (AQI): {aqi_data_dict['data']['current']['pollution']['aqius']}")
        # Display map
        map_creator(aqi_data_dict['data']['location']['coordinates']['latitude'],
                    aqi_data_dict['data']['location']['coordinates']['longitude'])
    else:
        st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":
    # Method c: Enter latitude and longitude
    latitude = st.text_input("Enter Latitude:")
    longitude = st.text_input("Enter Longitude:")

    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":
            # Display weather and air quality data
            st.write(f"## Weather and Air Quality at Latitude: {latitude}, Longitude: {longitude}")
            st.write(f"Temperature: {aqi_data_dict['data']['current']['weather']['tp']}°C")
            st.write(f"Humidity: {aqi_data_dict['data']['current']['weather']['hu']}%")
            st.write(f"Air Quality Index (AQI): {aqi_data_dict['data']['current']['pollution']['aqius']}")
            # Display map
            map_creator(float(latitude), float(longitude))
        else:
            st.warning("No data available for this location.")
    else:
        st.warning("Please enter latitude and longitude.")
