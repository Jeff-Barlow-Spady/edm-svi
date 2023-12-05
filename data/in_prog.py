import shapely.wkt
def parse_geom(geom_str):
    # Parse the WKT string to a Shapely geometry
    geom = shapely.wkt.loads(geom_str)

    # Convert the Shapely geometry to GeoJSON
    geom_geojson = shapely.geometry.mapping(geom)

    return geom_geojson

# Convert the multipolygon to polygon
def convert_multipolygon_to_polygon(geom):
    if geom['type'] == 'MultiPolygon':
        polygons = []
        for polygon in geom['coordinates']:
            polygons.append(polygon[0])
        return {
            'type': 'Polygon',
            'coordinates': polygons
        }
    else:
        return geom

# Iterate over each feature in the GeoJSON data
geojson_data = {}  # Define the geojson_data variable

for feature in geojson_data.get('features', []):
    neighborhood_name = feature.get('properties', {}).get('neighbourhood')
    if neighborhood_name:
        matching_rows = data[data['neighbourhood'] == neighborhood_name]
        if not matching_rows.empty:
            matching_row = matching_rows.iloc[0]
            feature['properties']['color'] = matching_row['color']
            if isinstance(matching_row['the_geom'], str):
                geom = parse_geom(matching_row['the_geom'])
            else:
                geom = matching_row['the_geom']
            feature['properties']['the_geom'] = convert_multipolygon_to_polygon(geom)




filtered_data_dict = filtered_data[['longitude', 'latitude', 'color']].to_dict(orient='records')
chloropleth_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_data,
    stroked=False,
    filled=True,
    extruded=False,
    wireframe=True,
    get_fill_color=[185,75,75],
    get_line_color=[255, 255, 255],
    get_line_width=20,
    visible=filled_polygon_visible,
    pickable=True,
    auto_highlight=True,
    get_polygon='properties.the_geom',
    get_position='properties.coordinates',
)

# Color the chloropleth layer based on the output of get_color_from_score() or quartiles column
#filtered_data['color'] = filtered_data.apply(lambda row: get_color_from_score(row['weighted_score']), axis=1)
# or
# filtered_data['color'] = filtered_data['quartiles'].apply(lambda x: get_color_from_quartiles(x))

# Convert the filtered data to GeoJSON format


# Update the chloropleth layer with the new GeoJSON data
chloropleth_layer.data = geojson_data


import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk
import altair as alt
import math
st.sidebar.title("Map Options and Filters")
st.sidebar.divider()
# Radio button for selecting color mapping mode
color_mapping_mode = st.sidebar.radio(
    "Select Color Mapping Mode",
    ("Standard", "Emphasized High Scores")
)
cmap_options = {
    "cividis": "Designed for those with color vision deficiency",
    "viridis": "Perceptually uniform and colorblind-friendly",
    "plasma": "Perceptually uniform with a different color range",
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
        import matplotlib.pyplot as plt
        import shapely.geometry

        # Function to get color for a given score
        def get_color_for_score(score, min_score, max_score, mode, cmap):
            """
            Maps a score to a color based on the given color mapping mode and colormap.

            Args:
                score (float): The score to map to a color.
                min_score (float): The minimum score in the range.
                max_score (float): The maximum score in the range.
                mode (str): The color mapping mode.
                cmap (str): The colormap to use.

            Returns:
                list: The RGB color values in the range of 0-255.
            """
            normalized_score = (score - min_score) / (max_score - min_score)

            if mode == "emphasized":
                # Apply power transformation to emphasize higher scores
                emphasized_score = np.power(normalized_score, 1.2)
                color = plt.colormaps.get_cmap(cmap)(emphasized_score)
            else:
                # Standard linear mapping
                color = plt.colormaps.get_cmap(cmap)(normalized_score)

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

                return data
            except FileNotFoundError:
                st.error("Data file not found.")
                return pd.DataFrame()


        data = get_data()

        # Apply color mapping
        data['color'] = data['weighted_score'].apply(lambda x: get_color_for_score(x, data['weighted_score'].min(), data['weighted_score'].max(), mode=color_mapping_mode, cmap=selected_cmap))

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
        else:
            st.error("GeoJSON data could not be created.")

        # Set up the Streamlit application
        st.title("Social Vulnerability in Edmonton Neighbourhoods: Creating an Index")
        st.markdown("""Analysis by Jeff Barlow-Spady""")    # Markdown text
        st.divider()

        # ... Rest of the code ...
