# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import PIL
import io
from tensorflow.keras.models import load_model
import datetime
from dash.dependencies import Input, Output, State
import base64



# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

column = dbc.Col([
    dcc.Markdown(
        """
        # Here you can upload your picture
        ### Please use a jpeg-file. The neural net expects width = 640 pixels and height = 480 pixels.
        > The app will adjust your picture to those dimensions. Please note that if the picture
        differs too strongly, the model might not work properly. 
        """
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a File')
        ]),
        style={
            'width':'100%',
            'height':'60px',
            'lineHeight':'60px',
            'borderWidth':'1px',
            'borderStyle':'dashed',
            'borderRadius':'5px',
            'text-align':'center',
            'margin':'10px'
        }
    ),
    html.Hr(),
    html.Div(id='output-data-upload')
],
style={
    'text-align':'center'
},
md=12,
)

# Begin parse
def parse_contents(contents, filename, date):
    try:
        # Transform the jpeg to width = 640, height= 480
        # returns pic
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        pic = io.BytesIO(decoded)
        #np_decoded = np.frombuffer(decoded)
        print(type(pic))
        print(pic)
        #pic = PIL.Image.open(content_string)
        #pic = pic.resize((640, 480))
        #pic = decoded.astype("float64")
        pic = np.array(pic)
        pic = np.swapaxes(pic,0,1)
        pic = pic.reshape((1,) + pic.shape)  
        pic = pic.astype("float64")
        # Feed into model -> Get prediction!
        model = pickle.load(open('./second_attempt.h5', 'rb'))
        prediction = model.predict(pic)

        
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    if prediction[0][0] == 0:
        return html.Div([
            html.H1(filename, style={'color':'#ededed'}),
            html.H2('Hotdog!!!',
            style = {
                'color':'green'
            })#,
            #dcc.Markdown(
            #    """
            #    ### This is the lightcurve:
            #    """
            #),
            #html.Div([dcc.Graph(id='curve-final', figure=curve_final)],
            #className = "d-flex justify-content-center"
            #)
        ])
    else:
        return html.Div([
            html.H1(filename, style={'color':'#ededed'}),
            html.H2('No Hotdog :-(',
            style = {
                'color':'red'
            })#,
            #dcc.Markdown(
            #    """
                ### This is the lightcurve:
            #    """
            #),
            #html.Div([dcc.Graph(id='curve-final', figure=curve_final)],
            #className = "d-flex justify-content-center"
            #)
            
        ])
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)
        ]
        return children

layout = dbc.Row([column])