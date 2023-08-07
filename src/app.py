####################################################################
################## LIBRARIES IMPORT ################################

#Note: this code has been taken from Michel Vanderhulst's thesis code to ensure the consistency of the app if another student want
#implement new features. Small changes have been done to adapt the code for the purpose of this thesis. 

## APP-RELATED LIBRARIES
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np


# Importing app header, body and graphs from the other .py scripts
from appHeader import header
from appBody import body, graphs

from mc_asian import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], #modern-looking buttons, sliders, etc
                          external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML', "./assets/mathjax.js"], #LaTeX in app
                          meta_tags=[{"content": "width=device-width"}] # app width adapts itself to the user device
                          )
server = app.server

app.layout = html.Div(
                id='main_page',
                children=[
                    dcc.Store(id='memory-output'),
                    header(),
                    body(),
                    graphs()
                         ],
                     )

@app.callback(
    [Output('memory-output', 'data'),
     Output('seed','value')],
    [Input('ModelSel', 'value'),
     Input('ModelSel2','value'),
     Input('CallOrPut', 'value'),
     Input("S","value"),
     Input("K", "value"),
     Input("rf","value"),
     Input("vol", "value"),
     Input("T","value"),
     Input("TS", "value"),
     Input("M", "value"),
     Input("MC", "value"),
     Input('seed', 'value'),
     Input('ButtonChangeStockTrajectory', 'n_clicks'),
     ])
def get_simu(ModelSel,ModelSel2,CallOrPut,S,K,mu,vol,T,TS,M,MC,seed,n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0] #Detect the input that triggered the callback and place it in change_id
    #detect if the user push on the button
    if 'ButtonChangeStockTrajectory' in changed_id: 
        seed=["RandomSeed"] 
    else:
        seed = seed if type(seed)==int else 5

    #first run of simulation to display price, SE and confidence interval
    Price,Price2,SE,SE2,seed,seed2 = Model_provider(S,K,T,mu,vol,TS,M,CallOrPut,seed, ModelSel, ModelSel2)
    PriceVec1 = []
    PriceVec2 = []
    
    #run the MC simulation multiple times to get a vector of estimated option prices
    for i in range (0,MC):    
        temp = Model_provider(S,K,T,mu,vol,TS,M,CallOrPut,seed+i, ModelSel, ModelSel2) #seed+i to move the seed for each MC
        PriceVec1.append(temp[0])
        PriceVec2.append(temp[1])
    print("Vector of prices done")

    return (Price,Price2,SE,SE2,seed, PriceVec1,PriceVec2, ModelSel, ModelSel2), seed

## PLOT
#Boxplot 
@app.callback( 
    Output('boxplot', 'figure'),
    [Input('memory-output', 'data'),]
)
def boxplot(data):
    Price,Price2,SE,SE2,seed, PriceVec1,PriceVec2, ModelSel, ModelSel2 = data
    figure={
            'data': [
                go.Box(y=PriceVec1, name=ModelSel),
                go.Box(y=PriceVec2, name=ModelSel2)
            ],
            'layout': go.Layout(
                title='Prices boxplot',
                xaxis=dict(title='Model'),
                yaxis=dict(title='Price'),
                showlegend=False
            )
        }   
    return figure

#First density plot    
@app.callback(
        Output('density1','figure'),
        [Input('memory-output', 'data'),]
)
def graph_density(data):
    Price,Price2,SE,SE2,seed, PriceVec1,PriceVec2, ModelSel, ModelSel2 = data
    title = "Price distribution using {0}".format(ModelSel)

    figure={
            'data': [
                go.Histogram(x=PriceVec1, nbinsx=10, histnorm='probability'),
                go.Scatter(x=np.linspace(min(PriceVec1), max(PriceVec1), len(PriceVec1)), y=estimated_density(PriceVec1)
                           , mode='lines', name='Estimated Density',marker=dict(color='green'), yaxis='y2')
            ],
            'layout': go.Layout(
                title=title,    
                xaxis={'title': 'Price'},
                yaxis={'title': 'Distribution'},
                yaxis2={'title': 'Estimated Density', 'overlaying': 'y', 'side': 'right'},
                showlegend=False
            )
        }
    return figure

