# Import necessary libraries
import streamlit as st
import pydeck as pdk
import pandas as pd
import json
import math

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Edmonton Neighbourhood Social Vulnerability", page_icon="📊", menu_items={
    "Get Help":'mailto:jeff.barlow.spady@gmail.com', 
    'report a bug':'mailto:jeff.barlow.spady@gmail.com'
    })

# Function to map score to color
def get_color_for_score(score, min_score, max_score):
    """
    Maps a score to a color based on a given range of scores.
    Args:
        score (float): The score to map to a color.
        min_score (float): The minimum score in the range.
        max_score (float): The maximum score in the range.
    Returns:
        list: A list of RGBA values representing the color.
    """
    normalized_score = (score - min_score) / (max_score - min_score)
    red = int(255 * normalized_score)
    green = 255 - red
    blue = 0
    return [red, green, blue, 255]

@st.cache_data
def get_data():
    """
    Retrieves the data from a CSV file and caches it for faster access.
    Returns:
        pandas.DataFrame: The loaded data.
    """
    return pd.read_csv('data/neighbourhood_scores_subset.csv')

# Load data and GeoJSON file
data = get_data()
geojson_file_path = 'data/new_geom.geojson'
with open(geojson_file_path) as f:
    geojson_data = json.load(f)

# Step 2: Color Mapping
# Apply the color mapping function to the 'weighted_score' column and create a new 'color' column
data['color'] = data['weighted_score'].apply(lambda x: get_color_for_score(x, data['weighted_score'].min(), data['weighted_score'].max()))

# Step 3: Merge Data with GeoJSON
# Iterate over each feature in the GeoJSON data and add the corresponding color from the data DataFrame
for feature in geojson_data['features']:
    neighborhood_name = feature['properties']['neighbourhood']
    matching_row = data[data['neighbourhood'] == neighborhood_name].iloc[0]
    feature['properties']['color'] = matching_row['color']

# Set up the Streamlit application
st.title("Edmonton Neighbourhood Social Vulnerability")
st.markdown("""Analysis by Jeff Barlow-Spady""")    # Markdown text
st.divider()
# Sidebar text
st.markdown(
"""
**This application is a working prototype of the Neighborhood Social Vulnerability Map and 
Scoring System. There are currently issues with the tooltips for the hexagon layer.
On the sidebar you will find sliders to alter the map's appearance and filter by score.
Detailed information about the project can be found near the top of the sidebar - click on 'methodology'.**
""")

# Sidebar options
st.sidebar.title("Options")


# Slider to filter weighted scores
score_range = st.sidebar.slider(
    label="Filter Weighted Scores",
    min_value=int(data["weighted_score"].min()),
    max_value=math.ceil(data["weighted_score"].max()),
    value=(int(data["weighted_score"].min()), math.ceil(data["weighted_score"].max()))  # Set default value to the new maximum score
)
st.sidebar.divider()
# Filter data based on selected score range
filtered_data = data[
    (data["weighted_score"] >= score_range[0]) & (data["weighted_score"] <= score_range[1])
].copy()  # Create a copy of the filtered data

min_score, max_score = score_range

# Apply the color mapping function to the filtered data
filtered_data['color'] = filtered_data["weighted_score"].apply(lambda x: get_color_for_score(x, min_score, max_score))

st.sidebar.markdown("""Select the layer you would like to display.""")
# Layer selection with checkboxes
scatterplot_visible = st.sidebar.checkbox("Show Scatterplot Layer", True)
hexagon_visible = st.sidebar.checkbox("Show Hexagon Layer", False)
st.sidebar.divider()
st.sidebar.markdown("""Adjust The Height and Elevation of Hex Layer.""")
# Hexagon Layer Interactivity
elevation_scale = st.sidebar.slider("Adjust Elevation Scale", 1, 100, 10)
elevation_range_max = st.sidebar.slider("Adjust Height of hex-tiles", 100, 5000, 450)
st.sidebar.divider()
# Define Layers
scatterplot_layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_data,
    get_position=["longitude", "latitude"],
    get_color="color",
    get_radius=st.sidebar.slider("Point Size", 1, 500, 300),
    pickable=True,
    opacity=st.sidebar.slider("Opacity", 0.0, 1.0, 0.8),
    visible=scatterplot_visible,
)

hexagon_layer = pdk.Layer(
    "HexagonLayer",
    filtered_data,
    auto_highlight=True,
    get_position=["longitude", "latitude"],
    elevation_scale=elevation_scale,
    pickable=True,
    stroked=True,
    filled=True,
    elevation_range=[0, elevation_range_max],
    extruded=True,
    coverage=1,
    visible=hexagon_visible,
)

# Map view setup
view_state = pdk.ViewState(
    latitude=data["latitude"].mean(),
    longitude=data["longitude"].mean(),
    zoom=9,
    pitch=10,
)

map_style = st.selectbox("Select your map style using this dropdown", [None, 'mapbox://styles/mapbox/light-v9', 'mapbox://styles/mapbox/dark-v9', 'mapbox://styles/mapbox/satellite-v9'])

map_view = pdk.Deck(
    map_style=map_style,
    initial_view_state=view_state,
    layers=[scatterplot_layer, hexagon_layer],
    tooltip={
        "html": "<b>Score:</b> {weighted_score}<br><b>Neighborhood:</b> {neighbourhood}",
        "style": {"backgroundColor": "steelblue", "color": "white"},
        "hover": True,
    },
)

# Render the map
st.pydeck_chart(map_view)

# Display information about the neighborhoods
st.markdown("**Neighbourhood Information**")
st.write(
    f"Displaying data for {len(filtered_data)} neighborhoods using Weighted Scores between {score_range[0]} and {score_range[1]}."
)
