# Import necessary libraries
import streamlit as st
import pydeck as pdk
import pandas as pd
import json
import math
import altair as alt
import shapely.wkt
import shapely.geometry
import numpy as np


# Set Streamlit page configuration
st.set_page_config(layout="wide", 
                   page_title="Edmonton Neighbourhood Social Vulnerability", 
                   page_icon=":earth_americas:", 
                   menu_items={
    "Get Help":'mailto:jeff.barlow.spady@gmail.com', 
    'report a bug':'mailto:jeff.barlow.spady@gmail.com',
})

import matplotlib.cm as cm
st.sidebar.title("Map Options and Filters")
st.sidebar.divider()
# Radio button for selecting color mapping mode
color_mapping_mode = st.sidebar.radio(
    "Select Color Mapping Mode",
    ("Standard", "Emphasized High Scores")
)
cmap_options = {
    "viridis": "Perceptually uniform and colorblind-friendly",
    "plasma": "Perceptually uniform with a different color range",
    "cividis": "Designed for those with color vision deficiency",
    "inferno": "Perceptually uniform, bright in the middle and dark at both ends",
    "magma": "Perceptually uniform, bright at the high end and dark at the low end",
    "coolwarm": "Two contrasting colors with a neutral color in the middle",
    "rainbow": "Spectrum of colors from red to violet",
    "jet": "A high-contrast, four-color map (not recommended for colorblind users)"
}

selected_cmap = st.sidebar.selectbox(
    "Select a color map",
    options=list(cmap_options.keys()),
    format_func=lambda x: f"{x} - {cmap_options[x]}"
)
st.sidebar.divider()
def get_color_for_score(score, min_score, max_score, mode='Standard', cmap=selected_cmap):
    """
    Maps a score to a color. 
    Mode can be 'Standard' or 'Emphasized High Scores'.

    Args:
        score (float): The score to map to a color.
        min_score (float): The minimum score in the range.
        max_score (float): The maximum score in the range.
        mode (str): The color mapping mode ('Standard' or 'Emphasized High Scores').
        cmap (str): The name of the color map to use.

    Returns:
        list: A list of RGBA values representing the color.
    """
    # Normalize the score between the minimum and maximum values
    normalized_score = (score - min_score) / (max_score - min_score)

    if mode == 'Emphasized High Scores':
        # Apply a nonlinear transformation to emphasize higher scores
        emphasized_score = np.power(normalized_score, 1)
        color = cm.get_cmap(cmap)(emphasized_score)
    else:
        # Standard linear mapping
        color = cm.get_cmap(cmap)(normalized_score)

    # Convert color from 0-1 RGB format to 0-255 RGB format, keeping alpha as 255
    return [int(channel * 255) for channel in color[:3]] + [255]



@st.cache_data
def get_data():
    """
    Retrieves and processes the data from a CSV file.
    Returns:
        pandas.DataFrame: The processed data.
    """
    try:
        data = pd.read_csv('data/neighbourhood_scores_subset.csv')

        # Check if 'the_geom' column exists
        if 'the_geom' not in data.columns:
            st.error("The 'the_geom' column is missing from the data.")
            return pd.DataFrame()

        # Convert WKT to GeoJSON
        try:
            data['geojson'] = data['the_geom'].apply(lambda x: shapely.geometry.mapping(shapely.wkt.loads(x)))
        except Exception as e:
            st.error(f"Error converting WKT to GeoJSON: {e}")
            return pd.DataFrame()

        # Apply color mapping
        data['color'] = data['weighted_score'].apply(lambda x: get_color_for_score(x, data['weighted_score'].min(), data['weighted_score'].max(), mode=color_mapping_mode,cmap=selected_cmap))
        
        return data
    except FileNotFoundError:
        st.error("Data file not found.")
        return pd.DataFrame()

data = get_data()

