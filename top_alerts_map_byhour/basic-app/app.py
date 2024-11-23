from shiny import App, render, ui, reactive
from shinywidgets import render_altair, output_widget
import pandas as pd
import altair as alt
import json
import re

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
    ui.input_slider(id='hour',label= "Choose an Hour (UTC)", min=1, max=24, value=1),
    output_widget('plot'))


def server(input, output, session):
    @reactive.calc
    def df():
        df=pd.read_csv(r"C:\Users\laine\OneDrive\Documents\GitHub\problem-set-6\top_alerts_map_byhour\top_alerts_map_byhour.csv")
        return df
    
    @reactive.calc
    def choice():
        return input.type_subtype()
    
    @reactive.calc
    def type():
        return choice().split(':')[0]
    
    @reactive.calc
    def subtype():
        subtype = choice().split(':')[1]
        subtype = subtype.replace(" ", "")  # Remove extra spaces
        return subtype
    
    @reactive.calc
    def hour():
        return input.hour()
    
    @render.text
    def hour_check():
        return input.hour()

    @reactive.calc
    def subset():
        # Filter the dataframe based on selected type and subtype and hour 
        current_type = type()
        current_subtype = subtype()
        current_hour= hour()
        
        full_df=df()
        hour_subset=full_df[full_df['hour']==current_hour]
        type_subset = hour_subset[hour_subset['type'] == current_type]
        subset = type_subset[type_subset['subtype'] == current_subtype]
        return subset
    
    @reactive.calc
    def chi_geo_data():
        file_path = r"C:\Users\laine\OneDrive\Documents\GitHub\problem-set-6\Boundaries - Neighborhoods .geojson"
        with open(file_path) as f:
            chicago_geojson = json.load(f)

        geo_data = alt.Data(values=chicago_geojson["features"])
        return geo_data

    @render_altair
    def plot():
        data=subset()
        min_long=-87.93
        max_long=-87.56
        min_lat=41.65
        max_lat=42.01

        points=chart = alt.Chart(data).mark_point().encode(
        alt.X('Longitude:Q', scale=alt.Scale(domain=[min_long, max_long])),
        alt.Y('Latitude:Q', scale=alt.Scale(domain=[min_lat, max_lat])),
        alt.Size('Count:Q')
        )

        chi_map=alt.Chart(chi_geo_data()).mark_geoshape(
        fill='lightgray',
        stroke='white'
        ).encode().properties(
            width=350,
            height=500)
        
        full_plot=chi_map+points
        return full_plot


app = App(app_ui, server)
