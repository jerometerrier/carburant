# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events

# loc_button = Button(label="Get Location")
# loc_button.js_on_event("button_click", CustomJS(code="""
#     navigator.geolocation.getCurrentPosition(
#         (loc) => {
#             document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
#         }
#     )
#     """))
# result = streamlit_bokeh_events(
#     loc_button,
#     events="GET_LOCATION",
#     key="get_location",
#     refresh_on_update=False,
#     override_height=75,
#     debounce_time=0)
# st.write(result)

import streamlit as st
from geopy import Point
from geopy.distance import distance
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

@st.cache(allow_output_mutation=True)
def read_data():
	df = pd.read_csv('src/prix-carburants-fichier-instantane-test-ods-copie.csv', sep=';')
	df['lat'] = [x.split(',')[0] for x in df['geom']]
	df['lon'] = [x.split(',')[1] for x in df['geom']]
	return df

def calculate_distance(df, lat, long):
	df['distance_km'] = df.apply(lambda row: distance(row['geom'], (lat, long)).km if row['geom'] is not None else float('nan'), axis=1)
	return df

def get_location(adresse):
	geolocator = Nominatim(user_agent="carburant")
	location = geolocator.geocode(adresse)
	return location





data_load_state = st.text('Loading data...')
df = read_data()
data_load_state = st.text('Data loaded succesfully!!')

adresse = st.text_input("Adresse")
location = get_location(adresse)
df2 = calculate_distance(df, location.latitude, location.longitude)

st.write(df2[df2['distance_km'] < 5][["ville", 'prix_valeur', 'prix_nom', 'prix_maj', 'geom', 'lat','lon']])

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)


st.write(df)
# map1 = folium.Map(
#     location=[59.338315,18.089960],
#     tiles='cartodbpositron',
#     zoom_start=12,
# )
# df.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]]).add_to(map1), axis=1)
# map1