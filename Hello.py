import streamlit as st
import pydeck as pdk
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Edmonton Neighbourhood Social Vulnerability",page_icon="📊")

# Function to map score to color
def get_color_for_score(score, min_score, max_score):
    normalized_score = (score - min_score) / (max_score - min_score)
    red = int(255 * normalized_score)
    green = 255 - red
    blue = 0
    return [red, green, blue, 255]

@st.cache_data
def get_data():
    return pd.read_csv('data/neighbourhood_scores_subset.csv')

data = get_data()
geojson_file_path = 'data/new_geom.geojson'
with open(geojson_file_path) as f:
    geojson_data = json.load(f)

# Create a DataFrame from the GeoJSON properties
#geojson_df = pd.DataFrame(geojson_data['features'])
#geojson_df['neighbourhood'] = geojson_df['properties'].apply(lambda x: x['neighbourhood'])
# Step 2: Color Mapping
data['color'] = data['weighted_score'].apply(lambda x: get_color_for_score(x, data['weighted_score'].min(), data['weighted_score'].max()))

# Step 3: Merge Data with GeoJSON
for feature in geojson_data['features']:
    neighborhood_name = feature['properties']['neighbourhood']
    matching_row = data[data['neighbourhood'] == neighborhood_name].iloc[0]
    feature['properties']['color'] = matching_row['color']
# Join the data with GeoJSON
#data = data.merge(geojson_df, on='neighbourhood')
score_map = data.set_index('neighbourhood')['weighted_score'].to_dict()
st.title("Edmonton Neighbourhood Social Vulnerability")

# Sidebar text
st.sidebar.markdown(
"""
This application is a working prototype of the Neighborhood Social Vulnerability Map and 
Scoring System. There are currently issues with the tooltips for the hexagon layer.
Below you will find sliders to alter the map's appearance and filter by score.
Detailed information about the project can be found near the top of the sidebar - click on 'methodology'.
""")
# Sidebar options
st.sidebar.title("Options")
score_range = st.sidebar.slider(
    "Filter Weighted Scores",
    int(data["weighted_score"].min()),
    int(data["weighted_score"].max()),
    (int(data["weighted_score"].min()), int(data["weighted_score"].max())),
)

# Filter data based on selected score range
filtered_data = data[
    (data["weighted_score"] >= score_range[0]) & (data["weighted_score"] <= score_range[1])
].copy()  # Create a copy of the filtered data

min_score, max_score = score_range
filtered_data['color'] = filtered_data["weighted_score"].apply(lambda x: get_color_for_score(x, min_score, max_score))


# Layer selection with checkboxes
scatterplot_visible = st.sidebar.checkbox("Show Scatterplot Layer", True)
hexagon_visible = st.sidebar.checkbox("Show Hexagon Layer", False)

# Hexagon Layer Interactivity
elevation_scale = st.sidebar.slider("Hexagon Elevation Scale", 1, 100, 10)
elevation_range_max = st.sidebar.slider("Hexagon Elevation Range Max", 100, 5000, 450)
#print(filtered_data.columns)  # Check if 'weighted_score' and 'neighbourhood' are present

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
    filtered_data,  # Fix: Provide the filtered_data DataFrame as the data source
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

map_style = st.selectbox('Select Map Style', [None, 'mapbox://styles/mapbox/light-v9', 'mapbox://styles/mapbox/dark-v9', 'mapbox://styles/mapbox/satellite-v9'])
st.write('Select your map style from the dropdown menu above.')
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

st.pydeck_chart(map_view)

st.markdown("**Neighbourhood Information**")
st.write(
    f"Displaying data for {len(filtered_data)} neighborhoods using Weighted Scores between {score_range[0]} and {score_range[1]}."
)

