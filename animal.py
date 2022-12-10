import base64
import pandas as pd
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output

from animal_shelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "admin"
shelter = AnimalShelter(username, password)



# class read method must support return of cursor object and accept projection json input
#df = pd.DataFrame.from_records(shelter.readAll({}))
df = pd.read_csv('/Users/tennyvongtip/projects/AAC_shelter/aac_shelter_outcomes.csv')

#########################
# Dashboard Layout / View
#########################
external_stylesheets = ['https//codepen.io/']
app = Dash(__name__, external_stylesheets=[external_stylesheets])


#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'file.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.A([
    html.Img(src='data:image/png;base64, {}'.format(encoded_image.decode()),
        style={
            'height' : '25%',
            'width'  : '25%',
            'float'  : 'left',
            'position': 'relative',
            'padding-top': 0,
            'padding-left':0,
        })
    ], href='https://www.snhu.edu'),
html.Center(html.B(html.H1('Search and Rescue Candidate Locator'))),
html.Hr(),
dcc.Dropdown(
id='select_categories',
options=[
    {'label': 'All', 'value': 'All'},
    {'label': 'Water Rescue', 'value': 'MWR'},
    {'label': 'Mountain or Wilderness Rescue', 'value': 'MWR'},
    {'label': 'Disaster/Individual Tracking', 'value': 'DIT'}
],
    value='All'

),
html.Div(className='row',
            style={'display' : 'flex'},
            children=[
                    html.Button(id='submit-button-one', n_clicks=0, children='Cats'),
                    html.Button(id='submit-button-two', n_clicks=0, children='Dogs')
            ]),
dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),  # imports DATA
        editable=False,  #start of data Table
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable=False,
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size =10,
    ),
html.Br(),
html.Hr(),
html.Div(className='row',
        style={'display' : 'flex'},
        children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
           id='map-id',
           className='col s12 m6',
            ),

        ]),
    html.Br(),
    html.Hr(),
    html.Header("Tenny Vongtip")
    ])

#############################################
# Interaction Between Components / Controller
#############################################
#This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_map(viewData):
    dff = pd.DataFrame.from_dict(viewData)
    # Austin, TX is at [30.75, -97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=[30.75,-97.48], children=[
                dl.Tooltip(dff.iloc[0,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[1,9])
                ])
            ])
        ])
    ]
app
