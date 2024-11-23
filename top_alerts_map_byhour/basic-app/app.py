from shiny import App, render, ui

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
    ui.input_slider("hour", "Choose an Hour (UTC)", 1, 24, 1),

)


def server(input, output, session):
    


app = App(app_ui, server)
