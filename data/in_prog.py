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