import geocoder
from pymongo import MongoClient
from haversine import haversine
import clicksend_client
from clicksend_client.rest import ApiException
from pprint import pprint

# ClickSend API credentials
USERNAME = '22ise023@bnmit.in'  # Replace with your username
API_KEY = '5092A108-F269-4055-80FA-94135D386B9E'  # Replace with your API key

# Preset coordinates
PRESET_LATITUDE = 12.6608
PRESET_LONGITUDE = 77.4496

# Function to send SMS via ClickSend
def send_sms(to_number, message):
    configuration = clicksend_client.Configuration()
    configuration.username = USERNAME
    configuration.password = API_KEY

    api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

    sms_message = clicksend_client.SmsMessage(
        source="python",
        body=message,
        to=to_number
    )

    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

    try:
        api_response = api_instance.sms_send_post(sms_messages)
        pprint(api_response)
        return "Message sent successfully"
    except ApiException as e:
        return f"Exception when sending SMS: {e}"

# Function to get user's live location based on IP
def get_location():
    # Use preset coordinates instead of live geolocation
    latitude = PRESET_LATITUDE
    longitude = PRESET_LONGITUDE
    city = "Fixed City"  # Hardcoded for demonstration
    postal = "Fixed Postal Code"  # Hardcoded for demonstration
    
    # Organize the output
    print(f"Using preset location: Latitude = {latitude}, Longitude = {longitude}")
    print(f"City: {city}")
    print(f"Pin Code: {postal}")
    
    # Return a dictionary with all relevant info
    return {
        'latitude': latitude,
        'longitude': longitude,
        'city': city,
        'postal': postal
    }

# Function to find the nearest police station
def find_nearest_station(user_location):
    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')  # Adjust the connection string as needed
    db = client['safteyAlerts']  # Ensure this matches your database name
    police_stations = db['PoliceStations']

    # Initialize variables to track the nearest station
    nearest_station = None
    min_distance = float('inf')  # Start with an infinitely large distance

    # Loop through each police station in the database
    for station in police_stations.find():
        # Get the latitude and longitude of the station
        station_location = (station['latitude'], station['longitude'])
        
        # Calculate the distance using the Haversine formula
        distance = haversine(user_location, station_location)

        # Check if this station is the closest one found so far
        if distance < min_distance:
            min_distance = distance
            nearest_station = station

    return nearest_station, min_distance

# Main flow of the program
if __name__ == "__main__":  # Corrected this line
    # Get the preset user location
    location_data = get_location()
    
    if location_data:
        latitude = location_data['latitude']
        longitude = location_data['longitude']
        
        # Create the Google Maps link with the preset coordinates
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        # If location is found, proceed to find the nearest police station using the preset location
        user_location = (latitude, longitude)
        
        # Find the nearest police station
        nearest_station, distance = find_nearest_station(user_location)

        if nearest_station:
            print(f"The nearest police station is: {nearest_station['stationName']}")
            print(f"Address: {nearest_station['address']}")
            print(f"Distance: {distance:.2f} km")

            # Prepare the SMS content
            sms_content = f"Alert: Nearest police station is {nearest_station['stationName']}, located at {nearest_station['address']}. Distance: {distance:.2f} km. View on map: {google_maps_link}"

            # Get the phone number of the nearest police station
            police_phone_number = nearest_station['phoneNumberString']
            
            # Send the SMS to the nearest police station's phone number
            sms_result = send_sms(police_phone_number, sms_content)
            print(sms_result)
        else:
            print("No police stations found.")
    else:
        print("No location available")