#Second density plot
@app.callback(
        Output('density2','figure'),
        [Input('memory-output', 'data'),]
)
def graph_density(data):
    Price,Price2,SE,SE2,seed, PriceVec1,PriceVec2, ModelSel, ModelSel2 = data
    title = "Price distribution using {0}".format(ModelSel2)

    figure={
            'data': [
                go.Histogram(x=PriceVec2, nbinsx=10, histnorm='probability', name='Histogram',marker=dict(color='orange')),
                go.Scatter(x=np.linspace(min(PriceVec2), max(PriceVec2), len(PriceVec2)), y=estimated_density(PriceVec2)
                           , mode='lines', name='Estimated Density',marker=dict(color='red'), yaxis='y2')
            ],
            'layout': go.Layout(
                title=title,
                xaxis={'title': 'Price'},
                yaxis={'title': 'Distribution'},
                yaxis2={'title': 'Estimated Density', 'overlaying': 'y', 'side': 'right'},  
                showlegend=False
            )
        }
    print("All plots done")
    return figure

   
## DOUBLE-CHECKING USER INPUT 
@app.callback(Output('message_S', 'children'),
              [Input('S', 'value')])
def check_input_S(S):
    if S<0:
        return f'Cannot be lower than 0.'
    else:
        return ""
    
@app.callback(Output('message_K', 'children'),
              [Input('K', 'value')])
def check_input_K(K):
    if K<0:
        return f'Cannot be lower than 0.'
    else:
        return ""
    
@app.callback(Output('message_TS', 'children'),
              [Input('T', 'value'),
              Input("TS", "value")])
def check_input_dt(T, TS):
    if TS>506:  
        return f'Higher than 506 time steps will make the app run slowly'
    elif TS < T:
        return f"Cannot be lower than {T}"
    else:
        return ""
    
@app.callback(Output('message_M', 'children'),
              [Input('M', 'value')])
def check_input_S(M):
    if M>1000000:
        return f'More than 100000 simulation will make the app run slowly'
    else:
        return ""
    
@app.callback(Output('message_MC', 'children'),
              [Input('MC', 'value')])
def check_input_MC(MC):
    if MC>100:
        return f'Doing the simulation more than 100 times will make the app run slowly'
    else:
        return ""

## DISPLAYING PRICE
@app.callback(Output('PriceMod1', 'children'),
              Output('SEMod1', 'children'),
              Output('ConfIntMod1', 'children'),
              [Input('memory-output', 'data'),])
def display_price(data):
    Price,Price2,SE,SE2,seed, PriceVec1,PriceVec2, ModelSel, ModelSel2 = data
    LowInt = np.round(Price - norm.ppf(0.975)*SE,3)
    HighInt = np.round(Price + norm.ppf(0.975)*SE,3)
    return f': {np.round(Price,4)}', f': {np.round(SE,4)}', f': [{LowInt} ; {HighInt}]'

@app.callback(Output('PriceMod2', 'children'),
              Output('SEMod2', 'children'),
              Output('ConfIntMod2', 'children'),
              [Input('memory-output', 'data'),])
def display_price(data):
    Price,Price2,SE,SE2,seed, PriceVec1,PriceVec2, ModelSel, ModelSel2 = data
    LowInt = np.round(Price2 - norm.ppf(0.975)*SE2,3)
    HighInt = np.round(Price2 + norm.ppf(0.975)*SE2,3)
    return f': {np.round(Price2,4)}', f': {np.round(SE2,4)}', f': [{LowInt} ; {HighInt}]'


## INPUTS VISUALS
@app.callback(Output('Risk-free', 'children'),
              [Input('rf', 'value')])
def display_value_mu(value):
    return f': {int(value*100)}%'

@app.callback(Output('sigma', 'children'),
              [Input('vol', 'value')])
def display_value_vol(value):
    return f': {int(value*100)}%'

@app.callback(Output('matu', 'children'),
              [Input('T', 'value')])
def display_value_T(value):
    if value==0.25 or value==0.5 or value==0.75:
        return f": {int(value*12)} months"
    elif value == 1:
        return f': {value} year'
    else:
        return f': {value} years'
    
##MISC
@app.callback(
    Output("popover", "is_open"),   
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("list", "is_open"),
    [Input("model-list", "n_clicks")],
    [State("list", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

## MAIN FUNCTION
if __name__ == '__main__':
    app.run_server(debug=True)