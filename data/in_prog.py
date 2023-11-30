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

# Iterate over each feature in the GeoJSON data and add the corresponding color from the data DataFrame
for feature in geojson_data.get('features', []):
    neighborhood_name = feature.get('properties', {}).get('neighbourhood')
    if neighborhood_name:
        matching_row = data[data['neighbourhood'] == neighborhood_name].iloc[0]
        feature['properties']['color'] = matching_row['color']
        if isinstance(matching_row['the_geom'], str):
            # If the_geom is a string, try to parse it as WKT
            geom = shapely.geometry.mapping(shapely.wkt.loads(matching_row['the_geom']))
        else:
            # If the_geom is not a string, assume it's already in a GeoJSON-like format
            geom = matching_row['the_geom']
        # Convert the_geom to a Polygon if it's a MultiPolygon
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
    get_elevation=elevation_range_max,
    get_line_width=20,
    elevation_scale=elevation_scale,
    opacity=opacity,
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