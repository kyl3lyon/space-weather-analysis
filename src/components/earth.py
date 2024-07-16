import os
import streamlit as st
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
import math

load_dotenv()
NASA_API_KEY = os.getenv('NASA_API_KEY')

def earth():
    """Display the Earth component of the application."""

    def fetch_space_weather_events(start_date, end_date):
        base_url = "https://api.nasa.gov/DONKI/"

        events = []
        for event_type in ['GST', 'FLR', 'CME']:
            url = f"{base_url}{event_type}?startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}&api_key={NASA_API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                events.extend([{'type': event_type, **event} for event in response.json()])

        return events

    def create_interactive_globe(start_date, end_date):
        events = fetch_space_weather_events(start_date, end_date)

        fig = go.Figure()

        for event_type, color in [('GST', 'red'), ('FLR', 'yellow'), ('CME', 'blue')]:
            event_data = [e for e in events if e['type'] == event_type]
            if event_data:
                lats, lons, text = [], [], []
                for e in event_data:
                    lat, lon = get_event_coordinates(e)
                    if isinstance(lat, list):  # For GST events
                        lats.extend(lat)
                        lons.extend(lon)
                        text.extend([create_event_text(e)] * len(lat))
                    else:
                        lats.append(lat)
                        lons.append(lon)
                        text.append(create_event_text(e))

                fig.add_trace(go.Scattergeo(
                    lon = lons,
                    lat = lats,
                    text = text,
                    mode = 'markers',
                    marker = dict(size = 5, color = color),
                    name = event_type
                ))

        fig.update_layout(
            title = 'Global Space Weather Events',
            geo = dict(
                showland = True,
                showcountries = True,
                showocean = True,
                countrywidth = 0.5,
                landcolor = 'rgb(40, 40, 40)',
                oceancolor = 'rgb(20, 20, 40)',
                bgcolor = 'rgb(10, 10, 20)',
                projection = dict(type = 'orthographic')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )

        return fig, events

    def get_event_coordinates(event):
        event_type = event['type']
        if event_type == 'CME':
            # Plot CMEs on the sun-facing side of Earth
            return 0, -90
        elif event_type == 'FLR':
            # Convert solar coordinates to lat/lon
            location = event.get('sourceLocation', '')
            return convert_solar_coordinates(location)
        elif event_type == 'GST':
            # For GST, create a ring of points around the Earth
            return create_gst_ring()
        else:
            return 0, 0

    def create_gst_ring(num_points=12):
        lats, lons = [], []
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            lats.append(30 * math.sin(angle))  # 30 degrees latitude ring
            lons.append(180 * math.cos(angle) / math.pi)
        return lats, lons

    def convert_solar_coordinates(location):
        if not location:
            return 0, 0

        try:
            ns, ew = location[0], location[1:]
            lat = float(ew[:-1])
            lon = -90 if ew[-1] == 'W' else 90

            if ns == 'S':
                lat = -lat

            # Adjust longitude to be relative to Earth's center
            lon = (lon / 180) * 90  # Scale from [-180, 180] to [-90, 90]

            return lat, lon
        except ValueError:
            return 0, 0

    def create_event_text(event):
        """Create a text description for an event, including the note if available."""
        event_type = event['type']
        basic_info = f"{event_type}: {event.get('startTime', 'Time not available')}"
        note = event.get('note', '')
        return f"{basic_info}\n\nNote: {note}" if note else basic_info

    # Execution
    col1, col2 = st.columns(2)

    with col1:
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        fig, events = create_interactive_globe(start_date, end_date)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        tab1, tab2 = st.tabs(["About", "Data Table"])

        with tab1:
            st.markdown(
                """
                <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <h3>Event Types</h3>
                    <ul>
                        <li>🔴 <strong>GST (Red)</strong>: Geomagnetic Storms</li>
                        <li>🟡 <strong>FLR (Yellow)</strong>: Solar Flares</li>
                        <li>🔵 <strong>CME (Blue)</strong>: Coronal Mass Ejections</li>
                    </ul>
                </div>
                """, 
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <h3>Last Update</h3>
                    <p style='font-size: 24px; text-align: center; color: #1E90FF;'>{}</p>
                </div>
                """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
                    <h3>About the Data</h3>
                    <p>This data is sourced from NASA's DONKI (Database Of Notifications, Knowledge, Information) API. 
                    It provides near real-time information about space weather phenomena.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        with tab2:
            df = pd.DataFrame(events)
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    earth()