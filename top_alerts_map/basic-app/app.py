from shiny import App, render, ui, reactive
import re
import pandas as pd
import altair as alt
from shinywidgets import render_altair, output_widget
import json


app_ui = ui.page_fluid(
    ui.input_select(id='type_subtype', label='Choose a type and subtype',
                    choices=['JAM: Unclassified',
                             'JAM: JAM_HEAVY_TRAFFIC',
                             'JAM: JAM_MODERATE_TRAFFIC',
                             'JAM: JAM_STAND_STILL_TRAFFIC',
                             'JAM: JAM_LIGHT_TRAFFIC',
                             'ACCIDENT: Unclassified',
                             'ACCIDENT: ACCIDENT_MAJOR',
                             'ACCIDENT: ACCIDENT_MINOR',
                             'ROAD_CLOSED: Unclassified',
                             'ROAD_CLOSED: ROAD_CLOSED_EVENT',
                             'ROAD_CLOSED: ROAD_CLOSED_CONSTRUCTION',
                             'ROAD_CLOSED: ROAD_CLOSED_HAZARD',
                             'HAZARD: Unclassified',
                             'HAZARD: ON_ROAD',
                             'HAZARD: On Shoulder',
                             'HAZARD: Weather']),
    ui.output_text_verbatim('subtype_check'),
    output_widget('test'),
    ui.output_table('table')
)

def server(input, output, session):
    
    @reactive.effect
    def choice():
        return input.type_subtype()
    
    @reactive.effect
    def type():
        return choice().split(':')[0]
    
    @reactive.effect
    def subtype():
        subtype = choice().split(':')[1]
        subtype = subtype.replace(" ", "")  # Remove extra spaces
        return subtype
    
    @render.text
    def subtype_check():
        return subtype()  # Output the subtype as text
    
    @reactive.value
    def full_df():
        return pd.read_csv(r"C:\Users\laine\OneDrive\Documents\GitHub\problem-set-6\top_alerts_map\top_alerts_map.csv")
    
    @reactive.value
    def subset():
        # Filter the dataframe based on selected type and subtype
        current_type = type()
        current_subtype = subtype()
        type_subset = full_df()[full_df()['type'] == current_type]
        subset = type_subset[type_subset['subtype'] == current_subtype]
        return subset
    
    @render.table
    def table():
        # Get the subset data and pass it to the table render function
        return subset()  # No need to use subset() as a function, it's already a DataFrame
    
    @reactive.effect
    def chi_geo_data():
        # Load the GeoJSON data for future use in a geospatial plot
        file_path = r"C:\Users\laine\OneDrive\Documents\GitHub\student30538\problem_sets\ps6\top_alerts_map\Boundaries - Neighborhoods.geojson"
        with open(file_path) as f:
            chicago_geojson = json.load(f)

        geo_data = alt.Data(values=chicago_geojson["features"])
        return geo_data
    
    @render_altair
    def test():
        # Ensure we are accessing the reactive data properly
        full_data = full_df()  # This will access the reactive value directly

        if full_data.empty:
            return alt.Chart()  # Return an empty chart if the data is empty
        
        # Filter data based on the selected type and subtype
        current_type = type()
        current_subtype = subtype()
        type_subset = full_data[full_data['type'] == current_type]
        subset = type_subset[type_subset['subtype'] == current_subtype]

        if subset.empty:
            return alt.Chart()  # Return an empty chart if the subset is empty

        # Create an Altair chart for the subset data
        plot = alt.Chart(subset()).mark_point().encode(
            alt.X('Longitude:Q', title='Longitude'),
            alt.Y('Latitude:Q', title='Latitude')
        )
        
        return plot




app = App(app_ui, server)