# Ensure that the 'geojson' column exists before proceeding
if 'geojson' in data.columns:
    # Creating a GeoJSON Feature Collection from the processed data
    geojson_features = [
        {
            'type': 'Feature',
            'geometry': row['geojson'],
            'properties': {
                'neighbourhood': row['neighbourhood'],
                'weighted_score': row['weighted_score'],
                'color': row['color']
            }
        }
        for _, row in data.iterrows()
    ]

    geojson_data = {'type': 'FeatureCollection', 'features': geojson_features}

    # ... [rest of the streamlit app setup and pydeck configuration] ...
else:
    st.error("GeoJSON data could not be created.")
# Step 2: Color Mapping
# Apply the color mapping function to the 'weighted_score' column and create a new 'color' column
#data['color'] = data['weighted_score'].apply(lambda x: get_color_for_score(x, data['weighted_score'].min(), data['weighted_score'].max()))

# Step 3: Merge Data with GeoJSON


# Set up the Streamlit application
st.title("Edmonton Neighbourhood Social Vulnerability")
st.markdown("""Analysis by Jeff Barlow-Spady""")    # Markdown text
st.divider()
# Sidebar text
st.markdown(
"""
This application is a working prototype of the Neighborhood Social Vulnerability Map and 
Scoring System. A higher score indicates more risk of vulnerability
wiithin a neighbourhood. Weighted score ranges from 5 to 16. Weighted score is calculated by aggregating the
scores of the factor loadings and feature importance scores from the Random Forest and XGBoost models.

Important Notes:
Tooltips for the hexagon and filled polygon layers are not working as I would like. This is a known issue with pydeck.
My current workaround is using the scatterplot layer as an overlay to display the tooltip, so it may feel a bit clunky for now.


On the sidebar you will find sliders to alter the map's appearance and filter by score.
A link to detailed information about the project can be found near the top of the sidebar - click on 'methodology' to learn more

You will also find a link to download the data used to create the map and the top 15 neighborhoods by weighted score.
""")
st.divider()
# Sidebar options


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
filtered_data['color'] = filtered_data["weighted_score"].apply(lambda x: get_color_for_score(x, min_score, max_score, mode=color_mapping_mode, cmap=selected_cmap))
map_style = st.sidebar.selectbox("Select your map style using this dropdown", [None, 'mapbox://styles/mapbox/light-v9', 'mapbox://styles/mapbox/dark-v9', 'mapbox://styles/mapbox/satellite-v9'])

st.sidebar.divider()
st.sidebar.markdown("""Select the layer you would like to display""")
# Layer selection with checkboxes
scatterplot_visible = st.sidebar.checkbox("Show Scatterplot Layer", True)
hexagon_visible = st.sidebar.checkbox("Show Hexagon Layer", False)
filled_polygon_visible = st.sidebar.checkbox("Show Filled Polygon Layer", True)
st.sidebar.divider()
st.sidebar.markdown("""Adjust The Height and Elevation of Hex Layer.""")
# Hexagon Layer Interactivity
elevation_scale = st.sidebar.slider("Adjust Elevation Scale", 1, 100, 10)
elevation_range_max = st.sidebar.slider("Adjust Height of hex-tiles", 100, 5000, 450)
st.sidebar.divider()
st.sidebar.markdown("""Change Point Size and Opacity""")
opacity = st.sidebar.slider("Opacity", 0.0, 1.0, 0.3)
radius = st.sidebar.slider("Point Size", 1, 500, 415)

# Function to get the appropriate tooltip based on the visible layer
def get_tooltip_for_visible_layer():
    if scatterplot_visible and not hexagon_visible and not filled_polygon_visible:
        return {
            "html": "<b>Neighbourhood:</b> {neighbourhood}<br><b>Score:</b> {weighted_score}",
            "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "14px",
            "fontFamily": "Arial, sans-serif",
            "padding": "5px",
            "border": "2px thin",
            "borderRadius": "2px",
            "boxShadow": "3px 3px 5px rgba(0, 0, 0, 0.3)",
            }
        }
    elif hexagon_visible:
        return {
            "html": "<b>Count:</b> {points}",
            "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "14px",
            "fontFamily": "Arial, sans-serif",
            "padding": "5px",
            "border": "2px thin",
            "borderRadius": "2px",
            "boxShadow": "3px 3px 5px rgba(0, 0, 0, 0.3)",
            }
        }
    elif filled_polygon_visible:
        return {
            "html": "<b>Neighbourhood:</b> {'trying to get this to work}<br><b>Score:</b> {'no luck yet. can apparently only have one tooltip at a time'}",
            "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "14px",
            "fontFamily": "Arial, sans-serif",
            "padding": "5px",
            "border": "2px thin",
            "borderRadius": "2px",
            "boxShadow": "3px 3px 5px rgba(0, 0, 0, 0.3)"
            }
        }
    else:
        return None
