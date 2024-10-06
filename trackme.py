import streamlit as st
import folium
from streamlit_folium import folium_static
from opencage.geocoder import OpenCageGeocode
import numpy as np
import time

# Replace 'your_api_key' with your actual OpenCage API key
API_KEY = '5b50cdc5c4b64bd086edc3a33fb4610d'  # Make sure to replace this with your API key
geocoder = OpenCageGeocode(API_KEY)

# Starting coordinates (default location if geolocation fails)
start_coords = (12.6608, 77.4496)

st.title("Track me")

# Input for the destination
destination = st.text_input("Enter destination (place name or address):")

if destination:
    # Get the location of the destination
    results = geocoder.geocode(destination)

    if results:
        # Get destination coordinates
        dest_coords = (results[0]['geometry']['lat'], results[0]['geometry']['lng'])

        # Create a map
        m = folium.Map(location=start_coords, zoom_start=12)

        # Add starting point marker
        folium.Marker(start_coords, popup='Your Location', icon=folium.Icon(color='blue')).add_to(m)

        # Add destination point marker
        folium.Marker(dest_coords, popup='Destination', icon=folium.Icon(color='green')).add_to(m)

        # Add a line between the start and destination
        folium.PolyLine([start_coords, dest_coords], color='red', weight=2.5, opacity=1).add_to(m)

        # Initial rendering of the map
        folium_static(m)

        # Button to start the animation
        if st.button("ⓘ"):
            # Generate points along the route for animation (3 main frames)
            num_points = 3  # Main frames along the route
            line_coords = np.linspace(start_coords, dest_coords, num_points)

            # 4th frame: Red pointer outside 10 km radius but near starting point
            outside_radius_coord = (start_coords[0] + 0.1, start_coords[1] + 0.1)  # Near starting point but outside radius

            # 5th frame: Calculate a point along the path for notification (somewhere near the middle)
            notification_coord = line_coords[1]  # Choose the second point on the path for the notification

            descriptions = [
                "1st : Your live location is being monitored.",
                "2nd : The car starts moving towards the destination.",
                "3rd : The destination is reached safely.",
                "4th : The car is outside the 10 km radius and a notification is triggered.",
                "5th : A notification has been triggered along the path if the car stops for more than 5mins."
            ]

            # Create a moving marker
            for i, coord in enumerate(line_coords):
                # Reset map for animation
                m = folium.Map(location=start_coords, zoom_start=12)

                # Add starting point marker again
                folium.Marker(start_coords, popup='Your Location', icon=folium.Icon(color='blue')).add_to(m)

                # Add destination point marker again
                folium.Marker(dest_coords, popup='Destination', icon=folium.Icon(color='green')).add_to(m)

                # Add a line between the start and destination again
                folium.PolyLine([start_coords, dest_coords], color='red', weight=2.5, opacity=1).add_to(m)

                # Add the car marker at the current position
                folium.Marker(location=(coord[0], coord[1]), icon=folium.Icon(color='red', icon='car')).add_to(m)

                # Add a circle with a radius of 10 km around the current position
                if i < 3:  # Show radius only for the first three frames
                    folium.Circle(
                        location=(coord[0], coord[1]),  # Circle around the car's current position
                        radius=10000,  # 10 km in meters
                        color='black',
                        fill=True,
                        fill_opacity=0.1,  # Adjust opacity for visibility
                        stroke=True,
                        weight=2,
                        popup="10 km Radius"
                    ).add_to(m)

                # Render the updated map
                folium_static(m)

                # Show the description below the map
                st.write(descriptions[i])

                # Sleep to create animation effect
                time.sleep(1)  # Adjust speed of animation as needed

            # 4th frame: Pointer outside the 10 km radius near the starting point, with a notification
            st.write(descriptions[3])

            # Reset map for 4th frame
            m = folium.Map(location=start_coords, zoom_start=12)

            # Add starting point marker again
            folium.Marker(start_coords, popup='Your Location', icon=folium.Icon(color='blue')).add_to(m)

            # Add destination point marker again
            folium.Marker(dest_coords, popup='Destination', icon=folium.Icon(color='green')).add_to(m)

            # Add a line between the start and destination again
            folium.PolyLine([start_coords, dest_coords], color='red', weight=2.5, opacity=1).add_to(m)

            # Place the red pointer outside the 10 km radius near the starting point
            folium.Marker(location=(outside_radius_coord[0], outside_radius_coord[1]), icon=folium.Icon(color='red', icon='car')).add_to(m)

            # Place the notification symbol (orange bell) next to the red pointer
            folium.Marker(location=(outside_radius_coord[0] + 0.01, outside_radius_coord[1]), 
                          icon=folium.Icon(color='orange', icon='bell', prefix='fa')).add_to(m)

            # Render the updated map for the 4th frame with the red pointer outside the radius and notification
            folium_static(m)

            # 5th frame for notification at the point on the path
            st.write(descriptions[4])

            # Reset map for notification frame
            m = folium.Map(location=start_coords, zoom_start=12)

            # Add starting point marker again
            folium.Marker(start_coords, popup='Your Location', icon=folium.Icon(color='blue')).add_to(m)

            # Add destination point marker again
            folium.Marker(dest_coords, popup='Destination', icon=folium.Icon(color='green')).add_to(m)

            # Add a line between the start and destination again
            folium.PolyLine([start_coords, dest_coords], color='red', weight=2.5, opacity=1).add_to(m)

            # Place the notification symbol (orange bell) on the path at notification_coord
            folium.Marker(location=(notification_coord[0], notification_coord[1]), 
                          icon=folium.Icon(color='orange', icon='bell', prefix='fa')).add_to(m)

            # Render the updated map for the 5th frame with the notification
            folium_static(m)

    else:
        st.error("Could not find the specified location. Please check the name or address.")
