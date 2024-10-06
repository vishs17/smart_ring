from flask import Flask, request
import clicksend_client
from clicksend_client.rest import ApiException
from pprint import pprint
import re

app = Flask(__name__)  # Corrected __name__ instead of _name_

# Your ClickSend API credentials
USERNAME = '22ise023@bnmit.in'  # Replace with your username
API_KEY = '5092A108-F269-4055-80FA-94135D386B9E'  # Replace with your API key

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

# Validate Indian phone numbers
def is_valid_indian_number(number):
    pattern = r"^\+91[6-9]\d{9}$"  # Regex for Indian numbers (+91 followed by 10 digits)
    return re.match(pattern, number)

@app.route('/trigger', methods=['POST'])
def trigger():
    message = request.data.decode('utf-8')
    print(f'Received trigger messa.ge: {message}')
    
    # Default phone number set to +91 8123856196
    phone_number = "+917975675506"
    print(f"Sending SMS to default number: {phone_number}")

    # Validate the phone number (optional, since it's hardcoded and known to be valid)
    if not is_valid_indian_number(phone_number):
        print("Invalid phone number! Please enter a valid Indian number starting with +91.")
        return "Invalid phone number", 400

    # Use hardcoded coordinates
    latitude = 12.6608
    longitude = 77.4496
    
    # Create a Google Maps link
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    
    # Create the SMS message with the location and link
    message_to_send = f"Your current location is: Latitude = {latitude}, Longitude = {longitude}. View on map: {google_maps_link}"

    # Send the SMS with the location link
    result = send_sms(phone_number, message_to_send)
    print(result)

    return 'Message received and SMS sent', 200

if __name__ == '__main__':  # Corrected __name__ and __main__
    app.run(host='10.1.7.105', port=5000)