tooltip_text = get_tooltip_for_visible_layer()


# Define Layers


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
    get_tooltip=lambda layer: f"Count: {layer.context['count']}",
)
chloropleth_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_data,
    stroked=True,
    filled=True,
    extruded=False,
    wireframe=True,
    get_fill_color='properties.color',
    get_line_color=[0, 0, 0],
    get_line_width=30,
    visible=filled_polygon_visible,
    pickable=True,
    auto_highlight=True,
    get_polygon='properties.the_geom',
    get_position='properties.coordinates',
)
scatterplot_layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_data,
    get_position=["longitude", "latitude"],
    get_color="color",
    get_radius=radius,
    pickable=True,
    opacity=opacity,
    visible=scatterplot_visible,
    auto_highlight=True,
)
# Map view setup
view_state = pdk.ViewState(
    latitude=data["latitude"].mean(),
    longitude=data["longitude"].mean(),
    zoom=9,
    pitch=10,
    bearing=0,
)


map_view = pdk.Deck(
    map_style=map_style,
    initial_view_state=view_state,
    layers=[hexagon_layer, chloropleth_layer, scatterplot_layer],
    tooltip={
            "html": "<b>Neighbourhood:</b> {neighbourhood}<br><b>Score:</b> {weighted_score}",
            "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "14px",
            "fontFamily": "Arial, sans-serif",
            "padding": "5px",
            "border": "2px thin",
            "borderRadius": "2px",
            "boxShadow": "3px 3px 5px rgba(0, 0, 0, 0.3)",
            }
        },
)

# Render the map
st.pydeck_chart(map_view)
st.divider()
# Display information about the neighborhoods
st.markdown("**Neighbourhood Information**")
st.write(
    f"Total number of neighborhoods: {len(data)}\n"
    f"Average weighted score: {data['weighted_score'].mean():.2f}\n"
    f"Minimum weighted score: {data['weighted_score'].min():.2f}\n"
    f"Maximum weighted score: {data['weighted_score'].max():.2f}\n"
)

#Plot Chart with the top 15 neighborhoods by weighted score

top_neighborhoods = filtered_data[["neighbourhood", "weighted_score"]].sort_values(by="weighted_score", ascending=False).head(15).reset_index(drop=True)
top_neighborhoods["weighted_score"] = top_neighborhoods["weighted_score"].round(2)

chart = alt.Chart(top_neighborhoods).mark_bar().encode(
    y=alt.Y("neighbourhood", axis=alt.Axis(labelAngle=0), sort=alt.EncodingSortField(field="weighted_score", order="descending")),
    x="weighted_score",
    tooltip=["neighbourhood", "weighted_score"],
    color=alt.Color("weighted_score", scale=alt.Scale(scheme='goldred'))
).properties(
    title="Top 15 Neighborhoods by Weighted Score",
    width=600,
    height=400
).configure_mark(
    color='steelblue'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

st.divider()
# Display the chart and dataframe with a divider in between
col1, col2 = st.columns(2)
with col1:
    st.dataframe(top_neighborhoods, width=600, height=400)
with col2:
    st.altair_chart(chart)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

scores_data = convert_df(data)
st.sidebar.divider()
st.sidebar.download_button(
    label="Download score data as CSV",
    data=scores_data,
    file_name='edmonton_vulnerability_scores.csv',
    mime='text/csv',
)
top_15 = convert_df(top_neighborhoods)
st.sidebar.download_button(
    label='Download Top 15 Data as CSV',
    data=top_15,
    file_name='top_15_neighbourhoods.csv',
    mime='text/csv',
)

